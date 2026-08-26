from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import JsonOutputParser
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

mark_json_human = HumanMessagePromptTemplate.from_template(
    '{marking}\nExample: [{{"student_answer":"a", "correct_answer": "an", "is_correct": false, "explanation":"Apple以a開頭，以元音字母（a,e,i,o,u）開頭的單詞前要加an"}},{{"student_answer":"the", "is_correct": true}}] Format the marking in JSON like the example. Start from the first question. Include both correct and inscorrect questions.'
)
runnable = ChatPromptTemplate(messages=[mark_work_system, mark_json_human]) | model4o | JsonOutputParser()
