from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType


AdverbsIntro_SEL_FITB: BasicPrompts = BasicPrompts(
    title="Introduction to Adverbs",
    instruction="Please fill in the blanks with the correct adverbs. You have to change the given adjective into appropriate adverbs.",
    tags=["Adverbs"],
    question_type=QuestionType.SEL_FITB,
    exercise_type_id=40,
)
AdverbsIntro_SEL_FITB.add_chain(
    system_prompt="""You are an english teacher teaching beginners under the age of 12. You are going to create some examples of using proper adverbs.

OUTPUT::
Examples:
She is climbing ***slowly*** up the hill. It is going to take a long time for her.
Peter ran so ***fast*** that he won the competition.

Options: slow, fast


CONDITIONS:
Highlight the adverb with triple asterisk.
At the last part of the output, include the adjective that you have used for the examples. The adjective should be just adjective (the original form of an adverb)


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.


output only the examples and options
""",
    user_prompt="Give {numOfQ} examples. Remarks: {remarks} Theme for the output:{theme}",
)
AdverbsIntro_SEL_FITB.add_json_chain(JSONPrompt.SEL_FITB)
