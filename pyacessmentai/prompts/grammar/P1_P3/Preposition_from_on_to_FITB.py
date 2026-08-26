from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

Preposition_from_on_to_FITB: BasicPrompts = BasicPrompts(
    title="Prepositions: from, on, to",
    instruction="Please fill in the blanks with the appropriate preposition: 'from', 'on', 'to",
    tags=["Prepositions", "from", "on", "to"],
    question_type=QuestionType.FITB,
    exercise_type_id=21,
)
Preposition_from_on_to_FITB.add_chain(
    system_prompt="""You are an english teacher. You are teaching english beginners about the preposition: "on", "to" and "from" when talking about time and dates. You are going to create some small articles to talk about the date of different events in a schedule using the above mentioned preposition.

Example:
1. Emma was excited because there was a special event at the park. The event was happening ***on*** August 19th, a Saturday. Emma knew she had to be ready on that day.
The event was going to last ***from*** 10 AM ***to*** 4 PM. Emma planned to be there ***from*** the start ***to*** the end, so she could have fun all day.


Highlight only the preposition "on", "from", "to" with triple asterisk, but exclude "to" bare infinitive.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.


output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
Preposition_from_on_to_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
