from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

OughtTo_SEL_FITB: BasicPrompts = BasicPrompts(
    title="Ought to",
    instruction="Please fill in the blanks using 'ought to' and select the appropriate verb in the box below.",
    tags=["modal verb", "ought to"],
    question_type=QuestionType.SEL_FITB,
    exercise_type_id=46,
)
OughtTo_SEL_FITB.add_chain(
    system_prompt="""You are an English Teacher. You are going to create some grammar examples for english beginners. All the vocabulary use should be for english beginners.


You are going to teach the students about the modal verb "ought to". You are going to create sample sentences and sample questions to demonstrate how to use 'ought to'

Examples
He ***ought to keep*** quiet in the library?
You ***ought to follow*** the rules.

Options:keep,follow

CONDITIONS:
1. use triple asterisk to highlight the 'ought to' and the corresponding verb following.
2. add all the verb you have used in options

Output only the sample and options.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.

                             """,
    user_prompt="Give {numOfQ} samples. Remarks: {remarks}. Theme: {theme}",
)
OughtTo_SEL_FITB.add_json_chain(JSONPrompt.SEL_FITB)
