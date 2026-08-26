from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

WhenWhile_FITB: BasicPrompts = BasicPrompts(
    title="When, While",
    instruction="Please fill in the blanks with either 'when' or 'while'",
    tags=["when", "while", "past continuous tense"],
    question_type=QuestionType.FITB,
    exercise_type_id=17,
)
WhenWhile_FITB.add_chain(
    system_prompt="""You are an English teacher. All of your students are under the age of twelve. You are drafting a notes regarding the difference between 'when' and 'while'. The format should be as follows:

Examples:
1. ***When*** is your birthday?
2. I went to the church ***when*** I was young.
3. ***While*** I was cooking dinner, my phone rang.

CONDITIONS:
1. please use triple asterisk to highlight the "when" and "while".



You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.

Output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
WhenWhile_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)

exercise_chain = WhenWhile_FITB.build_chain()
