from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

modelGeminiFlash = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    model="google/gemini-2.5-flash",
    api_key=OPENROUTER_API_KEY,
    temperature=1.0,
    reasoning_effort="medium",
)

ocr_work_prompt = 'Please extract the text in the images. \
In addition to simple OCR, if there are multiple choice questions, indicate the choice of the blackened circle next below the question text, by clearly saying "Student answer: <answer>" \
Preserve the original text and keep the spelling and grammatical mistakes as is. Output only the extracted text and the selected answers of the multiple choice questions below the question text.'


def getOcrRunnable(image_chat_object):
    mark_work_human = HumanMessagePromptTemplate.from_template(
        template=[image_chat_object]
        + [
            {
                "type": "text",
                "text": ocr_work_prompt,
            },
        ]
    )
    mark_work_prompt = ChatPromptTemplate(messages=[mark_work_human])
    return mark_work_prompt | modelGeminiFlash | StrOutputParser()


marking_json_prompt = "Given the OCR result of a student's work and the json array of exercise objects, \
Add fields to the same json array of exercises object: add the properties 'student_answer' and 'is_correct' to each object with type 'mcq', 'blank', or 'sq'. \
The 'student_answer' property should contain the student's answer extracted from the OCR result, and the 'is_correct' property should be a boolean indicating whether the answer is correct. Output the complete input json array with the added properties."

marking_json_human = HumanMessagePromptTemplate.from_template(
    "OCR result: {ocr_result}\n. Exercise objects: {exercise_objects}\n" + marking_json_prompt
)
marking_json_runnable = ChatPromptTemplate(messages=[marking_json_human]) | modelGeminiFlash | JsonOutputParser()
