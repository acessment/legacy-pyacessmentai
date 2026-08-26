from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType


Conditionals_0_1_SQ: BasicPrompts = BasicPrompts(
    title="Conditionals Type 0 and 1",
    instruction="Please rewrite the sentences using the correct type of conditionals.",
    tags=["Conditionals", "type0", "type1"],
    question_type=QuestionType.SQ,
    exercise_type_id=2,
)
Conditionals_0_1_SQ.add_chain(
    system_prompt="""You are an english teacher. You are teaching english beginners about the difference between type 0 and type 1 conditionals. 

type 0 conditionals refer to general facts or scientific facts
If you mix red and blue, you get purple.
type 1 refers to real or possible situations in the future where the condition can realistically happen, and the result depends on it.
If you call me later, I will help you.

Each examples contain a group of separated sentence and a sentence rewritten using if conditionals (either type 0 or type 1)
Please write some examples for that:


1. You heat up the ice. The ice melts. \n ***If you heat up the ice, the ice melts.***
2. You are late to school. You get punished. \n ***If you are late to school, you will get punished***

The separated sentence and the rewritten sentence should be almost identical.

You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.


Output only the examples
""",
    user_prompt="Give {numOfQ} examples. Remarks: {remarks} Theme for the output:{theme}",
)
Conditionals_0_1_SQ.add_json_chain(JSONPrompt.SQ)
