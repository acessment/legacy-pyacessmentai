from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

Connectives_But_SQ: BasicPrompts = BasicPrompts(
    title="Connectives: but",
    instruction="Please rewrite the sentences using the appropriate connectives: (but)",
    tags=["connectives", "but"],
    question_type=QuestionType.SQ,
    exercise_type_id=28,
)
Connectives_But_SQ.add_chain(
    system_prompt="""You are an English teacher. Your students are all english beginners. You are drafting some sample sentences to illustrate the use of "but"

You are going to create some examples to demonstrate the application of the above connectives.
The examples will include:
first: A sentence that use connectives to join both sentences
second: Separated sentences that doesn't use any connectives

Use triple asterisk to highlight the first sentence.

Examples:
1. ***I like swimming but I don't like running***
I like swimming. I don't like running.

2. ***She was late to school but the teacher did not punish her.***
She was late to school. The teacher did not punish her.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
Connectives_But_SQ.add_json_chain(JSONPrompt.SQ)
