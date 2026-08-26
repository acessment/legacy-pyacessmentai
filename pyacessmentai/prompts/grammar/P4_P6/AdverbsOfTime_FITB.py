from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType


AdverbsOfTime_FITB: BasicPrompts = BasicPrompts(
    title="Adverbs of time",
    instruction="Please fill in the blanks with the correct adverbs of time: always, usually, sometimes, seldom, never.",
    tags=["Adverbs", "time", "adverbs of time"],
    question_type=QuestionType.FITB,
    exercise_type_id=40,
)
AdverbsOfTime_FITB.add_chain(
    system_prompt="""You are an english teacher. Your job is to create some grammar examples regarding the following adverbs of time:
always, usually, sometimes,seldom,never

always: 7/week
usually: 4-6/week
sometimes: 2-3/week
seldom: 1-2/year



Each example should contain 2 parts, first part explicitly mention the number of frequency of that activity. Second part use the adverbs of time.

1. Peter goes to the library 7 days a week. Peter ***always*** goes to the library.

2. Mary does not know how to swim. Mary has ***never*** swum

Use only week as time unit for sometimes,usually and always
Use year for seldom

use triple asterisk to enclose the adverbs of time


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.

output only the examples
""",
    user_prompt="Give {numOfQ} examples. Remarks: {remarks} Theme for the output:{theme}",
)
AdverbsOfTime_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
