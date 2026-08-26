from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType


ThankyouSorryFor_FITB: BasicPrompts = BasicPrompts(
    title="Preposition: Thank you for.... Sorry for...",
    instruction="Please fill in the blanks with the correct expressions: 'thank you for...' or 'sorry for...'",
    tags=["preposition", "for"],
    question_type=QuestionType.FITB,
    exercise_type_id=40,
)
ThankyouSorryFor_FITB.add_chain(
    system_prompt="""

You are an English teacher. All of your students are under the age of twelve. You are drafting a notes regarding the use of 'thank you for' and 'sorry for'.

1. thank you for
2. sorry for

Please use triple asterisk to highlight where you have used the above phrases

For instance:
***Thank you for*** helping me with my homework.
***Sorry for*** being late to the meeting.
...


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



Output only the examples.
""",
    user_prompt="Give {numOfQ} examples. Remarks: {remarks} Theme for the output:{theme}",
)
ThankyouSorryFor_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
