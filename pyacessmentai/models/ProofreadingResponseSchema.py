from pydantic import BaseModel, Field
from typing import List, Dict, Literal, Optional, Union


class PFRPassageResponse(BaseModel):
    text: str = Field(description="The correct passage text")


class PFRoutputList(BaseModel):
    """
    A list of proofreading components in PFR format.
    """

    lines: List[str] = Field("List of lines containing the error and the correct answer")


# class TextPart(BaseModel):
#     type: Literal["text"]
#     text: str = Field("Part of the line text")

#     def to_dict(self):
#         return {'type': self.type, 'text':self.text }


# class WrongPart(BaseModel):
#     type: Literal["wrong"]
#     text: str = Field("Wrong part of the line text")

#     def to_dict(self):
#         return {'type': self.type, 'text':self.text }


# class CorrectAnswer(BaseModel):
#     type: Literal["correct"]
#     text: str = Field("Correct replacement of the wrong part of the line text")

#     def to_dict(self):
#         return {'type': self.type, 'text':self.text }


# # Union type for all possible PFR components
# class PFRLineComponent(BaseModel):
#     parts: List[Union[TextPart, WrongPart, CorrectAnswer]] = Field(
#         description="This explicitly corresponds to one line"
#     )
