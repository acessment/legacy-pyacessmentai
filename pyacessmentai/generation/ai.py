from langchain_core.runnables import RunnableParallel
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
import io, os, base64, json

from dotenv import load_dotenv

from pyacessmentai.question_class.CategoryType import Category
from pyacessmentai.scripts.DefinedChatModel import DefinedChatModel
from pyacessmentai.prompts.reading import ReadingGenerator, LLMModelType, Difficulty
from pyacessmentai.prompts import PromptIndex
from pyacessmentai.scripts.TensesType import TensesType

from langchain_core.output_parsers import StrOutputParser

str_parser = StrOutputParser()

load_dotenv()

GOOGLE_CLOUD_API_KEY = os.getenv("GOOGLE_CLOUD_API_KEY")
AI_STUDIO_API_KEY = os.getenv("AI_STUDIO_API_KEY")


from pyacessmentai.prompts.listening import (
    listeningCopyCatNonsenseRunnable,
    listeningCopyCatGenScriptRunnable,
    listeningQuestionGenRunnable,
    listeningDSEQuestionsRunnable,
    listeningDSEScriptRunnable,
    listeningNoExamplePerplexityRunnable,
    listeningP6TSARunnable,
    listeningGetGenderRunnable,
    get_nonsense_infosheet_chain,
    listeningCopyCatInfosheetRunnable,
)

from pyacessmentai.scripts import common_parser

from pyacessmentai.prompts.other.OtherPrompts import (
    get_img2json_runnable,
    json2PromptRunnable,
    diyPromptRunnable,
    cloneExerciseRunnable,
    outputEnhancerPromptRunnable,
)


def enhance(exercise_json: dict, user_prompt: str = ""):
    return outputEnhancerPromptRunnable.invoke({"exercise_json": exercise_json, "user_prompt": user_prompt})


def generate_diy_exercise(prompt, stream=False):
    return diyPromptRunnable.invoke({"user_prompt": prompt}) if not stream else diyPromptRunnable.stream({"user_prompt": prompt})


def generate_reading_article(prompt, model_id, word_count, level):
    # Returns a dict containing the 'title' and 'content' of the article
    if model_id == "sonar":
        RG: ReadingGenerator = ReadingGenerator(article_model=LLMModelType.Online_llma_3_1)
    else:
        RG: ReadingGenerator = ReadingGenerator(article_model=LLMModelType.Offline_GPT4o)
    outline = RG.create_article_outline(
        prompt,
        word_count=word_count,
        level=Difficulty[level],
    )

    res = RG.create_article(
        outline,
        prompt,
        word_count=word_count,
        level=Difficulty[level],
    )
    return res


def generate_reading_exercise(title, article, hasFitB, hasSQ, hasTFNG, level, totalNumOfQ):
    RG = ReadingGenerator()
    res = RG.custom_create_exercise_fr_article(
        title=title,
        article=article,
        hasFitB=hasFitB,
        hasSQ=hasSQ,
        hasTFNG=hasTFNG,
        level=Difficulty[level],
        totalNumOfQ=totalNumOfQ,
    )
    res["category"] = Category.READING.value
    return res


def generate_new_ex(
    selected_exercises=[],
    start_index=0,
    numOfQ=7,
    theme="toys",
    remarks="use easy words",
    tenses="",
    hasExamples=False,
):
    batch_params = {i: {"remarks": remarks} for i, exercise in enumerate(selected_exercises)}
    batch_runnables = {
        i: {
            "numOfQ": lambda x: numOfQ,
            "theme": lambda x: theme,
            "remarks": lambda x: remarks,
            "word_count": lambda x: 90,
            "tenses": lambda x: tenses,
        }
        | exercise.build_chain()
        for i, exercise in enumerate(selected_exercises)
    }

    results = RunnableParallel(batch_runnables).invoke(batch_params)
    new_exercises = []
    for key, result in results.items():
        exercise_type = selected_exercises[int(key)]
        new_exercises.append(
            exercise_type.full_exercise_dict(
                common_parser.exercise_parser(exercise_type, result),
                haveExamples=hasExamples,
            ),
        )

    new_exercise_dicts = [new_ex for new_ex in new_exercises]
    for i, exercise in enumerate(new_exercise_dicts):
        exercise["title"] = f"Exercise {i+start_index+1} -- {exercise.get('title')}"

    return new_exercise_dicts


