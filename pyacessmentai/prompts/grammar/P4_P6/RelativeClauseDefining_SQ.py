from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

RelativeClauseDefining_SQ: BasicPrompts = BasicPrompts(
    title="Rewrite the sentence: Defining Relative Clause 2",
    instruction="Please use defining relative clause to rewrite the sentence.",
    tags=["relative clause", "defining relative clause"],
    question_type=QuestionType.SQ,
    exercise_type_id=72,
)
RelativeClauseDefining_SQ.add_chain(
    system_prompt="""You are an english teacher. Your job is to create some grammar examples regarding how to use defining relative clause.
The examples contain two parts. Part one is two separated sentences without using relative clause. Part two is one single sentence using relative clause. In the example restrict the use of relative clause to only 'which',  'who'

1. I appreciate the man. The man donated a great amount of money to the poor
***I appreciate the man who donated a great amount of money to the poor***

2. The man has a beautiful car. The man is a rich man.
***The man who is a rich man has a beautiful car.***


use triple asterisk to enclose the second part.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.

output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
RelativeClauseDefining_SQ.add_json_chain(JSONPrompt.SQ)

exercise_chain = RelativeClauseDefining_SQ.build_chain()
