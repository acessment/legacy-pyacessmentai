from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

Future_Tense_Advance_3Types_FITB: BasicPrompts = BasicPrompts(
    title="Advance usage of Expressing Future Actions",
    instruction="Please fill in the following blanks with the correct tenses.",
    tags=["relative clause", "prepositions"],
    question_type=QuestionType.FITB,
    exercise_type_id=1,
)
Future_Tense_Advance_3Types_FITB.add_chain(
    system_prompt="""You are an English teacher. All of your students are at the Key Stage 3. You are drafting a notes regarding the use of tenses and other verb form for describing future actions:

1) "Will": Used for spontaneous decisions, promises, or predictions without prior arrangements.
2) "Be going to": Used for plans or intentions that have already been made, or for predictions based on current evidence.
3) "Present Continuous": Used for definite, scheduled future arrangements where the time and place are often mentioned.

Examples:

1. I think the team ***will win*** the match. [win]
2. Look at the sky! I think it ***is going to rain***. [rain]
3. Professor Johnson ***is travelling*** to Paris for a conference next week. [travel]
4. I ***will open*** the window. [open]
...
Please use triple asterisk to highlight where you have used the question words.


Some students are particularly weak in certain aspects. Please customize the examples according to the remarks if provided.

Output only the examples.

                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
Future_Tense_Advance_3Types_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
