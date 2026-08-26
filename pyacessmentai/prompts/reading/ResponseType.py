from pydantic import BaseModel
from enum import Enum
from typing import Optional, Literal, Union


class MCSQQuestion(BaseModel):
    question: str
    type: str


class MCQQuestion(MCSQQuestion):
    type: Literal["mcq"] = "mcq"  # Type is fixed to "mcq"

    class MCQOption(BaseModel):
        A: str
        B: str
        C: str
        D: str

    answer: Literal["A", "B", "C", "D"]  # Restrict answer to A, B, C, or D
    options: MCQOption  # Options must be provided


class SQQuestion(MCSQQuestion):
    type: Literal["sq"] = "sq"  # Type is fixed to "sq"
    answer: str  # Answer can be any string
    options: None = None  # No options for SQ


class MCSQResponse(BaseModel):
    questions: list[Union[MCQQuestion, SQQuestion]]  # questions can be either MCQ or SQ


class ArticleResponse(BaseModel):
    title: str
    content: str


class ParagraphJSONResponse(BaseModel):
    paragraphs: list[str]


class TFNGResponse(BaseModel):
    class __TFNGStatement(BaseModel):
        class __TFNGOption(str, Enum):
            TRUE = "T"
            FALSE = "F"
            NOT_GIVEN = "NG"

        statement: str
        answer: __TFNGOption

    statements: list[__TFNGStatement]
