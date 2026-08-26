from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

PossessivePronouns_FITB: BasicPrompts = BasicPrompts(
    title="Possessive Pronouns",
    instruction="Please fill in the blanks with the correct possessive pronouns: 'mine','yours','his'...etc.",
    tags=["Pronouns", "Possessive Pronouns"],
    question_type=QuestionType.FITB,
    exercise_type_id=20,
)
PossessivePronouns_FITB.add_chain(
    system_prompt="""Possessive Pronouns
You are an expert in English teaching for more than 2 decades. You are
preparing teaching materials (grammar examples) focusing on grammar
content for Primary 5.

examples:
1. This is my pen. The pen is ***mine***.
2. This is her doll. The doll is ***hers***. 
3. The car belongs to my father. The car is ***his***. 


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
PossessivePronouns_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)

exercise_chain = PossessivePronouns_FITB.build_chain()
