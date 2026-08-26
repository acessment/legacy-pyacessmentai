from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType


AnotherOther_FITB: BasicPrompts = BasicPrompts(
    title="Another and Other",
    instruction="Please fill in the blanks with 'another' or 'other'.",
    tags=["determiners", "another","other"],
    question_type=QuestionType.FITB,
    exercise_type_id=40,
)
AnotherOther_FITB.add_chain(
    system_prompt="""
You are an English teacher. All of your students are under the age of twelve. You are drafting a notes regarding the use of the determiners: "another" and "other".
For each sentence example, please also add contextual information where each question includes a short scenario to help student understand which determiners to use.

Use triple asterisk to highlight where you have used the above determiners as shown above

Example Output:

1. After finishing her first cup of tea, Mary asked for ***another*** cup.
2. I don’t like this shirt. Do you have any ***other*** colors?



""",
    user_prompt="Give {numOfQ} examples. Remarks: {remarks} Theme for the output:{theme}",
)
AnotherOther_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
