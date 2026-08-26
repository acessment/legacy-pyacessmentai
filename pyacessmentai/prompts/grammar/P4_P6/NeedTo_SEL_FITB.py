from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

NeedTo_SEL_FITB: BasicPrompts = BasicPrompts(
    title="Need to...",
    instruction="Please fill in the blanks using 'need to....' with the appropriate verb inside the box. You may need to change the verb form accordingly.",
    tags=["simple present tense", "to-infinitive", "need to..."],
    question_type=QuestionType.SEL_FITB,
    exercise_type_id=8,
)
NeedTo_SEL_FITB.add_chain(
    system_prompt="""You are an English teacher. All of your students are under the age of twelve. You are drafting a notes regarding the use of "need to". The format should be as follows:

Examples: 
I ***need to finish*** my homework today.
He ***needs to do*** shopping before 6pm.
They ***need to be*** careful when they walk in the woods.

Options:
finish,do,be

CONDITIONS:
1. use triple asterisk to highlight the "need to" and the verb following afterwards
2. the output consists of two parts, examples and options.
3. Please include all the verbs under options.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



Output only the examples and options.
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
NeedTo_SEL_FITB.add_json_chain(JSONPrompt.SEL_FITB)
