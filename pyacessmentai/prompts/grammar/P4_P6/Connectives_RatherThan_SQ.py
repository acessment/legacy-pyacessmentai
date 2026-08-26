from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

Connectives_RatherThan_SQ: BasicPrompts = BasicPrompts(
    title="Connectives: rather than",
    instruction="Please rewrite the sentences using the appropriate connectives: (rather than)",
    tags=["connectives", "rather than"],
    question_type=QuestionType.SQ,
    exercise_type_id=28,
)
Connectives_RatherThan_SQ.add_chain(
    system_prompt="""You are an English teacher. Your students are all english beginners. You are drafting some sample sentences to illustrate the use of "rather.... than...."

You are going to create some examples to demonstrate the application of the above connectives.
The examples will include:
first: A sentence that use connectives to join both sentences
second: Separated sentences that doesn't use any connectives

Use triple asterisk to highlight the first sentence.

Examples:
1. ***I would rather go swimming than running.***
I would go swimming. I would not go running.

2. ***She prefers to read a book rather than watch TV.***
She prefers to read a book. She prefers not to watch TV.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
Connectives_RatherThan_SQ.add_json_chain(JSONPrompt.SQ)
