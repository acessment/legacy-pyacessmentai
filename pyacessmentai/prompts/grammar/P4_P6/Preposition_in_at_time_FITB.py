from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType


Preposition_in_at_time_FITB: BasicPrompts = BasicPrompts(
    title="Preposition: in, at. (Time)",
    instruction="Please fill in the blanks with the correct preposition: 'in','at'",
    tags=["preposition", "in", "at"],
    question_type=QuestionType.FITB,
    exercise_type_id=40,
)
Preposition_in_at_time_FITB.add_chain(
    system_prompt="""
You are an English teacher. All of your students are under the age of twelve. You are drafting a notes regarding the usage of prepositions of time:

1. in (century, season, month)
2. at (o'clock, 11:30 pm, lunchtime, the moment, midnight...)


Please use triple asterisk to highlight where you have used the prepositions. For instance:

1. Farmers pick cherries ***in*** summer.
2. Let's meet ***at*** 5 o'clock tomorrow!
...

You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



Output only the examples.
""",
    user_prompt="Give {numOfQ} examples. Remarks: {remarks} Theme for the output:{theme}",
)
Preposition_in_at_time_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
