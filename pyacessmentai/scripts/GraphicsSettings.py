from enum import Enum
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage


class GraphicsSettings(Enum):
    NO_GRAPHICS = "no graphic settings"
    SINGLE = "single"
    ONE_BY_ONE = "one by one"
