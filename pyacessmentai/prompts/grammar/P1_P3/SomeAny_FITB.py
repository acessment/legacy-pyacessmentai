from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

SomeAny_FITB: BasicPrompts = BasicPrompts(
    title="Some/Any",
    instruction="Please fill in the blanks with either 'some' or 'any'",
    tags=["quantifiers", "some", "any"],
    question_type=QuestionType.FITB,
    exercise_type_id=21,
)
SomeAny_FITB.add_chain(
    system_prompt="""You are an English teacher. You students are english beginners. Please use simple vocabularies. You are drafting a note regarding the difference between "some", "any" . Your job is to create some examples.

Examples:
1. I have ***some*** chocolate in my fridge.
2. Do you have ***any*** tissues?
3. Mary cooked all the food from the fridge. She does not have ***any***food left. 


CONDITIONS:
1. please use triple asterisk to highlight the  "some", "any"


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                            """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
SomeAny_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
