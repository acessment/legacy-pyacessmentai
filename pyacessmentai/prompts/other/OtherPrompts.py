from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from dotenv import load_dotenv
import os

from pyacessmentai.models import ExerciseResponse, ExerciseItem
from pyacessmentai import schema
from importlib import resources

load_dotenv()
# Get OpenAI API key from dotenv
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PPLX_API_KEY = os.getenv("PPLX_API_KEY")
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
IMG2JSON_API_KEY = os.getenv("IMG2JSON_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")

model4o = AzureChatOpenAI(
    azure_endpoint="https://ACEssmentSponsoredAI1.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview",
    azure_deployment="gpt-4o",
    api_version="2024-08-01-preview",
    api_key=AZURE_API_KEY,
    temperature=0.3,
)
model4oMini = AzureChatOpenAI(
    azure_endpoint="https://ACEssmentSponsoredAI1.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-08-01-preview",
    azure_deployment="gpt-4o-mini",
    api_version="2024-08-01-preview",
    api_key=AZURE_API_KEY,
    temperature=0.7,
)
model4oDiy = ChatOpenAI(
    model="ft:gpt-4o-2024-08-06:acessment:p1-6-englishv1:ASI6c1Ok",
    api_key=OPENAI_API_KEY,
    temperature=0.5,
)

modelO4mini = AzureChatOpenAI(
    azure_endpoint="https://seanx-ma2b6hay-eastus2.openai.azure.com/openai/deployments/o4-mini/chat/completions?api-version=2025-01-01-preview",
    azure_deployment="o4-mini",
    api_version="2024-12-01-preview",
    api_key=IMG2JSON_API_KEY,
    temperature=1.0,
    reasoning_effort="medium",
)

modelGemini25 = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1", model="google/gemini-2.5-pro-preview", api_key=OPENROUTER_API_KEY, temperature=0.3
)
modelGemini20Flash = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1", model="google/gemini-2.0-flash-001", api_key=OPENROUTER_API_KEY, temperature=0.3
)

modelGemini25Flash = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    model="google/gemini-2.5-flash",
    api_key=OPENROUTER_API_KEY,
    temperature=0.5,
    reasoning_effort="medium",
)

modelGrok3 = ChatOpenAI(base_url="https://api.x.ai/v1/", model="grok-3", api_key=XAI_API_KEY, temperature=0.5)

Img2JsonSystem = """You are performing digitalization of some exercises. Your job is to output the JSON format of the given exercise. 
RULES:
a. You must output a json object having the property called 'response' and the value are some exercise JSON objects. Your target output JSON schema is provided below. 
b. Only include fill in the blanks, multiple choice, true false not given, and short questions/open ended questions. Some questions might not suit well in the json schema. If you can slightly change the format while fitting it into the json schema, you should format it and make sure the meaning and the completeness of the question maintains after formatting. Otherwise ignore and skip the question.
c. You should skip and ignore questions containing images that affects the ability to be answered (if removing the images makes answering impossible, skip and ignore the question. In contrast, if images are for decorations only, you can still process the question but just remove the images.
d. For mcq, you should remove questions having more than one answer.
e. The reading field can be formatted by HTML. Make sure all tags are closed properly, especially the <br/> tag. 
f. If the question refers some texts at a line number, you should remove the line number reference and quote the text directly. You may slightly change the wording. But I don't want to see any line number reference in the output. If removing the line number reference is not possible, you should skip and ignore the question.
g. The content of the question must be exactly the same as the image content. You should not change the content of the question unless it is necessary for fitting into the json schema or removing line number references.

During your reasoning, you should:
1. first draft a digitalized json object. 
2. If no answer is provided, you should give suggested answers by giving values to the 'answer' and 'blank' fields.
3. Check if the draft fits the json schema, the above rules, and the user instructions. If it does not fit, or does not make sense after forcefully fitting it to the json schema, you should ignore the question/exercise and skip it.


Json schema:
""" + resources.read_text(
    schema, "exercise_response_json.schema.json"
)


def get_img2json_runnable(encodedImages):
    import json

    return ChatPromptTemplate(
        [
            SystemMessage(Img2JsonSystem),
            HumanMessagePromptTemplate.from_template(
                template=[
                    *[
                        {
                            "type": "image_url",
                            "image_url": encodedImage,
                        }
                        for encodedImage in encodedImages
                    ],
                    {
                        "type": "text",
                        "text": "{user_prompt}",
                    },
                ]
            ),
        ],
    ) | modelGemini25.with_structured_output(json.loads(resources.read_text(schema, "exercise_response_json.schema.json")))


