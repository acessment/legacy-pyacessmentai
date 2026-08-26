from enum import Enum
class QuestionType(Enum):
    SQ = "sq"
    ARTICLE_FITB = "art_fitB"
    FITB = "fitB"
    MCQ = "mcq"
    SEL_FITB = "sel_fitB"
    PFR = 'pfr'

    @property
    def json_type(self):
        # Return 'fitB' for all xxFITB types
        if self in {QuestionType.ARTICLE_FITB, QuestionType.FITB, QuestionType.SEL_FITB}:
            return 'fitB'
        return self.value  # For other types, return their original value
    
    def to_full_string(self):
        if self == QuestionType.SQ:
            return 'short question'
        elif self in {QuestionType.ARTICLE_FITB, QuestionType.FITB, QuestionType.SEL_FITB}:
            return 'fill in the blanks'
        elif self == QuestionType.MCQ:
            return 'multiple choice question'
        elif self == QuestionType.PFR:
            return 'proofreading question'