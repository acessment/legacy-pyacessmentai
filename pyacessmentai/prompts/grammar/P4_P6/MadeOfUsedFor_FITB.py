from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType


MadeOfUsedFor_FITB: BasicPrompts = BasicPrompts(
    title="Made of... used for...",
    instruction="Please fill in the blanks with either 'made of' or 'used for'.",
    tags=["preposition", "made of", "used for"],
    question_type=QuestionType.FITB,
    exercise_type_id=40,
)
MadeOfUsedFor_FITB.add_chain(
    system_prompt="""
You are an English teacher. All of your students are under the age of twelve. You are drafting a notes regarding the use of the phrases 'made of' and 'used for':

1. made of
2. used for

Please use triple asterisk to highlight where you have used the above phrases. For instance:

1. The table is ***made of*** solid oak.
2. Baking soda is generally ***used for*** cleaning purposes.
...

You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



Output only the examples.
""",
    user_prompt="Give {numOfQ} examples. Remarks: {remarks} Theme for the output:{theme}",
)
MadeOfUsedFor_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
