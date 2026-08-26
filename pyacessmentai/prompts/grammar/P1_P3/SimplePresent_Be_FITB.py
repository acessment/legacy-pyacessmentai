from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

SimplePresent_Be_FITB: BasicPrompts = BasicPrompts(
    title="Simple Present Tense: Be",
    instruction="Please fill in the blanks with the correct form of 'be': 'is', 'am' or 'are'",
    tags=["simple present tense", "be", "is/am/are"],
    question_type=QuestionType.FITB,
    exercise_type_id=21,
)
SimplePresent_Be_FITB.add_chain(
    system_prompt="""You are an English teacher. You are drafting a notes regarding the difference between is, am and are. Your job is to create certain examples.

please use triple asterisk to highlight where you have used the 'is', 'am' and 'are'
1. My grandpa ***is*** in the hospital now.
2. There ***are*** 5 apples on the table.
3. I ***am*** sick today.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                            """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
SimplePresent_Be_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
