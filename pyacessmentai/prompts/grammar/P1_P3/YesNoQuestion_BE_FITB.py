from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

YesNoQuestion_BE_FITB: BasicPrompts = BasicPrompts(
    title="Yes,No Question: Be",
    instruction="Please fill in the blanks with the correct form of 'be': 'is', 'am' or 'are'",
    tags=["simple present tense", "be", "is/am/are"],
    question_type=QuestionType.FITB,
    exercise_type_id=21,
)
YesNoQuestion_BE_FITB.add_chain(
    system_prompt="""You are an English teacher. You are drafting a notes regarding the difference between is, am and are. Your job is to create certain examples of questions.


1. ***Is*** this your uncle's bag?
2. ***Are*** you happy today?
3. ***Am*** I full?


please use triple asterisk to highlight where you have used the 'is', 'am' and 'are'


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                            """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
YesNoQuestion_BE_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
