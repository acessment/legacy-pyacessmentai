from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

Connectives_because_sothat_SQ: BasicPrompts = BasicPrompts(
    title="Connectives: because, so that",
    instruction="Please rewrite the sentences using the appropriate connectives: (because, so that)",
    tags=["connectives", "because", "so that"],
    question_type=QuestionType.SQ,
    exercise_type_id=28,
)
Connectives_because_sothat_SQ.add_chain(
    system_prompt="""You are an English Teacher. You are teaching beginners about the following connectives:

1. because (Used to show the reason.)
2. so that (Used to show the purpose of an action.)


You are going to create some examples to demonstrate the application of the above connectives.
The examples will include:
first: A sentence that use connectives to join both sentences
second: Separated sentences that doesn't use any connectives

Use triple asterisk to highlight the first sentence.

Example:

1. ***She chose a red bag because she likes red.***
She chose a red bag. She likes red.


2. ***Peter works hard so that he can get good grades.***
Peter works hard. He can get good grades.



You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
Connectives_because_sothat_SQ.add_json_chain(JSONPrompt.SQ)
