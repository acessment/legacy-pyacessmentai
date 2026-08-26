from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType


Comparative_Superlative_Adj_ART_FITB: BasicPrompts = BasicPrompts(
    title="Comparative and Superlative adjectives",
    instruction="Please fill in the blanks with the correct form of adjectives.",
    tags=["Adjectives", "Superlative", "Comparative"],
    question_type=QuestionType.ARTICLE_FITB,
    exercise_type_id=40,
)
Comparative_Superlative_Adj_ART_FITB.add_chain(
    system_prompt="""You are an English teacher. All of your students are under the age of twelve. You are drafting a paragraph involving the use of comparative and superlative adjectives:

The new car I bought is ***faster than*** (fast) my old one, but it’s not ***the fastest*** (fast) car on the road. It’s also ***more comfortable*** (comfortable) than my previous car, which makes long trips much ***easier*** (easy). However, the price was ***higher than*** (high) I expected, and it's definitely ***the most expensive*** (most) car I've ever owned. Still, it feels like ***the best*** (good) choice for me!

1. Use triple asterisk to enclose the corresponding comparative or superlative adjectives.
2. Add the original form of the adjective in the brackets

You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.

Output only the examples.
...


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



Output only the examples.
""",
    user_prompt="Give 1 paragraph in 150 words. Remarks: {remarks} Theme for the output:{theme}",
)
Comparative_Superlative_Adj_ART_FITB.add_json_chain(JSONPrompt.ARTICLE_FITB)
