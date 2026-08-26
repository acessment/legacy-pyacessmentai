from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType


Preposition_with_in_FITB: BasicPrompts = BasicPrompts(
    title="Preposition: with, in",
    instruction="Please fill in the blanks with the correct preposition: 'with' or 'in'",
    tags=["preposition", "with", "in"],
    question_type=QuestionType.FITB,
    exercise_type_id=40,
)
Preposition_with_in_FITB.add_chain(
    system_prompt="""
You are an English teacher. All of your students are under the age of twelve. You are drafting a notes regarding the usage of prepositions of 'with' and 'in':

1. with (body parts or accessories)
2. in (clothing items)

Please use triple asterisk to highlight where you have used the prepositions for expressing
I. body parts or accessories and
II. Clothing items.
For instance:
1. She greeted him ***with*** a smile.
2. He opened the door ***with*** his right hand.
3. The man stood ***in*** a black suit.
4. The children ran outside ***in*** their raincoats.

...


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



Output only the examples.
""",
    user_prompt="Give {numOfQ} examples. Remarks: {remarks} Theme for the output:{theme}",
)
Preposition_with_in_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
