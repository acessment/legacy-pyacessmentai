from enum import Enum
class TensesType(Enum):
    SIMPLE_PRESENT = "simple present tense"
    SIMPLE_PRESENT_TENSE_Q = "simple present tense q"
    SIMPLE_PAST = "simple past tense"
    SIMPLE_PAST_Q = "simple past tense q"
    SIMPLE_FUTURE = "simple future tense"
    PRESENT_PERFECT = "present perfect tense"
    PAST_CONTINUOUS = "past continuous tense"
    PRESENT_CONTINUOUS = "present continuous tense"
    PAST_PERFECT = "past perfect tense"
    PRESENT_PERFECT_CONTINUOUS = "present perfect continuous tense"
    FUTURE_CONTINUOUS_TENSE = "future continuous tense"
    PAST_PERFECT_CONTINUOUS = "past perfect continuous tense"
    MODAL_VERB = "modal verb"
    ANY_TENSES = "any tenses"
    def get_tenses_dict():
        return {
            1:TensesType.SIMPLE_PRESENT, 
            2:TensesType.SIMPLE_PAST,
            3:TensesType.SIMPLE_FUTURE,
            4:TensesType.PRESENT_PERFECT,
            5:TensesType.PAST_CONTINUOUS,
            6:TensesType.PRESENT_CONTINUOUS,
            7:TensesType.PAST_PERFECT,
            8:TensesType.PRESENT_PERFECT_CONTINUOUS,
            9:TensesType.FUTURE_CONTINUOUS_TENSE,
            10:TensesType.PAST_PERFECT_CONTINUOUS,
            }