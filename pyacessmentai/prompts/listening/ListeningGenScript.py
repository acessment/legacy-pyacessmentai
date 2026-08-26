from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
model4o = AzureChatOpenAI(
    azure_endpoint="https://ACEssmentSponsoredAI1.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview",
    azure_deployment="gpt-4o",
    api_version="2024-08-01-preview",
    api_key=AZURE_API_KEY,
    temperature=0.3,
)

listeningCopyCatNonsenseSystemPrompt = """You'll receive a tape script. Your job is to create a new tape script similar to the given one. But don't be too similar. It should have similar length, similar pace, similar organization. But it should also have different wordings, different sentence structure, and different content. Make the sentences sound like conversation between dramatic and flirty people. Paraphrase every word in a playful tone. Rewrite every sentence in a flirty way. Output in plain text."""
listeningCopyCatNonsenseHumanPrompt = """{tapescript}

The new script should be more nonsense. It is a script in a magical world of little pigs fighting and a big bad wolf. Add new nonsense storylines in the middle if you want. Replace nouns with magical objects. Replace verbs with magical actions. Make every sentence longer to waste people's time. Rewrite dialogs to sound unnatural like drunk Teletubbies."""

listeningCopyCatNonsensePrompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=listeningCopyCatNonsenseSystemPrompt),
        HumanMessagePromptTemplate.from_template(listeningCopyCatNonsenseHumanPrompt),
    ]
)

listeningCopyCatNonsenseRunnable = listeningCopyCatNonsensePrompt | model4o | StrOutputParser()


listeningCopyCatGenScriptSystemPrompt = """You'll receive a total nonsense and flirty tape script. Your job is to create a new tape script similar to the given one. But don't be too similar. It should have similar length, similar pace, similar organization. But it should also have different wordings, different sentence structure, and different content. Make the sentences sound like normal conversation between normal people. Paraphrase every word in a less playful tone. Rewrite every sentence in a less flirty way."""

listeningCopyCatGenScriptHumanPrompt = """{tapescript}

The new script should be like a normal conversation between normal people. It is a script about {theme}. Keep it lengthy and detailed. Use alternative sentence structures to make the conversation more natural. Output in plain text."""

listeningCopyCatGenScriptPrompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=listeningCopyCatGenScriptSystemPrompt),
        HumanMessagePromptTemplate.from_template(listeningCopyCatGenScriptHumanPrompt),
    ]
)

listeningCopyCatGenScriptRunnable = listeningCopyCatGenScriptPrompt | model4o | StrOutputParser()