# We should gradually deprecate generate_new_ex and replace it with generate_grammar_exercise
def generate_grammar_exercise(selected_exercise_id: int, theme: str, remarks: str, tenses: list, totalNumOfQ: int, hasExamples: bool):
    selected_exercise = PromptIndex.prompt_index_dict[selected_exercise_id]
    tenses_str = ", ".join([TensesType.get_tenses_dict()[int(t)].value for t in tenses]) if tenses else ""
    result = selected_exercise.build_chain().invoke(
        {"numOfQ": totalNumOfQ, "theme": theme, "remarks": remarks, "word_count": 90, "tenses": tenses_str}
    )
    exercise = selected_exercise.full_exercise_dict(
        common_parser.exercise_parser(selected_exercise, result),
        haveExamples=hasExamples,
    )
    exercise["title"] = selected_exercise.title
    exercise["category"] = Category.GRAMMAR.value
    return exercise


def generate_listening_script(
    theme,
    model_id,
    word_count=300,
    stream=False,
    example_script=None,
    level="P6",
):
    # 6 Aug 2025: The level param is now only used for determining whether to use the DSE model when no internet is required.
    if example_script:
        combined_chain = {
            "tapescript": listeningCopyCatNonsenseRunnable,
            "theme": lambda x: x["theme"],
        } | listeningCopyCatGenScriptRunnable
    elif model_id == "sonar":
        combined_chain = listeningNoExamplePerplexityRunnable
    else:
        combined_chain = listeningP6TSARunnable if (level != "S4-6" and level != "S4_S6") else listeningDSEScriptRunnable
    return (
        combined_chain.invoke({"theme": theme, "tapescript": example_script, "length": word_count}).replace("’", "'")
        + (f"\n\n{level}" if level == "S4_S6" else "")
        if not stream
        else combined_chain.stream({"theme": theme, "tapescript": example_script, "length": word_count})
    )


def generate_listening_questions_nonsense(tapescript, reference):
    copycatRunnable = {
        "infosheet": get_nonsense_infosheet_chain(reference),
        "tapescript": lambda x: tapescript,
    } | listeningCopyCatInfosheetRunnable
    return copycatRunnable.invoke({})


def generate_listening_questions(tapescript, level="P6", word_count=300, theme=None, stream=False):
    # 6 Aug 2025: The level, theme, and word_count params are now only used for DSE level listening questions.
    if (level == "S4-6" or level == "S4_S6") and theme:
        return (
            listeningDSEQuestionsRunnable.invoke({"tapescript": tapescript, "theme": theme, "length": word_count})
            if not stream
            else listeningDSEQuestionsRunnable.stream({"tapescript": tapescript, "theme": theme, "length": word_count})
        )
    return (
        listeningQuestionGenRunnable.invoke({"tapescript": tapescript})
        if not stream
        else listeningQuestionGenRunnable.stream({"tapescript": tapescript})
    )


def get_listening_gender(tapescript):
    # Returns a JSON list of genders like ["male", "female", "male"]
    return listeningGetGenderRunnable.invoke({"tapescript": tapescript})


def generate_speech(ssml, speed=0.7):
    from google.cloud.texttospeech import TextToSpeechClient, SynthesisInput, VoiceSelectionParams, AudioConfig, AudioEncoding

    # Creates a client
    client = TextToSpeechClient(client_options={"api_key": GOOGLE_CLOUD_API_KEY})

    # Set up request parameters
    synthesis_input = SynthesisInput(ssml=ssml)

    voice = VoiceSelectionParams(language_code="en-US", name="en-US-Studio-O")
    print("speed", speed)
    audio_config = AudioConfig(audio_encoding=AudioEncoding.MP3, speaking_rate=speed)

    # Perform the text-to-speech request
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    # Return the audio content
    return response.audio_content


def generate_premium_speech(prompt, voice):
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=AI_STUDIO_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.5-pro-preview-tts",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=voice,
                    )
                )
            ),
        ),
    )
    print("TTS response:", response)
    return response.candidates[0].content.parts[0].inline_data.data


