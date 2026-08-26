from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType


Preposition_at_on_festival_FITB: BasicPrompts = BasicPrompts(
    title="Preposition: at, on. (Festivals)",
    instruction="Please fill in the blanks with the correct preposition: 'at','on'",
    tags=["preposition", "at", "on"],
    question_type=QuestionType.FITB,
    exercise_type_id=40,
)
Preposition_at_on_festival_FITB.add_chain(
    system_prompt="""
You are an English teacher. All of your students are under the age of twelve. You are drafting a notes regarding the usage of prepositions of festival:

1. at (Christmas, Mid-autumn festival, Chinese New Year, Ching Ming Festival...)
2. on (Mother's Day, Father's Day, ...)


Please use triple asterisk to highlight where you have used the prepositions. For instance:

1. We always have mooncakes ***at*** Mid-Autumn Festival.
2. Let's buy a gift to our mother ***on*** Mother's Day!
...

You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



Output only the examples.
""",
    user_prompt="Give {numOfQ} examples. Remarks: {remarks} Theme for the output:{theme}",
)
Preposition_at_on_festival_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
