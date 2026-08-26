from langchain_openai import AzureChatOpenAI
from langchain_perplexity import ChatPerplexity
from enum import Enum
from dotenv import load_dotenv


import os

load_dotenv()
AZURE_API_KEY = os.environ.get("AZURE_API_KEY")
PPLX_API_KEY = os.environ.get("PPLX_API_KEY")


class LLMModelType(Enum):
    Offline_GPT4o = AzureChatOpenAI(
        azure_endpoint="https://ACEssmentSponsoredAI1.openai.azure.com/",
        azure_deployment="gpt-4o",
        api_version="2024-08-01-preview",
        api_key=AZURE_API_KEY,
    )
    Offline_GPT4oMini = AzureChatOpenAI(
        azure_endpoint="https://ACEssmentSponsoredAI1.openai.azure.com/",
        azure_deployment="gpt-4o-mini",
        api_version="2024-08-01-preview",
        api_key=AZURE_API_KEY,
    )
    Online_llma_3_1 = ChatPerplexity(model="sonar", api_key=PPLX_API_KEY)
