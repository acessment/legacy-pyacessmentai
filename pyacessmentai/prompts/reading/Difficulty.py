from enum import Enum
class Difficulty(Enum):
    """
    Difficulty dictates the difficulty of the questions and article
    It also determines the distribution of the questions in default settings, whether KS1,2,3 has fitB and TFNG or not
    """
    P1_P3 = "English Beginners. A1-A2 level. 6 to 9 years old. Simple concept. Simple Vocabulary."
    P4_P6 = "English Beginners. A2-B1 level. 10 to 12 years old. Simple concept. Simple Vocabulary."
    S1_S3 = "Intermediate english learner. B1-B2 level. 15 to 17 years old"
    S4_S6 = "Advanced english learner. C1 level. Adults"