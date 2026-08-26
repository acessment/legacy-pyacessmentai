from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
# Get OpenAI API key from dotenv
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

model4oDiy = ChatOpenAI(
    model="ft:gpt-4o-2024-08-06:acessment:p1-6-englishv1:ASI6c1Ok",
    api_key=OPENAI_API_KEY,
    temperature=0.7,
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