def call_tts(
    tapescript_json, gender, situation="Listening Exercise", speed=0.7, intro=True, filename="listening_1.mp3", return_b64=False, premium=False
):
    from pydub import AudioSegment
    import random

    # Aceessment is intentionally spelled like this
    ssml = (
        f"""
    <speak><voice name="en-GB-Neural2-B">This computer-generated voice recording is for listening practice only. 
    Some information may not be accurate or factual.<break time="2s"/>
    You now have 30 seconds to study the questions. <say-as interpret-as="expletive">censor this</say-as>
    <break time="30s"/>The recording starts now. <break time="1s"/></voice>
    """
        if intro
        else "<speak>"
    )

    audio_segment = None

    if premium and return_b64:
        # Premium voice generation intended for Catherine and premium subscribers
        voice_list = {
            "male": ["Charon", "Umbriel", "Achird", "Sadaltager"],
            "female": ["Callirrhoe", "Achernar", "Gacrux", "Leda"],
        }
        speed_indicator = ", read a little bit quicker" if speed > 1 else ", read a little bit slower" if speed < 1 else ""
        # Pop the last item from the tapescript for gender info
        # genders = tapescript_json.pop()

        voices = {}
        if intro:
            audio_segment = AudioSegment.from_mp3(io.BytesIO(generate_speech(ssml + "</speak>", speed=speed)))
        for dialog in tapescript_json:
            if len(dialog) > 2:
                dialog[1] = " ".join(dialog[1:])
                dialog = dialog[:2]
            if len(dialog) < 2:
                continue

            speaker, speech = dialog
            if speaker not in voices:
                voices[speaker] = voice_list[gender.pop(0) if gender else random.choice(["male", "female"])].pop()
            prompt = f"Read aloud in a warm and friendly tone{speed_indicator}:\n{speech}"
            if not audio_segment:
                audio_segment = AudioSegment.from_raw(
                    io.BytesIO(generate_premium_speech(prompt, voices[speaker])), sample_width=2, frame_rate=24000, channels=1
                )
            else:
                audio_segment = audio_segment + AudioSegment.from_raw(
                    io.BytesIO(generate_premium_speech(prompt, voices[speaker])), sample_width=2, frame_rate=24000, channels=1
                )
            audio_segment = audio_segment + AudioSegment.silent(duration=500)  # 0.5 second pause between dialogues

        buffer = io.BytesIO()
        audio_segment.export(buffer, format="mp3")
        buffer.seek(0)
        audio_base64 = base64.b64encode(buffer.read()).decode("utf-8")
        return f"data:audio/mp3;base64,{audio_base64}"

    else:

        # If return_b64 is True, return the base64 encoded audio content instead of saving to a file and returning the file path.
        print("call tts speed", speed)
        voice_list = {
            "male": ["en-AU-Neural2-B", "en-GB-Studio-B", "en-US-Studio-Q"],
            "female": ["en-AU-Neural2-A", "en-GB-Studio-C", "en-US-Studio-O"],
        }
        # Pop the last item from the tapescript for gender info
        # genders = tapescript_json.pop()

        voices = {}

        for dialog in tapescript_json:
            if len(dialog) > 2:
                dialog[1] = " ".join(dialog[1:])
                dialog = dialog[:2]
            if len(dialog) < 2:
                continue
            speaker, speech = dialog

            if len(ssml) + len(speech) >= 4800:
                ssml += "</speak>"
                if not audio_segment:
                    audio_segment = AudioSegment.from_mp3(io.BytesIO(generate_speech(ssml, speed=speed)))
                else:
                    audio_segment = audio_segment + AudioSegment.from_mp3(io.BytesIO(generate_speech(ssml, speed=speed)))
                ssml = "<speak>"

            if speaker not in voices:
                try:
                    voices[speaker] = voice_list[gender.pop(0) if gender else random.choice(["male", "female"])].pop()
                except:
                    voices[speaker] = random.choice(voice_list["male"] + voice_list["female"])

            voice_name = voices[speaker]
            ssml += f'<voice name="{voice_name}">{speech}</voice><break time="1s"/>'

        ssml += '<voice name="en-GB-Neural2-B">This is the end of the recording.</voice></speak>'

        if not audio_segment:
            audio_segment = AudioSegment.from_mp3(io.BytesIO(generate_speech(ssml, speed=speed)))
        else:
            audio_segment = audio_segment + AudioSegment.from_mp3(io.BytesIO(generate_speech(ssml, speed=speed)))

        if return_b64:
            # Convert the audio segment to bytes and then to base64
            buffer = io.BytesIO()
            audio_segment.export(buffer, format="mp3")
            buffer.seek(0)
            audio_base64 = base64.b64encode(buffer.read()).decode("utf-8")
            return f"data:audio/mp3;base64,{audio_base64}"
        else:
            # Save the file to a temporary location, and return the path
            with open(f"temp/{filename}", "wb") as f:
                audio_segment.export(f, format="mp3")
            return f"temp/{filename}"


