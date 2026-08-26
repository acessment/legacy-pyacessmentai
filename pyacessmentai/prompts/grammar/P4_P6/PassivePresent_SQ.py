from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType


PassivePresent_SQ: BasicPrompts = BasicPrompts(
    title="Passive Voice: Present Tense",
    instruction="Please rewrite the sentence using passive voice in present tense.",
    tags=["Passive Voice", "Present Tense"],
    question_type=QuestionType.SQ,
    exercise_type_id=12,
)
PassivePresent_SQ.add_chain(
    system_prompt="""You are an english teacher. You are teaching english beginners about the difference between active voice and passive voice. You are going to write some examples for comparisons.

Use only simple present tense.

Use triple asterisk to highlight the whole passive voice sentence.
Example:
1. The air pressure forces the door to close itself.
***The door is forced by the air pressure to close itself***


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.


""",
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme for the output:{theme}",
)
PassivePresent_SQ.add_json_chain(JSONPrompt.SQ)

exercise_chain = PassivePresent_SQ.build_chain()
