from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

Should_SEL_FITB: BasicPrompts = BasicPrompts(
    title="Modal verb: Should",
    instruction="Please fill in the blanks using the modal verb 'should' and select the appropriate verb in the box below. You may also need to add negation:'should not' when necessary.",
    tags=["modal verb", "should"],
    question_type=QuestionType.SEL_FITB,
    exercise_type_id=46,
)
Should_SEL_FITB.add_chain(
    system_prompt="""You are an English Teacher. You are going to create some grammar examples for english beginners. All the vocabulary use should be for english beginners.


You are going to teach the students about the modal verb "should". You are going to create sample sentences and sample questions to demonstrate how to use 'should'

Examples
***Should*** we ***cook*** some food for ourselves?
You ***should follow*** the rules.
He ***should not throw*** the rubbish on the ground.

Options:cook,follow,throw

CONDITIONS:
1. use triple asterisk to highlight the modal verb should and the corresponding verb following.
2. add all the verb you have used in options

Output only the sample and options.

You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.

                             """,
    user_prompt="Give {numOfQ} samples. Remarks: {remarks}. Theme: {theme}",
)
Should_SEL_FITB.add_json_chain(JSONPrompt.SEL_FITB)
