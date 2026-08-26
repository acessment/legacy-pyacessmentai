from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

Quantifiers_lot_few_little_FITB: BasicPrompts = BasicPrompts(
    title="Quantifiers: a lot of, a few, a little",
    instruction="Please fill in the blanks with the appropriate quantifiers: 'a lot of', 'a few', 'a little'. The graphics are given as a hint.",
    tags=["quantifiers", "countable/uncountable", "a lot of", "a few", "a little"],
    question_type=QuestionType.FITB,
    exercise_type_id=40,
)
Quantifiers_lot_few_little_FITB.add_chain(
    system_prompt="""You are an English Teacher. You are going to create some grammar examples for english beginners. All the vocabulary use should be for english beginners.

You need to teach students about quantifiers: 'a lot of', 'a few' and 'a little'.

The examples have to include two parts. First sentence involves the use of the above quantifiers. Second sentence is the results/consequences of that quantifiers. Third part is some emojis to show the quantity. Use 6 emojis to represent a lot of. 1 emoji to represent a little and a few. You can refer to the example below:

Examples: 
1. There are ***a lot of*** apples. We cannot eat them all. 🍎🍎🍎🍎🍎🍎🍎
2. There are ***a few*** oranges. We need to buy more.🍊
3. There are only ***a little*** mango juice left. We should restock. 

Please write some examples.

You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.


output only the examples.
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
Quantifiers_lot_few_little_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
