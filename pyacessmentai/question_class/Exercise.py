import hashlib
import json

from pyacessmentai.question_class.CategoryType import Category
from pyacessmentai.question_class.BasicQuestion import BasicQuestion
from pyacessmentai.question_class.FitBQuestion import *
from pyacessmentai.question_class.SQQuestion import SQQuestion
from pyacessmentai.question_class.MCQQuestion import *
from typing import Union


class Exercise:
    def __init__(
        self,
        title: str = "",
        reading: str = "",
        questions: list[Union[BasicQuestion, FitBQuestion]] = None,
        is_correction: bool = False,
        exercise_id: str = None,
        options: list[str] = None,
        category: Category = None,
    ):
        self.title = title
        self.reading = reading
        self.options = options
        self.questions = questions
        self.is_correction = is_correction
        self.exercise_id = exercise_id
        self.category = category

    def add_question(self, question: Union[BasicQuestion, FitBQuestion]):
        self.questions.append(question)

    def insert_question(self, question: Union[BasicQuestion, FitBQuestion], index: int):
        self.questions.insert(index, question)

    def insert_question_before(
        self,
        original_question: Union[BasicQuestion, FitBQuestion],
        new_question: Union[BasicQuestion, FitBQuestion],
    ):
        o_index = self.questions.index(original_question)
        self.questions.insert(o_index, new_question)
        return o_index

    def insert_question_after(
        self,
        original_question: Union[BasicQuestion, FitBQuestion],
        new_question: Union[BasicQuestion, FitBQuestion],
    ):
        o_index = self.questions.index(original_question)
        self.questions.insert(o_index + 1, new_question)
        return o_index

    def get_question_index(self, question: Union[BasicQuestion]) -> int:
        """
        Note that one blank is considered as one question.
        """
        index_count = -1
        for q in self.questions:
            if isinstance(q, FitBQuestion):
                index_count += q.count_blank()
            else:
                index_count += 1
                if question is q:
                    return index_count

    def get_fitBBlank_index(self, blank_obj: FitBBlank, fitB_question: FitBQuestion) -> int:
        index_count = -1
        for question in self.questions:
            if isinstance(question, FitBQuestion):
                if question is fitB_question:
                    index_count += fitB_question.get_only_blank_index(blank_obj) + 1
                    return index_count
                else:
                    index_count += fitB_question.count_blank()
            else:
                index_count += 1
        return -1

    def get_exercise_id(self) -> str:
        exercise_dict = self.__to_dict_no_id()
        json_str = json.dumps(exercise_dict, sort_keys=True)
        json_bytes = json_str.encode("utf-8")
        hash_object = hashlib.sha256(json_bytes)
        hash_hex = hash_object.hexdigest()
        return hash_hex

    def __to_dict_no_id(self) -> dict:
        """
        This is a private method that returns the exercise json without the exercise_id attribute
        """
        exercise_dict = {
            "title": self.title,
            "reading": self.reading,
            "options": self.options,
            "questions": [question.to_dict() for question in self.questions],
            "is_correction": self.is_correction,
            "category": self.category.value if self.category is not None else None,
        }
        return exercise_dict

    def to_dict(self) -> dict:
        exercise_dict = self.__to_dict_no_id()
        exercise_dict["exercise_id"] = self.get_exercise_id()
        return exercise_dict

    @classmethod
    def from_exercise_json(cls, exercise_json: dict):
        try:
            title = exercise_json.get("title", "English Exercise")
            reading = exercise_json.get("reading", "")
            options = exercise_json.get("options", "")
            is_correction = exercise_json.get("is_correction", False)
            exercise_id = exercise_json.get("exercise_id", None)
            category_value = exercise_json.get("category")
            if category_value is not None:
                category = Category(category_value)
            else:
                category = None
            questions_list = exercise_json["questions"]

        except KeyError:
            raise ValueError("Missing required keys in exercise JSON")

        questions = []

        for question_data in questions_list:
            question_type = question_data.get("type")
            if question_type == QuestionType.SQ.value:
                question = SQQuestion.from_question_dict(question_data)
            elif question_type == QuestionType.MCQ.value:
                question = MCQQuestion.from_question_dict(question_data)
            elif question_type == QuestionType.FITB.value:
                question = FitBQuestion.from_question_dict(question_data)
            else:
                raise ValueError(f"Unsupported question type: {question_type}")
            questions.append(question)
        return cls(
            title=title,
            reading=reading,
            options=options,
            questions=questions,
            is_correction=is_correction,
            exercise_id=exercise_id,
            category=category,
        )
