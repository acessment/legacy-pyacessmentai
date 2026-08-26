from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

Articles_FITB: BasicPrompts = BasicPrompts(
    title="Articles: 'a' & 'an'",
    instruction="Please fill in the blanks with the correct articles.",
    tags=["Articles"],
    question_type=QuestionType.FITB,
    exercise_type_id=1,
)
Articles_FITB.add_chain(
    system_prompt="""You are an english teacher. Your job is to create some grammar examples regarding articles 'a' and 'an' 

Create sentences using the articles mentioned. Use triple asterisk to highlight where the articles are in the sentence like this:

1. This is ***an*** apple
2. He is ***a*** boy


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.

output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
Articles_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
