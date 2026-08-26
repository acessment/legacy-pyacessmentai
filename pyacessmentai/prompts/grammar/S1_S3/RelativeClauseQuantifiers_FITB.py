from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

RelativeClauseQuantifiers_FITB: BasicPrompts = BasicPrompts(
    title="Relative Clause (quantifiers - of which whom)",
    instruction="Employ 'of' with relative pronouns: Use **'of whom'** or **'of which'** with specific quantifiers like **'both,' 'each,' 'many,'** or **'most'** to form precise sentences. The quantifier must agree with the noun it refers to. Watch for the highlighted words in the examples.",
    tags=["relative clause", "quantifiers"],
    question_type=QuestionType.FITB,
    exercise_type_id=1,
)
RelativeClauseQuantifiers_FITB.add_chain(
    system_prompt="""You are an English teacher. All of your students are under the age of twelve. You are drafting a notes regarding the use of relative clause with specific relative pronouns 'of which' or 'of whom' with some specific quantifiers:

1. both
2. each
3. many
4. most
5. neither
6. none
7. part
8. some
9. a number

and others that lie within the same category for quantifier.

Please use triple asterisk to highlight where you have used the question words. For instance:

1. I have two sisters, both ***of whom*** live abroad.
2. The teacher introduced three new students, each ***of whom*** had excellent academic records.
3. She inherited a collection of rare books, many ***of which*** were first editions.
...


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.


output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
RelativeClauseQuantifiers_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
