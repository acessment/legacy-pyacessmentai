from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

RelativeClause_Prep_WhichWhen_FITB: BasicPrompts = BasicPrompts(
    title="Relative Clause (which when)",
    instruction="Modify relative pronouns: For 'where' into phrases like 'from which' or 'by which'; and 'when' into phrases like 'upon which' or 'after which'. These changes allow sentences to be more formal and precise. Look for the highlighted words in the examples.",
    tags=["relative clause", "prepositions"],
    question_type=QuestionType.FITB,
    exercise_type_id=1,
)
RelativeClause_Prep_WhichWhen_FITB.add_chain(
    system_prompt="""You are an English teacher. All of your students are under the age of twelve. You are drafting a notes regarding the use of relative clause with 'where' into 'from/ to/ by which' and 'when' into 'upon/ since/ before/ after which'. For instance,

1. This is the coffee shop in which we first met.
2. There was a moment at which everything changed.
3. There was a day upon which he finally confessed.
4. That was the year since which she has been happily married.
... and other modification.

Please use triple asterisk to highlight where you have used the question words. For instance:

1. This is the road ***by which*** we travelled to the village.
2. That was the moment ***after which*** everything changed.


Some students are particularly weak in certain aspects. Please customize the examples according to the remarks if provided.

Output only the examples.

                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
RelativeClause_Prep_WhichWhen_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
