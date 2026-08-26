from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

QuestionsWords_FITB: BasicPrompts = BasicPrompts(
    title="Questions words 1",
    instruction="Please fill in the blanks with the correct question words: 'What','How','When','Where','Who','Why','Which'",
    tags=["Question words"],
    question_type=QuestionType.FITB,
    exercise_type_id=21,
)
QuestionsWords_FITB.add_chain(
    system_prompt="""You are an English teacher. You are drafting a notes regarding the question words:
1. What
2. How
3. When
4. Where
5. Who
6. Why
7. Which

please use triple asterisk to highlight where you have used the question words:
1. ***When*** is our lunch time? - Our lunch time is 12pm.
2. ***Which*** one is your favourite? Blue or yellow? - My favourite colour is blue.

Remember to add options when using 'which'.

You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
QuestionsWords_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
