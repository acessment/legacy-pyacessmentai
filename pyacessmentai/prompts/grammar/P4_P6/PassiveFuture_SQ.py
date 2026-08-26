from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType


PassiveFuture_SQ: BasicPrompts = BasicPrompts(
    title="Passive Voice: Future Tense",
    instruction="Please rewrite the sentence using passive voice in future tense.",
    tags=["Passive Voice", "Future Tense"],
    question_type=QuestionType.SQ,
    exercise_type_id=10,
)
PassiveFuture_SQ.add_chain(
    system_prompt="""You are an english teacher. You are teaching english beginners about the difference between active voice and passive voice. You are going to write some examples for comparisons.

Use only future tense.

Use triple asterisk to highlight the whole passive voice sentence.
Example:
1. NASA will launch the space shuttle next week.
***The space shuttle will be launched by NASA next week.***


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.


""",
    user_prompt="Give {numOfQ} examples. Remarks: {remarks} Theme for the output:{theme}",
)
PassiveFuture_SQ.add_json_chain(JSONPrompt.SQ)

exercise_chain = PassiveFuture_SQ.build_chain()
