from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

ThereIsAre_FITB: BasicPrompts = BasicPrompts(
    title="There is... There are...",
    instruction="Please fill in the blanks with either 'there is' or 'there are'",
    tags=["there", "be", "is/am/are"],
    question_type=QuestionType.FITB,
    exercise_type_id=21,
)
ThereIsAre_FITB.add_chain(
    system_prompt="""You are an English teacher. You are drafting a notes regarding the difference between "there is" and "there are". Your job is to create some examples. 

please use triple asterisk to highlight where you have used the 'there is', and 'there are'

Examples:

1. ***There are*** five cars in the car park.
2. ***There is*** an apple on the table


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                            """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
ThereIsAre_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
