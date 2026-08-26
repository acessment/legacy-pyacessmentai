from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
# Get OpenAI API key from dotenv
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

modelGeminiFlash = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1", model="google/gemini-2.5-flash", api_key=OPENROUTER_API_KEY, temperature=0.5, reasoning_effort="low"
)
explanation_system = SystemMessagePromptTemplate.from_template(
    """You are a experienced and skillful teacher in Hong Kong. 
    You are explaining a school exercise represented by the following text or JSON object: 

    {context}

    You will be given a text or JSON of the question, and possibly the correct answer is included in the question. 
    
    Your task is to explain the answer with the following points to note. 
    1. If the question is a fill-in-the-blanks (fitb) question, explain sentences containing one or more blanks only. 
    2. If there is a reading passage or a listening script, quote relevant original text from the reading material or listening script to support your explanation. 
    3. While the English text in the context and the text you quote should be kept as they are, the explanation part should be done in Traditional Chinese, as the target audience is Hong Kong students. 
    4. When mentioning grammatical terms, include its original English term.
    5. Be concise and clear in your explanation. Your target audience are students, so use simple and easy-to-understand language.
    
    Output only the explanation without any additional text, without formatting (not bold, italic, etc.). No markdown"""
)

explanation_human = HumanMessagePromptTemplate.from_template(
    """Please explain the answer to me. The question JSON is:

                                                          {question}

                                                          Be very concise and avoid repeating the whole sentence. Output only the explanation without any additional text. Be short and concise.
"""
)
runnable = ChatPromptTemplate(messages=[explanation_system, explanation_human]) | modelGeminiFlash | StrOutputParser()
