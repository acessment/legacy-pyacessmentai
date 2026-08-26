from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

AdjectivePreposition_FITB: BasicPrompts = BasicPrompts(
    title="Adjective and Preposition Collocation",
    instruction="Please fill in the blanks with correct prepositions.",
    tags=["Adjective", "Preposition"],
    question_type=QuestionType.FITB,
    exercise_type_id=1,
)
AdjectivePreposition_FITB.add_chain(
    system_prompt="""You are an english teacher. You are teaching english beginners adjective preposition collocation. (Adjective + Preposition)

Use triple asterisk to highlight the preposition.

Examples:
1. I am excited ***about*** the disney trip tomorrow
2. I am happy ***for*** you.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
AdjectivePreposition_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)

exercise_chain = AdjectivePreposition_FITB.build_chain()
