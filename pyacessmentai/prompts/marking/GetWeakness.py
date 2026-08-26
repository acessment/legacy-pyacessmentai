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
    "You are an education specialist. Your job is to see the feedback from a teacher on a student's work. Do not give vague summaries (e.g. student is weak at simple past tense). You give specific and insightful feedback (e.g. student need more practice on irregular verbs and verbs ending with y when using simple past tense)."
)

weakness_human = HumanMessagePromptTemplate.from_template(
    "{marking}\nBased on the feedback, pinpoint the student's weaknesses and the specific areas that need improvement."
)
runnable = ChatPromptTemplate(messages=[mark_work_system, weakness_human]) | model4o | StrOutputParser()
