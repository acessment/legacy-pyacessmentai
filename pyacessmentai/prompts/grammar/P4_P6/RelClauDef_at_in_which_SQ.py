from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

RelClauDef_at_in_which_SQ: BasicPrompts = BasicPrompts(
    title="Rewrite the sentence: Defining Relative Clause 3, 'at which', 'in which'",
    instruction="Please rewrite the sentence using 'at which' and 'in which'",
    tags=["relative clause", "defining relative clause"],
    question_type=QuestionType.SQ,
    exercise_type_id=73,
)
RelClauDef_at_in_which_SQ.add_chain(
    system_prompt="""You are an english teacher. Your job is to create some grammar examples regarding how to use defining relative clause, specifically targeting the interchangeability of group 1:  'when'or  'where' and group 2: 'at which' or  'in which'
The examples contain two parts. Part one is a random relative clause sentence using group 1 or group 2, part two is the corresponding alternatives using group 2

Some examples...

1. I remember the day when we first met at the park.
***I remember the day at which we first met at the park.***

2. I love visiting the town where my grandparents live.
***I love visiting the town in which my grandparents live***


use triple asterisk to enclose the second part.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.

output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
RelClauDef_at_in_which_SQ.add_json_chain(JSONPrompt.SQ)
