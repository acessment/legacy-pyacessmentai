from enum import Enum


class ReadingQuestionType(Enum):
    FITB = "fitB"
    MC = "mcq"
    SQ = "sq"
    TFNG = "tfng"
    MCSQ_MIXED = "mixed mc and sq" #not to be used as intrinsic question type within the JSON