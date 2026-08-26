from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

Can_SEL_FITB: BasicPrompts = BasicPrompts(
    title="Modal verb: can",
    instruction="Please fill in the blanks using the modal verb 'can' and select the appropriate verb in the box below. You may also need to add negation:'cannot' when necessary.",
    tags=["modal verb", "can"],
    question_type=QuestionType.SEL_FITB,
    exercise_type_id=46,
)
Can_SEL_FITB.add_chain(
    system_prompt="""You are an English teacher. You are drafting a notes regarding the use of "can". Your job is to create some examples.


Examples:
***Can*** you ***run*** 100m in 12 seconds?
My legs are hurt and I ***cannot walk*** fast.
We ***can work*** on this project together.



Options:
run,walk,work


CONDITIONS:
1. please use triple asterisk to highlight the "can" and the corresponding "verb". 
2. At the last part of the output, you should include verb you have used.
3. Output only the example and options
4. When you use negation, you must explain the reason within the sentence as well.



You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples and options.

                             """,
    user_prompt="Give {numOfQ} examples with different verb choices. Remarks: {remarks}. Theme: {theme}",
)
Can_SEL_FITB.add_json_chain(JSONPrompt.SEL_FITB)
