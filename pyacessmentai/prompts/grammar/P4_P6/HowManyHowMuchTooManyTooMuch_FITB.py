from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

HowManyHowMuchTooManyTooMuch_FITB: BasicPrompts = BasicPrompts(
    title="How many, How much, Too many, Too much",
    instruction="Please fill in the blanks with 'How many', 'How much', 'Too many' or 'Too much'.",
    tags=["How questions", "How many", "How much", "Too many", "Too much"],
    question_type=QuestionType.FITB,
    exercise_type_id=8,
)
HowManyHowMuchTooManyTooMuch_FITB.add_chain(
    system_prompt="""You are an english teacher. You are teaching english beginners about the following grammar item:
Using \"how many\", \"how much\", \"too many\" and \"too much\"

Only include the following adjectives:
1. How many
2. How much
3. Too many
4. Too much

You will write some examples. Each examples contains one question and an answer.

Examples:
1. ***How many*** apples are there?
 - There are 5 apples.
2. There are 1000 apples. We only need 100 apples. 
 - There are ***too many*** apples.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
HowManyHowMuchTooManyTooMuch_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)

exercise_chain = HowManyHowMuchTooManyTooMuch_FITB.build_chain()
