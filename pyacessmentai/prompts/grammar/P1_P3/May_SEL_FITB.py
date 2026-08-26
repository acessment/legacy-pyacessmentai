from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

May_SEL_FITB: BasicPrompts = BasicPrompts(
    title="Modal verb: may",
    instruction="Please fill in the blanks using the modal verb 'may' and select the appropriate verb in the box below. Please add negation 'may not' when necessary.",
    tags=["modal verb", "may"],
    question_type=QuestionType.SEL_FITB,
    exercise_type_id=46,
)
May_SEL_FITB.add_chain(
    system_prompt="""You are an English teacher. All of your students are under the age of twelve. You are teaching the students regarding the use of "may". Your job is to draft some examples.

Examples:
1. You ***may pack*** your belongings and leave.
2. Peter ***may come*** by eleven if he wishes.
3. ***May*** I ***leave*** now?
4. You ***may not start*** before 11am.


Options:
pack,come,leave,start

CONDITIONS:
1. please use triple asterisk to enclose the 'may' and the corresponding "verb" 
2. You should include verb you have used under options.
3. Output only the example and options


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.

Output only the examples and options.

                             """,
    user_prompt="Give {numOfQ} samples with different choice of verbs. Remarks: {remarks}. Theme: {theme}",
)
May_SEL_FITB.add_json_chain(JSONPrompt.SEL_FITB)
