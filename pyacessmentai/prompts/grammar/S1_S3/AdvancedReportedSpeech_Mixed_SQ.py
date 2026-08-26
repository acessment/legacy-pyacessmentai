from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

AdvancedReportedSpeech_Mixed_SQ: BasicPrompts = BasicPrompts(
    title="Reported Speech Mixed tenses",
    instruction="Please rewrite the sentence into reported speech'",
    tags=["reported speech", "mixed tenses"],
    question_type=QuestionType.SQ,
    exercise_type_id=18,
)
AdvancedReportedSpeech_Mixed_SQ.add_chain(
    system_prompt="""You are an english teacher. You are teaching english beginners about reported speech.

The examples should contain a pair of direct and indirect speech. Use triple asterisk to highlight the whole reported speech sentence.
Please try to incorporate the following changes in your examples:
1. Verb tense shifts
2. Pronoun and possessive changes
3. Time and place references
4. Modal verbs
5. Embedded questions


Example OUTPUT:
1. “I’ll finish the report by tomorrow,” said Maria.
***Maria said (that) she would finish the report by the next day.***

2. “We were planning to move to Canada last year,” said Tom and Sarah.
***Tom and Sarah said (that) they had been planning to move to Canada the previous year.***

3. “Have they completed the renovation yet?” he wanted to know.
***He wanted to know if they had completed the renovation yet.***

You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
AdvancedReportedSpeech_Mixed_SQ.add_json_chain(JSONPrompt.SQ)

exercise_chain = AdvancedReportedSpeech_Mixed_SQ.build_chain()
