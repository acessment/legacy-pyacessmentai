from QuestionType import QuestionType
from BasicQuestion import BasicQuestion

class SQQuestion(BasicQuestion):
    type_ = QuestionType.SQ
    def __init__(self, question:str, answer:str, is_example:bool = False, is_correct:bool = None, student_answer: str = None, explanation_text: str = None):
        super().__init__(type=self.type_, is_example=is_example, is_correct=is_correct, student_answer=student_answer, explanation_text= explanation_text)
        self.question = question
        self.answer = answer
    def to_dict(self):
        question_dict = super().to_dict()
        question_dict['question'] = self.question
        question_dict['answer'] = self.answer
        return question_dict
    @classmethod
    def from_question_dict(cls, question_dict: dict) -> "SQQuestion":
        """
        Create SQQuestion instance from the given json.
        """
        return cls(
            is_example=question_dict.get('is_example', False), 
            question=question_dict['question'], 
            answer=question_dict['answer'], 
            is_correct=question_dict.get('is_correct', None), # fields corresponding to marking are default none
            student_answer=question_dict.get('student_answer', None), # fields corresponding to marking are default none
            explanation_text=question_dict.get('explanation_text', None)) # fields corresponding to marking are default none
