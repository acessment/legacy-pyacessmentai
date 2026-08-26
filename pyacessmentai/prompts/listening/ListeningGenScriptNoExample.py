from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_perplexity import ChatPerplexity
from dotenv import load_dotenv
import os

load_dotenv()
# Get OpenAI API key from dotenv
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PPLX_API_KEY = os.getenv("PPLX_API_KEY")
AZURE_API_KEY = os.getenv("AZURE_API_KEY")

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
    temperature=0.3,
)
modelPerplexity = ChatPerplexity(model="sonar", api_key=PPLX_API_KEY)
modelP6TSA = ChatOpenAI(
    model="ft:gpt-4o-2024-08-06:acessment:p6-listening:A6cILiH7",
    api_key=OPENAI_API_KEY,
    temperature=0.7,
)

modelDSE = ChatOpenAI(
    model="ft:gpt-4.1-2025-04-14:acessment:dselisteningscript:C1DZW415",
    api_key=OPENAI_API_KEY,
    temperature=1.0,
)


listeningNoExampleSystem = "Please write a script of two or three people speaking, having both male and female. The speaker should have names. The discussion should only be between two or three people (including the host). Do not include any action description such as playing music. The script will be used for a listening exercise for students. Avoid mentioning specific company names. The script will be used for a listening exercise for students. Output with the format of <name> : <dialog>. Such as Peter: Hello! Output in plaintext. Do not put asterisks. Do not bold text."
listeningNoExampleHuman = "The discussion is about {theme}. Please make this understandable by all students. Do not include technical terms and anything that required background knowledge to understand. Give names to every person, do not use placeholders like Guest 1, Host. Use real english names. The script should be around {length} words."
listeningNoExampleHumanPerplexity = "Search topic: {theme}\n\n The discussion is about {theme}. Please make this understandable by all students. Do not include technical terms and anything that required background knowledge to understand. Give names to every person, do not use placeholders like Guest 1, Host. Use real english names. The script should be around {length} words. Output in plain text. Do not output anything other that the script. Start your output with the format <name of speaker(no bold text)>: <content spoken>. Good example: Mary: Hello.\nPeter: Hi, Mary."

listeningNoExamplePrompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=listeningNoExampleSystem),
        HumanMessagePromptTemplate.from_template(listeningNoExampleHuman),
    ]
)

listeningNoExamplePerplexityPrompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=listeningNoExampleSystem),
        HumanMessagePromptTemplate.from_template(listeningNoExampleHumanPerplexity),
    ]
)

listeningNoExampleRunnable = listeningNoExamplePrompt | model4o | StrOutputParser()

listeningNoExamplePerplexityRunnable = listeningNoExamplePerplexityPrompt | modelPerplexity | StrOutputParser()

listeningP6TSASystem = "You are a teacher drafting a tapescript for a recording for a listening assessment in the Hong Kong TSA targeting Primary 6 students. Please output in the format of <speaker>: <content>."
listeningP6TSAHuman = "Please draft a tapescript of a conversation. It should be about {theme}. The script should be around {length} words."
listeningP6TSARunnable = (
    ChatPromptTemplate.from_messages(
        [
            SystemMessage(listeningP6TSASystem),
            HumanMessagePromptTemplate.from_template(listeningP6TSAHuman),
        ]
    )
    | modelP6TSA
    | StrOutputParser()
)

listeningGetGenderRunnable = (
    ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                'You will be given a tapescript, you need to return a json array of the gender of each distinct speaker in sequence. For example. John: Hello. Mary: Hi John. How are you?  John: I\'m good. Mary: Me too. Peter: Hi John and Mary. Result: ["male", "female", "male"]. Output only the json array. '
            ),
            HumanMessagePromptTemplate.from_template("{tapescript}"),
        ]
    )
    | model4oMini
    | JsonOutputParser()
)


listeningDSEScriptSystemPrompt = """You are creating tapescripts for listening exercises for students.
You will be given the instructions to generate a listening exercise. You job is to output the listening TAPESCRIPT ONLY.
Please write a script of one to three people speaking, depending to the task content. It is better to have both male and female. 
The speaker should have names. The discussion should only be between three or fewer people (including the host). 
Do not include any action description such as playing music. The script will be used for a listening exercise for students. 
Output with the format of <name> : <dialog>. Such as Peter: Hello! Output in plaintext. Do not put asterisks. Do not bold text.
If the user provides context, such as a passage from the internet, use the information and generate a script about the topic mentioned in the passage.
Even the user prompts for generating an exercise, you should still output a script only."""

listeningDSEScriptHumanPrompt = "Around {length} words. DSE listening comprehension exercise:\n{theme}."
listeningDSEScriptRunnable = (
    ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=listeningDSEScriptSystemPrompt),
            HumanMessagePromptTemplate.from_template(listeningDSEScriptHumanPrompt),
        ]
    )
    | modelDSE
    | StrOutputParser()
)
