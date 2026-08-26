from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType


PhrasalVerb_FITB: BasicPrompts = BasicPrompts(
    title="Introduction to Phrasal Verb",
    instruction="Please complete the following phrasal verb using the correct preposition.",
    tags=["phrasal verb", "prepositions"],
    question_type=QuestionType.FITB,
    exercise_type_id=14,
)
PhrasalVerb_FITB.add_chain(
    system_prompt="""Phrasal Verb
You are an english teacher teaching beginners.
Topic: Phrasal Verb
The examples should only focus on the most common phrasal verb for english beginner.

Format:


You should hint the (meaning) of the phrasal verbs by introducing a verb
in bracket to assist students finishing the exercise.

You should use triple asterisk to highlight the preposition only

Example:
1. The detective look ***into*** the murder case thoroughly. (investigate)
2. The lady looks ***after*** her kids. (take care)
3. We should look ***at*** people when we are talking. (give a sight onto sth.)

Use triple asterisk to highlight the corresponding preposition inside the phrasal verb.

You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.


""",
    user_prompt="Give {numOfQ} examples. Remarks: {remarks} Theme for the output:{theme}",
)
PhrasalVerb_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)

exercise_chain = PhrasalVerb_FITB.build_chain()