json2PromptSystem = "You are generating synthetic data for fine-tuning a LLM. You will be given a json of an exercise, which is the expected output, and the level of that exercise (primary 1 to secondary 6 or DSE or Taiwan GSAT or IELTS ). You will then pretend you are a teacher using an AI tool and write a prompt for generating the given exercise, include a very brief topic and number of questions. The prompt should include minimal instructions without outlining the exercise in detail. Include the level (primary/secondary 1-6/DSE/Taiwan GSAT/IELTS) and subject (English reading/grammar/listening; Maths; Chinese). Output the prompt only and make it short and concise."
json2PromptRunnable = (
    ChatPromptTemplate(
        [
            SystemMessage(json2PromptSystem),
            HumanMessagePromptTemplate.from_template(
                "Output a prompt in {language}.\nLevel: {level}\nExercise: {exercise_json}",
            ),
        ],
    )
    | modelGemini20Flash
    | StrOutputParser()
)

diyPromptSystem = "You are a teacher drafting English exercises in Hong Kong Primary School exam format. Please output one single json object. containing an instruction, a reading (optional), a options array (optional), array of questions. Question array contains objects with type mcq (multiple choice), fitb (fill in the blanks), or sq (short questions). mcq and sq have answer property. fitb has question array with type and text properties. mcq has options object."
diyPromptRunnable = (
    ChatPromptTemplate(
        [
            SystemMessage(diyPromptSystem),
            HumanMessagePromptTemplate.from_template(
                "{user_prompt}",
            ),
        ],
    )
    | model4oDiy
    | JsonOutputParser()
)

cloneExerciseSystem = "You will be given a JSON object representing an exercise for students. Output a JSON object of the same schema containing an exercise having the similar format, structure and complexity but different content based on the provided json object. Output only the json object. Do not output anything else."
cloneExerciseRunnable = (
    ChatPromptTemplate(
        [
            SystemMessage(cloneExerciseSystem),
            HumanMessagePromptTemplate.from_template(
                "{exercise_json}\n\nGiven the above json, output another exercise in the same JSON schema. {user_prompt}. Output only the json object.",
            ),
        ],
    )
    | modelGrok3
    | JsonOutputParser()
)

outputEnhancerPromptSystem = """You are an expert in enhancing educational exercises for students. 
Your task is to take an existing exercise JSON and improve it. 
Ensure that the enhanced exercise maintains the same schema as the input JSON while improving the quality of the content. 
Output only the enhanced exercise JSON without any additional text.

Background information:
The exercise is generated by another AI model. 
The setup is specialized in generating exercises that are similar to the required exam formats, but it has the following limitations:
1. The model may be fine-tuned on smaller datasets, which can lead to less diverse content and overfitting. There might be repetitive sentences.
3. The questions and answers might be too direct and not thought-provoking enough.
4. The resulting exercises may not fully align with the user instructions, such as the specified number of questions or required tenses in a mixed tense exercise.
5. The questions may be hard to answer realistically. For example, word too difficult to spell in a listening exercise, or too complex to answer in a short time. 
6. The questions may be repetitive or very similar to each other.
7. Some content may not be suitable for the target age group.
8. In reading and listening exercises, the questions may not be spread evenly across the entire article/audio. Some parts of the article/audio may have no questions at all, while other parts may have too many questions.

Your enhancement should focus on:
1. Identify ONLY obvious repetitive sentences and rephrase them.
2. Paraphrasing questions to make them less direct.
3. Ensuring that the exercise fully meets the user instructions, including the number of questions and specific requirements.
4. Check for questions that are unrealistic to answer and modify or remove them to be more practical.
5. Check for any repetitive or very similar questions and modify or remove them to enhance variety.
6. Ensuring all content is age-appropriate for the intended students.
7. In reading and listening exercises, ensure questions are evenly distributed throughout the article/audio.

NOTE: In multiple choice questions, having an underline represented by underscores and asking for the most suitable option to fill in the underline is a common practice. It is not a problem unless there are other issues mentioned above.

Most parts of the exercise should remain unchanged. In your reasoning step, you should:
1. Analyze the level of difficulty in terms of vocabulary, style (point form vs complete sentences, wordings of questions, etc), and sentence structure. Remember to only use the limited sets of vocabulary and grammar suitable for the target age group all the time.
2. Identify areas that are obviously bad. The exercise can be perfect and no enhancement is needed.
3. Only enhance the parts that are obviously bad based on the above focus points.
"""
outputEnhancerPromptRunnable = (
    ChatPromptTemplate(
        [
            SystemMessage(outputEnhancerPromptSystem),
            HumanMessagePromptTemplate.from_template(
                "The user instructions are: {user_prompt}.\n\nPlease enhance this exercise json:\n\n{exercise_json}",
            ),
        ],
    )
    | modelGemini25Flash
    | JsonOutputParser()
)
