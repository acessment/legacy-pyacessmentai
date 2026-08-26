from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

SuchAs_SQ: BasicPrompts = BasicPrompts(
    title="Such as...",
    instruction="Please rewrite the sentences using 'such as...''",
    tags=["such as"],
    question_type=QuestionType.SQ,
    exercise_type_id=28,
)
SuchAs_SQ.add_chain(
    system_prompt="""You are an English teacher. All of your students are under the age of twelve. You are drafting a notes regarding the use of "such as". The format should be as follows:

You are going to create some examples to demonstrate the application of the above connectives.
The examples will include:
first: A sentence that use connectives to join both sentences
second: Separated sentences that doesn't use any connectives

Use triple asterisk to highlight the first sentence.

Examples: 
1. ***I like doing sports such as running and swimming***.
I like doing sports (running, swimming) 

2. ***He likes reading books such as Harry Potter, The Little Prince and Maze Runner.***
He likes reading books (Harry Potter, The Little Prince, Maze Runner).


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



Output only the examples and options.
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
SuchAs_SQ.add_json_chain(JSONPrompt.SQ)
