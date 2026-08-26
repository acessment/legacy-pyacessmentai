from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType


Adj_As_adj_As_SEL_FITB: BasicPrompts = BasicPrompts(
    title="As... as...",
    instruction="Look at two objects you want to compare. Choose an adjective that describes them correctly with the form of 'as {adjective} as'.",
    tags=["connectives", "as... as..."],
    question_type=QuestionType.SEL_FITB,
    exercise_type_id=2,
)
Adj_As_adj_As_SEL_FITB.add_chain(
    system_prompt="""You are an English teacher. All of your students are under the age of twelve. You are drafting a notes regarding the usage of adjectives with the form ' A is/are as [adjective] as B'. For instance,

Examples:
The mountain is ***as tall as*** the skyscraper.
Her smile is ***as bright*** as the sun.
This puzzle is ***as challenging as*** the last one.
The lake is ***as calm as*** a mirror.
His response was ***as quick as*** lightning.

Options: tall,bright,challenging,calm,quick

and all other adjectives with same rules applied.

Please use triple asterisk to highlight where you have used the adjective. Provide all the adjectives as in the list as options.

Some students are particularly weak in certain aspects. Please customize the examples according to the remarks if provided.

Output only the examples and options.
""",
    user_prompt="Give {numOfQ} examples. Remarks: {remarks} Theme for the output:{theme}",
)
Adj_As_adj_As_SEL_FITB.add_json_chain(JSONPrompt.SEL_FITB)
