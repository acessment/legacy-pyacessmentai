from .QuestionType import QuestionType
class BasicQuestion():
    def __init__(self, type:QuestionType, is_example:bool, is_correct:bool = None, explanation_text:str = None, student_answer: str = None):
        self.type = type
        self.is_example = is_example
        self.is_correct = is_correct
        self.explanation_text = explanation_text
        self.student_answer = student_answer
    def to_dict(self):
        question_dict = {
            'type': self.type.value,
            'is_example': self.is_example,
            'is_correct': self.is_correct,
            'explanation_text': self.explanation_text,
            'student_answer': self.student_answer,
        }
        return question_dict