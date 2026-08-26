from enum import Enum
from QuestionType import QuestionType

class TextBlankType(Enum):
    TEXT = 'text'
    BLANK = 'blank'
    EXPLANATION = 'explanation'

class FitBTextBlank():
    """
    The parent class for FitBText, FitBBlank and FitBExplanation
    """
    def __init__(self, type: TextBlankType, text: str):
        self.type = type
        self.text = text
    def to_dict(self):
        return {'type': self.type.value, 'text':self.text }
        
class FitBText(FitBTextBlank):
    """
    This class represents the part with raw text inside a FitBQuestion.
    """
    type_ = TextBlankType.TEXT
    def __init__(self, text: str):
        super().__init__(self.type_, text)
        
        
class FitBBlank(FitBTextBlank):
    """
    This class represents a blank.
    """
    type_ = TextBlankType.BLANK
    def __init__(self, text: str, is_example: bool = False, is_correct: bool = None, student_answer: str = None):
        super().__init__(self.type_, text)
        self.text = text
        self.is_example = is_example
        self.is_correct = is_correct
        self.student_answer = student_answer
        
    def to_dict(self):
        question_dict = super().to_dict()
        question_dict['is_example'] = self.is_example
        question_dict['is_correct'] = self.is_correct
        return question_dict
        
class FitBExplanation(FitBTextBlank):
    """
    This part represents the explanation.
    """
    type_ = TextBlankType.EXPLANATION
    def __init__(self, student_answer:str, correct_answer:str, explanation_text: str):
        super().__init__(self.type_, explanation_text)
        self.student_answer = student_answer
        self.correct_answer = correct_answer
    def to_dict(self):
        question_dict = {'type': self.type_.value, 'correct_answer': self.correct_answer, 'student_answer': self.student_answer, 'explanation_text': self.text}
        return question_dict
    
class FitBQuestion():
    type_ = QuestionType.FITB
    def __init__(self, question:list[FitBTextBlank]):
        self.question = question
        self.type = self.type_
    
    def fitB_factory(single_fitB_question: dict) -> FitBTextBlank:
        """
        This function helps to create the corresponding instance based on the given json.
        
        Args:
            single_fitB_question (dict): the question field inside each fitB question, check the below json for more information:
            {
                "type": "fitB",
                "question": [ <----- This is the question field
                    { <----- This is the single_fitB_question
                        "type": "text",
                        "text": "3. They suggested"
                    },
                    {
                        "type": "blank",
                        "text": "playing",
                        "is_correct": True
                    },
                    ...
                ],
            }
        """
        fitB_class_map = {
            TextBlankType.TEXT.value: FitBText,
            TextBlankType.BLANK.value: FitBBlank,
            TextBlankType.EXPLANATION.value: FitBExplanation,
        }
        text_blank_type = single_fitB_question.pop('type',None)
        if text_blank_type in fitB_class_map:
            return fitB_class_map[text_blank_type](**single_fitB_question)

    def fitB_factory_multiple(fitBQuestion: list[dict]) -> list[FitBTextBlank]:
        """
        Create all corresponding instances for all the items in the question field inside a fitB question
        """
        fitB_questions_instances = []
        for text_blank_obj in fitBQuestion:
            fitB_questions_instances.append(FitBQuestion.fitB_factory(text_blank_obj))
        return fitB_questions_instances
    
    @classmethod
    def from_question_dict(cls, question_dict: dict):
        question = FitBQuestion.fitB_factory_multiple(question_dict['question'])
        return cls(question)
    
    def to_dict(self):
        return {
            'type': self.type.value,
            'question': [text_blank.to_dict() for text_blank in self.question]
        }
        
    def get_blanks_as_list(self):
        """
        Getting all blanks in the question as list.
        """
        return [text_blank for text_blank in self.question if isinstance(text_blank, FitBBlank)]
    
    def get_blank_from_blank_index(self, blank_index: int) -> FitBBlank:
        """
        Returns the FitBBlank object according to the given blank index.

        Args:
            blank_index (int): index 0 refers to the first blank, index 1 refers to the second blank...
        """
        return self.get_blanks_as_list()[blank_index]
    
    def get_fitB_segment(self, target_blank_obj: FitBBlank, depth:int) -> list[FitBTextBlank]:
        """
        Returns a list of FitBBlank or FitBText Object based on the given blank index and depth.
        
        Args:
            depth (int): depth 0 means retrieving only the texts around the given target_blank_obj, 1 means retrieving the text around the neighbor blanks (1 step away from the given blank_obj), 2 means 2 steps away... etc.
        """
        blanks_list = self.get_blanks_as_list()
        blank_indices = [i for i, item in enumerate(self.question) if isinstance(item, FitBBlank)]
        target_blank_idx = blanks_list.index(target_blank_obj)
        start_blank = max(0, target_blank_idx - depth)
        end_blank = min(len(blank_indices) - 1, target_blank_idx + depth)
        
        start_pos = blank_indices[start_blank - 1] + 1 if start_blank > 0 else 0
        end_pos = blank_indices[end_blank + 1] if end_blank + 1 < len(blank_indices) else len(self.question)
        
        return self.question[start_pos:end_pos]
    
    def get_only_blank_index(self, blank_obj: FitBBlank) -> int:
        """
        This function returns only the blank index based on the total number of blanks. This index does not refer to the actual index within the fitB question array.
        """
        blank_count = 0
        for text_blank in self.question:
            if isinstance(text_blank, FitBBlank):
                blank_count += 1
            if blank_obj is text_blank:
                return blank_count
        return -1
    
    def add_text_blank(self, text_blank: FitBTextBlank):
        self.question.append(text_blank)
    
    def insert_text_blank(self, text_blank_obj: FitBTextBlank, index: int):
        self.question.insert(index, text_blank_obj)
    
    def insert_text_blank_before(self, original_text_blank: FitBTextBlank, new_text_blank: FitBTextBlank):
        """
        Insert a new text/blank before the original_text_blank
        """
        o_index = self.question.index(original_text_blank)
        self.question.insert(o_index, new_text_blank)
        return o_index
    
    def insert_text_blank_after(self, original_text_blank: FitBTextBlank, new_text_blank: FitBTextBlank):
        """
        Insert a new text/blank after the original_text_blank
        """
        o_index = self.question.index(original_text_blank)
        self.question.insert(o_index + 1, new_text_blank)
        return o_index + 1
    
    def count_blank(self):
        """
        Counts the number of blanks
        """
        count = 0
        for text_blank in self.question:
            if isinstance(text_blank, FitBBlank):
                count += 1
        return count