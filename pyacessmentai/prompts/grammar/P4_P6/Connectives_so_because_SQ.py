from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

Connectives_so_because_SQ: BasicPrompts = BasicPrompts(
    title="Connectives: so, because",
    instruction="Please rewrite the sentences using the appropriate connectives: (so, because)",
    tags=["connectives", "so", "because"],
    question_type=QuestionType.SQ,
    exercise_type_id=28,
)
Connectives_so_because_SQ.add_chain(
    system_prompt="""You are an English Teacher. You are teaching beginners about the following connectives:

1. so (Used to show the result or consequence of an action.)
2. because (Used to show the reason behind an action.)


You are going to create some examples to demonstrate the application of the above connectives.
The examples will include:
first: A sentence that use connectives to join both sentences
second: Separated sentences that doesn't use any connectives

Use triple asterisk to highlight the first sentence.

Example:

1. ***Mary likes red so she chose a red bag.***
Mary likes red. She chose a red bag.


2. ***Peter is absent today because he is sick***
Peter is absent today. He is sick



You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
Connectives_so_because_SQ.add_json_chain(JSONPrompt.SQ)
