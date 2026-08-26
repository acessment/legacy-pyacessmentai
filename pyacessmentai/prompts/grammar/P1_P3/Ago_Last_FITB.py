from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

Ago_Last_FITB: BasicPrompts = BasicPrompts(
    title="Ago, last",
    instruction="""Please fill in the blanks with either 'ago' or 'last'""",
    tags=["simple past tense", "time"],
    question_type=QuestionType.FITB,
    exercise_type_id=1,
)
Ago_Last_FITB.add_chain(
    system_prompt="""You are an english teacher. Your job is to create some grammar examples regarding how to use the word 'ago' and 'last'. Please use triple asterisks to enclose the word 'ago' and 'last' so that the students can understand.

OUTPUT:
1. We were there 3 months ***ago***.
2. They joined the competition ***last*** year


output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
Ago_Last_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
