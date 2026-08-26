from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
# Get OpenAI API key from dotenv
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
model4oMarking = ChatOpenAI(
    model="ft:gpt-4o-2024-08-06:acessment:markingocr2:ApXUHctP",
    api_key=OPENAI_API_KEY,
    temperature=0.3,
)
mark_work_system = SystemMessage(
    "You are a teacher seeing a student's homework. Ignore the already marked parts (review of previous exercise). Pay attention to his mistakes. Point out spelling mistakes, but treat abbreviations and informal language as correct. Students may also do multiple choice questions, for each question, give the choice of the blackened circle (A/B/C/D/T/F/NG).",
)


def getChain(image_b64s):
    mark_work_runnable = getRunnable(image_b64s)

    return mark_work_runnable | JsonOutputParser()


def getRunnable(image_b64s):
    mark_work_human = HumanMessagePromptTemplate.from_template(
        template=image_b64s
        + [
            {
                "type": "text",
                "text": """
                Example: ["some", "text", "here", "A", "some long answer here", "B", "short text",  "F", "NG", "some long answer here"]
                Extract all the handwritten parts of what the student wrote, and the blacken circles for each line. Give the raw text the handwritten text, or the choice of the blackened circle (A/B/C/D/T/F/NG) Put the result one by one in a JSON array of strings.
                """,
            },
        ]
    )
    mark_work_prompt = ChatPromptTemplate(messages=[mark_work_system, mark_work_human])
    return mark_work_prompt | model4oMarking
