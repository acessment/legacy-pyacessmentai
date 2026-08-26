from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

CardinalOrdinal_FITB: BasicPrompts = BasicPrompts(
    title="Cardinal and Ordinal numbers",
    instruction="Please fill in the blanks with either cardinal or ordinal numbers. (one, two, three... first, second, third...)",
    tags=["cardinal and ordinal numbers"],
    question_type=QuestionType.FITB,
    exercise_type_id=41,
)
CardinalOrdinal_FITB.add_chain(
    system_prompt="""You are an English Teacher. Your students are a group of English beginner and they are under the age of 12. You are going to teach them about cardinal and ordinal numbers. Please write some sentences as examples.


Example:
1. I live on the ***first*** (1) floor.
2. I have ***five*** (5) apples

CONDITIONS:
1. use triple asterisk to highlight the english of cardinal and ordinal numbers.
2. put the arabic number in the bracket as hint.
3. The examples together should be a mixed of demonstration of both cardinal and ordinal numbers.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



Output only the sentences
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
CardinalOrdinal_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
