from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

Preposition_in_on_at_FITB: BasicPrompts = BasicPrompts(
    title="Prepositions: in, on, at",
    instruction="Please fill in the blanks with 'in', 'on', 'at'",
    tags=["Prepositions", "in", "on", "at"],
    question_type=QuestionType.FITB,
    exercise_type_id=21,
)
Preposition_in_on_at_FITB.add_chain(
    system_prompt="""You are an English teacher. You are drafting a notes regarding the difference between in, on and at. Your job is to create certain examples regarding those 3 prepositions


please use triple asterisk to highlight where you have used the prepositions
1. My grandpa is ***in*** the hospital now.
2. There are 5 apples ***on*** the table.
3. I wait for you ***at*** the bus stop



You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
Preposition_in_on_at_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
