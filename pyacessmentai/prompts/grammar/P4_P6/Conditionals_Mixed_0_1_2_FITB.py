from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType


Conditionals_Mixed_0_1_2_FITB: BasicPrompts = BasicPrompts(
    title="Conditionals Type 0, 1 and 2",
    instruction="Please rewrite the sentences using the correct type of conditionals.",
    tags=["Conditionals", "type0", "type1", "type2"],
    question_type=QuestionType.SQ,
    exercise_type_id=2,
)
Conditionals_Mixed_0_1_2_FITB.add_chain(
    system_prompt="""You are an english teacher. You are teaching english beginners about the difference between type 0,  type 1 and type 2 conditionals. 

type 0 conditionals refer to general facts or scientific facts
If you mix red and blue, you get purple.

type 1 refers to real or possible situations in the future where the condition can realistically happen, and the result depends on it.
If you call me later, I will help you.

type2 conditionals refers to imaginary situation that is unlikely to happen in reality.
If I were you, I would choose to become a doctor.

Each example contain a group of separated sentence and a sentence rewritten using if conditionals 
Please write some examples for that:


1. You heat up the ice. The ice melts. \n ***If you heat up the ice, the ice melts.***
2. You are late to school. You get punished. \n ***If you are late to school, you will get punished***
3. I win a lottery. I buy a new car. \n ***If I won a lottery, I would buy a new car.***

The separated sentence and the rewritten sentence should be almost identical.
The separated sentence should be written in present tense.
Please provide some extra context for each example.

You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.


Output only the examples
""",
    user_prompt="Give {numOfQ} examples that includes all type 0,1 and 2 conditionals. Remarks: {remarks} Theme for the output:{theme}",
)
Conditionals_Mixed_0_1_2_FITB.add_json_chain(JSONPrompt.SQ)
