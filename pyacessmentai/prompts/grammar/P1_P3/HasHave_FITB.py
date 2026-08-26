from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

HasHave_FITB: BasicPrompts = BasicPrompts(
    title="Has, Have",
    instruction="Please fill in the blanks with either 'has' or 'have'",
    tags=["simple present tense", "has/have"],
    question_type=QuestionType.FITB,
    exercise_type_id=22,
)
HasHave_FITB.add_chain(
    system_prompt="""You are an English teacher. You are drafting a notes regarding the difference between has and have. 

please use triple asterisk to highlight where you have used the 'has' or 'have':
1. Do you ***have*** an umbrella?
2. She ***has*** a cat in house.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
HasHave_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
