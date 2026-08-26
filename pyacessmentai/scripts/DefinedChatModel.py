from enum import Enum
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, AzureChatOpenAI

load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
AZURE_API_KEY = os.environ.get("AZURE_API_KEY")


class DefinedChatModel(Enum):
    GPT3_5 = ChatOpenAI(model="gpt-3.5-turbo-0125", api_key=OPENAI_API_KEY)
    GPT4o = AzureChatOpenAI(
        azure_endpoint="https://ACEssmentSponsoredAI1.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview",
        azure_deployment="gpt-4o",
        api_version="2024-08-01-preview",
        api_key=AZURE_API_KEY,
    )
    GPT4oMini = AzureChatOpenAI(
        azure_endpoint="https://ACEssmentSponsoredAI1.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-08-01-preview",
        azure_deployment="gpt-4o-mini",
        api_version="2024-08-01-preview",
        api_key=AZURE_API_KEY,
    )
    GPT4oT08 = AzureChatOpenAI(
        azure_endpoint="https://ACEssmentSponsoredAI1.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview",
        azure_deployment="gpt-4o",
        api_version="2024-08-01-preview",
        api_key=AZURE_API_KEY,
        temperature=0.8
    )
    FineTunedV4_S258 = ChatOpenAI(model="ft:gpt-3.5-turbo-0125:acessment:mixed-tenses-4:9nYhXDoG:ckpt-step-258", api_key=OPENAI_API_KEY)
    FineTunedV4_S301 = ChatOpenAI(model="ft:gpt-3.5-turbo-0125:acessment:mixed-tenses-4:9nYhXTER:ckpt-step-301", api_key=OPENAI_API_KEY)
