from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

HowQAdjective_FITB: BasicPrompts = BasicPrompts(
    title="How+Adjectives: How heavy, how deep, how tall, how long, how fast, how hot, how big",
    instruction="Please fill in the blanks with 'how heavy', 'how deep', 'how tall', 'how long', 'how fast', 'how hot', or 'how big'",
    tags=["How questions", "How_(adjective)"],
    question_type=QuestionType.FITB,
    exercise_type_id=8,
)
HowQAdjective_FITB.add_chain(
    system_prompt="""You are an english teacher. You are teaching english beginners about the following grammar item:
How + units of measurements

Only include the following adjectives:
1. Heavy
2. Deep
3. Tall
4. Long
5. Fast
6. Hot
7. Big

You will write some examples. Each examples contains one question and an answer.

Examples:
1. ***How heavy*** are these clothes?
 - They weigh about 1 kilograms.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
HowQAdjective_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)

exercise_chain = HowQAdjective_FITB.build_chain()
