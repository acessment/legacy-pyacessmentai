from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

Lets_SQ: BasicPrompts = BasicPrompts(
    title="Let's",
    instruction="""Please write a suitable sentence using "let's" """,
    tags=["let's"],
    question_type=QuestionType.SQ,
    exercise_type_id=1,
)
Lets_SQ.add_chain(
    system_prompt="""You are an english teacher. Your job is to create some grammar examples regarding how to use "let's" 

The examples should involve a question asking a group of people whether they want or not want to do something, as well as a sentence using "let's" to call for action

1. Are we going to the party tonight?
***Yes, let's go to the party tonight!***

2. Do you want some hot drinks in the cold winter?
***Yes, let's have some hot drinks!***

use triple asterisk to enclose the second sentence




You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.

output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
Lets_SQ.add_json_chain(JSONPrompt.SQ)
