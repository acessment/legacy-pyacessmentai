from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

Connectives_BothAnd_SQ: BasicPrompts = BasicPrompts(
    title="Connectives: Both...and...",
    instruction="Please rewrite the sentences with the sentence structure 'both...and...'",
    tags=["connectives", "both...and...", "both", "and"],
    question_type=QuestionType.SQ,
    exercise_type_id=28,
)
Connectives_BothAnd_SQ.add_chain(
    system_prompt="""You are an English Teacher. You are creating grammar notes for english beginners. 
You teach students how to use "both ... and ..." to form sentences by creating sample sentences.

You are going to create some examples to demonstrate the application of the above connectives.
The examples will include:
first: A sentence that use connectives to join both sentences
second: Separated sentences that doesn't use any connectives

Use triple asterisk to highlight the first sentence.

Examples:
1. ***Both Jerry and Tom like eating ice cream.***
Jerry likes eating ice cream. Tom likes eating ice cream.

2. ***I am good at both swimming and dancing***
I am good at swimming. I am good at dancing.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
Connectives_BothAnd_SQ.add_json_chain(JSONPrompt.SQ)
