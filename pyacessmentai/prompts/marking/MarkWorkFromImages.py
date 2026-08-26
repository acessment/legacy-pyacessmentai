from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
# Get OpenAI API key from dotenv
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
model4o = AzureChatOpenAI(
    azure_endpoint="https://ACEssmentSponsoredAI1.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview",
    azure_deployment="gpt-4o",
    api_version="2024-08-01-preview",
    api_key=AZURE_API_KEY,
    temperature=0.3,
)
mark_work_system = SystemMessage(
    "You are a teacher seeing a student's homework. Ignore the already marked parts (review of previous exercise). Pay attention to his mistakes. Point out spelling mistakes, but treat abbreviations and informal language as correct. "
)


def getChain(image_b64s):
    mark_work_human = HumanMessagePromptTemplate.from_template(
        template=image_b64s
        + [
            {
                "type": "text",
                "text": """
                Output the step by step marking process of the student's homework as shown below:
                First directly List out the student's answers (handwritten part). 
                Then list out the model answers.
                Finally mark each answer according to the following rules:
                Please mark each answer by the question as correct or incorrect. Treat each blank as a separate question. By comparing the student's answer to the model answer: {answers}.  If incorrect, give explanations like a teacher patiently telling the student why the answer is wrong. Use a mix of Traditional Chinese and English like the example.
                
                Example: 
                Students answer:
                1. a
                2. an
                Model answer:
                1. an
                2. an
                Marking:
                1. I eat a apple. (Incorrect) 這裏的名詞是Apple，Apple以a開頭，以元音字母（a,e,i,o,u）開頭的單字前要加an，而a只適用非元音開頭的單字，所以正確答案是"an"。
                2. She eats an orange. (Correct)
                """,
            },
        ]
    )
    mark_work_prompt = ChatPromptTemplate(messages=[mark_work_system, mark_work_human])
    return mark_work_prompt | model4o | StrOutputParser()
