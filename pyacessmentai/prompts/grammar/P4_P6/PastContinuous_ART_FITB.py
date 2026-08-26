from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType


PastContinuous_ART_FITB: BasicPrompts = BasicPrompts(
    title="Introduction to Past Continuous Tense",
    instruction="Please fill in the blanks with the correct verb form",
    tags=["Tenses", "Past Continuous Tense"],
    question_type=QuestionType.ARTICLE_FITB,
    exercise_type_id=13,
)
PastContinuous_ART_FITB.add_chain(
    system_prompt="""You are an english teacher. You are teaching english beginners about past continuous tense.

Write a short story involving the use of past continuous tense. Include at least 5 sentences with past continuous tense. You also want to include both the use of was and were in the past continuous tense to make the example more dynamic.

Use triple asterisk to highlight where you have used past continuous tense.
Add bare infinitive right next to it.

Example:
While Ben ***was doing*** (do) his homework, his mom ***was cooking*** (cook) dinner.

You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



Output only the story
""",
    user_prompt="Write the story in 150 words. Remarks: {remarks} Theme for the output:{theme}",
)
PastContinuous_ART_FITB.add_json_chain(JSONPrompt.ARTICLE_FITB)

exercise_chain = PastContinuous_ART_FITB.build_chain()
