from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

EmbeddedQuestions_FITB: BasicPrompts = BasicPrompts(
    title="Embedded Question",
    instruction="Please complete the sentences using embedded question.",
    tags=["Embedded Question"],
    question_type=QuestionType.FITB,
    exercise_type_id=8,
)
EmbeddedQuestions_FITB.add_chain(
    system_prompt="""You are an English Teacher. You are going to create some examples regarding embedded questions.

1. Who is Mary?
Do you know ***who Mary is***.

2. When is your birthday?
I don't know ***when your birthday is***.

Try to create more examples following the above structure
use triple asterisk to highlight the embedded question

output only the examples.
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
EmbeddedQuestions_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
