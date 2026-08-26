from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

Listen_Play_Prepositions_FITB: BasicPrompts = BasicPrompts(
    title="Preposition: Listen to... play with...",
    instruction="Please fill in the blanks with either 'listen to' or 'play with'",
    tags=["preposition", "to", "with"],
    question_type=QuestionType.FITB,
    exercise_type_id=46,
)
Listen_Play_Prepositions_FITB.add_chain(
    system_prompt="""
You are an English teacher. All of your students are under the age of twelve. You are drafting a notes regarding the usage of prepositions.

1. (listen) to 
2. (play) with


Please use triple asterisk to highlight where you have used the prepositions. For instance:

1. ***Listen to*** instructions carefully or you may fail the test.
2. Do not ***play with*** fire. It's dangerous and you may hurt yourself!
...

You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



Output only the examples.

                             """,
    user_prompt="Give {numOfQ} samples with different choice of verbs. Remarks: {remarks}. Theme: {theme}",
)
Listen_Play_Prepositions_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
