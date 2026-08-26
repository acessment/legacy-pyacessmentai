from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

RelativeClauseDefining_FITB: BasicPrompts = BasicPrompts(
    title="Fill in the blanks: Defining Relative Clause 1",
    instruction="Please fill in the blanks with 'who', 'which', 'where' or 'whose'",
    tags=["relative clause", "defining relative clause"],
    question_type=QuestionType.FITB,
    exercise_type_id=17,
)
RelativeClauseDefining_FITB.add_chain(
    system_prompt="""You are an english teacher. You are teaching english beginners about defining relative clause. You will write a short article using mainly defining relative clauses to demonstrate to students how to apply this grammar item into their writing

Use only "who," "where," "whose," "which," for the demonstration. Use only defining relative clause(without comma)
Please use triple asterisk to highlight the "wh-" word 

Example: 
1. The dog that lives next door is very friendly to everyone ***who*** visits. 
2. The book ***which*** I borrowed from the library contains many interesting facts about history. 
3. The girl ***whose*** brother plays soccer is in my class. 
4. The store ***where*** we bought our groceries offers great discounts on weekends.



You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
RelativeClauseDefining_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)

exercise_chain = RelativeClauseDefining_FITB.build_chain()
