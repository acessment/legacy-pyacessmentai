from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType


Preposition_SinceFor_FITB: BasicPrompts = BasicPrompts(
    title="Preposition: since, for",
    instruction="Please fill in the blanks with either 'since' or 'for'",
    tags=["Preposition", "since", "for"],
    question_type=QuestionType.FITB,
    exercise_type_id=40,
)
Preposition_SinceFor_FITB.add_chain(
    system_prompt="""
You are an English teacher. All of your students are under the age of twelve. You are drafting a notes regarding the usage of prepositions of 'since' and 'for':

1. since
2. for


Please use triple asterisk to highlight where you have used the prepositions. For instance:

1. I have been working as a teacher ***for*** 2 decades.
2. I have played badminton ***since*** I was ten.
...

You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



Output only the examples.
""",
    user_prompt="Give {numOfQ} examples. Remarks: {remarks} Theme for the output:{theme}",
)
Preposition_SinceFor_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
