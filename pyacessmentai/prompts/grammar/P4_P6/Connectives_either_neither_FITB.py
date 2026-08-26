from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

Connectives_either_neither_FITB: BasicPrompts = BasicPrompts(
    title="Connectives: Either... or..., neither... nor...",
    instruction="Please fill in the blanks with 'Either... or..., neither... nor...'",
    tags=["Connectives", "either or", "neither nor"],
    question_type=QuestionType.FITB,
    exercise_type_id=5,
)
Connectives_either_neither_FITB.add_chain(
    system_prompt="""You are an english teacher. You are teaching english beginners about 3 types of connectives:
1. either...... or......
2. neither.....or.....
Use triple asterisk to highlight the preposition.

Examples:
1. We can ***either*** eat in ***or*** dine out.
2. ***Neither*** an ice cream ***nor*** a pudding can ease my stress right now.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
Connectives_either_neither_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)

exercise_chain = Connectives_either_neither_FITB.build_chain()
