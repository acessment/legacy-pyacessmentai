from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

Must_SEL_FITB: BasicPrompts = BasicPrompts(
    title="Modal verb: must",
    instruction="Please fill in the blanks using the modal verb 'must' and select the appropriate verb in the box below. You may also need to add negation:'must not' when necessary.",
    tags=["modal verb", "must"],
    question_type=QuestionType.SEL_FITB,
    exercise_type_id=46,
)
Must_SEL_FITB.add_chain(
    system_prompt="""You are an English teacher. All of your students are under the age of twelve. You are drafting a notes regarding the use of "must". The format should be as follows:

Examples:
You ***must*** now ***pack*** your belongings and leave.
Peter ***must come*** by eleven.
They ***must not be*** late to the exam.


Options:
borrow,pack,be

CONDITIONS:
1. please use triple asterisk to highlight the 'must' and the verb following afterwards 
2. At the last part of the output, you should include verb you have used.
3. Output only the example and options


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



Output only the examples and options.

                             """,
    user_prompt="Give {numOfQ} samples with different choice of verbs. Remarks: {remarks}. Theme: {theme}",
)
Must_SEL_FITB.add_json_chain(JSONPrompt.SEL_FITB)
