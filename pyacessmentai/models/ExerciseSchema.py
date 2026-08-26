from typing import List, Optional, Union, Literal
from pydantic import BaseModel, Field, RootModel


class QuestionPart(BaseModel):
    type: Literal["example_blank", "blank", "text", "image"]
    text: Optional[str] = None
    image: Optional[Union[str, None]] = None


class Options(BaseModel):
    a: Optional[str] = None
    b: Optional[str] = None
    c: Optional[str] = None
    d: Optional[str] = None
    e: Optional[str] = None
    t: Optional[str] = None
    f: Optional[str] = None
    ng: Optional[str] = None


class SQuestion(BaseModel):
    answer: str
    question: str
    type: Literal["sq"]


class MCQuestion(BaseModel):
    answer: Literal["a", "b", "c", "d", "e", "t", "f", "ng"]
    question: str
    type: Literal["mcq"]
    options: Options


class MSQuestion(BaseModel):
    answer: List[Literal["a", "b", "c", "d", "e"]]
    question: str
    type: Literal["msq"]
    options: Options


class FitBQuestion(BaseModel):
    question: List[QuestionPart]
    type: Literal["fitB"]


class ExerciseItem(BaseModel):
    instruction: str
    options: Optional[List[str]] = None
    reading: Optional[str] = None
    questions: Union[
        List[SQuestion], List[MCQuestion], List[MSQuestion], List[FitBQuestion]
    ]


class ExerciseResponse(BaseModel):
    response: List[ExerciseItem]
