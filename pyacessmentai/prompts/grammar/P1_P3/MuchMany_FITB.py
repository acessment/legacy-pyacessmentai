from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

MuchMany_FITB: BasicPrompts = BasicPrompts(
    title="Much, Many",
    instruction="Please fill in the blanks with either 'much' or 'many'.",
    tags=["countable/uncountable", "much/many"],
    question_type=QuestionType.FITB,
    exercise_type_id=21,
)
MuchMany_FITB.add_chain(
    system_prompt="""You are an English teacher. You are drafting a notes regarding the difference between much and many. Your job is to create some examples for 'much' and some for 'many'


please use triple asterisk to highlight where you have used the 'much' or 'many':
1. I don't have ***much*** water left.
2. There are ***many*** apples on the table



You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
MuchMany_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
