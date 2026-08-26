from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

Shall_SEL_FITB: BasicPrompts = BasicPrompts(
    title="Shall",
    instruction="Please fill in the blanks using 'shall' and select the appropriate verb in the box below.",
    tags=["modal verb", "shall"],
    question_type=QuestionType.SEL_FITB,
    exercise_type_id=46,
)
Shall_SEL_FITB.add_chain(
    system_prompt="""You are an English teacher. All of your students are under the age of twelve. You are drafting a notes regarding the use of "shall". The format should be as follows:

Examples: 
John is sick. ***Shall he go*** to see the doctor? (John)
A group of students are lost. ***Shall they look*** for help? (a group of students)

Options:
go,look

CONDITIONS:
1. use triple asterisk to highlight the modal verb and the verb following afterwards
2. the output consists of two parts, examples and options.
3. Please include all the verbs under options.
4. Please include the subject within the bracket at the end of each examples.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



Output only the examples and options.

                             """,
    user_prompt="Give {numOfQ} samples. Remarks: {remarks}. Theme: {theme}",
)
Shall_SEL_FITB.add_json_chain(JSONPrompt.SEL_FITB)
