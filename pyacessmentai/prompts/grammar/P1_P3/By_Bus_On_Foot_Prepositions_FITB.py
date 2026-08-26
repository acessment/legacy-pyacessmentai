from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

By_Bus_On_Foot_Prepositions_FITB: BasicPrompts = BasicPrompts(
    title="Preposition: by bus, on foot",
    instruction="Please fill in the blanks with either 'by' or 'on'",
    tags=["preposition", "by", "on"],
    question_type=QuestionType.FITB,
    exercise_type_id=46,
)
By_Bus_On_Foot_Prepositions_FITB.add_chain(
    system_prompt="""

You are an English teacher. All of your students are under the age of twelve. You are drafting a notes regarding the use of prepositions for different transportation.

1. by (transportation)
2. on (foot)


Please use triple asterisk to highlight where you have used the prepositions. For instance:

1. I go to school ***by*** bus.
2. Travelling ***by*** LRT is the fastest way to explore Tuen Mun.
3. We don't need to get on the bus. We can go to Tsim Sha Tsui ***on*** foot!
...

The use of 'by' and 'on' should be limited to only for transportation.

You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



Output only the examples.

                             """,
    user_prompt="Give {numOfQ} samples with different choice of verbs. Remarks: {remarks}. Theme: {theme}",
)
By_Bus_On_Foot_Prepositions_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