def image_to_json(
    imagebytes,
    stream=False,
    user_prompt="Please extract questions from the image and provide the output in json format.",
):
    return imageb64s_to_json(
        [base64.b64encode(imgbyte).decode("utf-8") for imgbyte in imagebytes],
        stream=stream,
        user_prompt=user_prompt,
    )


def imageb64s_to_json(
    imageb64s,
    stream=False,
    user_prompt="Please extract all suitable exercises from the images and provide the output in json format. Remove question numbers. Remove question numbers and indicators like (e.g.) (example). Output the json only.",
):
    if stream:
        return get_img2json_runnable([f"{imageb64}" for imageb64 in imageb64s]).stream({"user_prompt": user_prompt})
    else:
        return get_img2json_runnable([f"{imageb64}" for imageb64 in imageb64s]).invoke({"user_prompt": user_prompt})


def json_to_prompt(level, exercise_json, stream=False, language="English"):
    if stream:
        return json2PromptRunnable.stream({"level": level, "exercise_json": exercise_json, "language": language})
    else:
        return json2PromptRunnable.invoke({"level": level, "exercise_json": exercise_json, "language": language})


def jsons_to_prompt(level, exercise_jsons, language="English"):
    return json2PromptRunnable.batch(
        [{"level": level, "exercise_json": json.dumps(exercise_json), "language": language} for exercise_json in exercise_jsons]
    )


def clone_exercise(imageb64s, user_prompt=""):
    exercise_jsons = imageb64s_to_json(imageb64s).get("response", [])
    return cloneExerciseRunnable.batch([{"user_prompt": user_prompt, "exercise_json": exercise_json} for exercise_json in exercise_jsons])


def get_exercise_translation(exercise_json: dict):
    trimmed_json = {"reading": exercise_json.get("reading"), "questions": exercise_json.get("questions")}
    GET_TRANSLATION_SYSTEM_PROMPT = """
    You will be given a json representation of an English exercise. 
    Please only consider the value of each key-value pair. 

    Find some vocabularies that are difficult to understand for an average english learner. You should find at least 3 vocabularies but not more than 9.

    Output the traditional chinese translation and the original english verb in the following format, include the parts of speech next to the vocabulary in the brackets.:

    1. apple(n.) 蘋果  2. play(v.) 玩耍
    """

    GET_TRANSLATION_USER_PROMPT = "{json}"
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=GET_TRANSLATION_SYSTEM_PROMPT),
            HumanMessagePromptTemplate.from_template(GET_TRANSLATION_USER_PROMPT),
        ]
    )
    llm_chain = prompt | DefinedChatModel.GPT4oMini.value | str_parser

    results = llm_chain.invoke({"json": str(trimmed_json)})
    return results.replace("\n", "    ")


def mark_work_v2(image_b64s: list, exercise_jsons: list):
    from pyacessmentai.prompts.marking.MarkingV2 import (
        getOcrRunnable,
        marking_json_runnable,
    )

    image_chat_objects = []
    for image_b64 in image_b64s:
        image_chat_objects.append(
            {
                "type": "image_url",
                "image_url": {"url": f"{image_b64}"},
            }
        )

    ocr_parallel_runnable = RunnableParallel({f"{key}": getOcrRunnable(value) for key, value in enumerate(image_chat_objects)})
    ocr_results = ocr_parallel_runnable.invoke({})
    ocr_complete_string = "\n".join([ocr_results[f"{key}"] for key in sorted(ocr_results.keys())])
    print("OCR Results:", ocr_complete_string)
    return marking_json_runnable.invoke({"ocr_result": ocr_complete_string, "exercise_objects": json.dumps(exercise_jsons)})


def get_explanation_v2(context: str, question: str):
    from pyacessmentai.prompts.marking.GetExplanation import runnable as explanation_runnable

    explanation = explanation_runnable.invoke(
        {
            "context": context,
            "question": question,
        }
    )
    return explanation
