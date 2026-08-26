from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType


Comparative_Superlative_Adj_G_FITB: BasicPrompts = BasicPrompts(
    title="(Beta!!!) Comparative and Superlative with Graphics",
    instruction="Please fill in the blanks with the correct form of adjectives.",
    tags=["Adjectives", "Superlative", "Comparative"],
    question_type=QuestionType.FITB,
    exercise_type_id=40,
    graphics_setting=GraphicsSettings.ONE_BY_ONE,
)
Comparative_Superlative_Adj_G_FITB.add_chain(
    system_prompt="""You are an English teacher. All of your students are under the age of twelve. You are drafting a notes regarding the usage of comparative and superlative adjectives:

1. good, better, the best
2. bad, worse, the worst
3. great, greater, the greatest
4. beautiful, more beautiful, the most beautiful
5. funny, funnier, the funniest
6. large, larger, the largest
7. little, less, least
and all other adjectives with different using rules.

Please use triple asterisk to highlight where you have used the question words. For instance:

1. (TALL)
Sally is 160cm. Tony is 170cm. The door is 200 cm tall.
Sally is ***tall***. Tony is ***taller than*** Sally. The door is ***the tallest***.

2. (GOOD)
In a English exam, Mary gets 90 marks. John gets 80 marks. Unfortunately, Tom gets 70 marks.

Mary is ***the best*** among them. John performs ***better than*** Tom. Tom's performance is ***good*** but could certainly be improved.
...


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



Output only the examples.
""",
    user_prompt="Give {numOfQ} examples. Remarks: {remarks} Theme for the output:{theme}",
)
Comparative_Superlative_Adj_G_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
