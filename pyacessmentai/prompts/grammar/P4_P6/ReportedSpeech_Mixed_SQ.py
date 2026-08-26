from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

ReportedSpeech_Mixed_SQ: BasicPrompts = BasicPrompts(
    title="Reported Speech Mixed tenses",
    instruction="Please rewrite the sentence into reported speech'",
    tags=["reported speech", "mixed tenses"],
    question_type=QuestionType.SQ,
    exercise_type_id=18,
)
ReportedSpeech_Mixed_SQ.add_chain(
    system_prompt="""You are an english teacher. You are teaching english beginners about reported speech.

Be aware of the change in time expression

The examples should contain a pair of direct and indirect speech.
For within the sentence of direct speech, use only present tense or future tense.

Write some examples:
1. "I like eating apples," said Peter
***Peter said he liked eating apples. ***


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
ReportedSpeech_Mixed_SQ.add_json_chain(JSONPrompt.SQ)

exercise_chain = ReportedSpeech_Mixed_SQ.build_chain()
