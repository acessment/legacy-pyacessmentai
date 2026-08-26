from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType


Connectives_and_or_but_FITB: BasicPrompts = BasicPrompts(
    title="Connectives: and, or and but",
    instruction="Please fill in the blanks with the appropriate connectives: 'and', 'or', 'but'",
    tags=["Connectives", "and", "or", "but"],
    question_type=QuestionType.FITB,
    exercise_type_id=42,
)
Connectives_and_or_but_FITB.add_chain(
    system_prompt="""You are an English Teacher. You are teaching beginners about the following connectives:

1. and
2. or
3. but

Try to write some short sentences to demonstrate how to use those connectives.
Examples:
1. She likes both painting ***and*** drawing.
2. Which one do you prefer? Apple juice ***or*** orange juice?
3. The dog is friendly ***but*** shy.

When using or, you must ask the person to choose only one.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



Output only the examples.
""",
    user_prompt="Give {numOfQ} examples. Remarks: {remarks} Theme for the output:{theme}",
)
Connectives_and_or_but_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
