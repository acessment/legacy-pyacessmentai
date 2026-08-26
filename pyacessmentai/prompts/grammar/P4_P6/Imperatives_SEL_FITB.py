from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType


Imperatives_SEL_FITB: BasicPrompts = BasicPrompts(
    title="Imperatives",
    instruction="Please fill in the blanks with the appropriate verb from the box below. You may use the verb more than once.",
    tags=["imperatives", "verb"],
    question_type=QuestionType.SEL_FITB,
    exercise_type_id=40,
)
Imperatives_SEL_FITB.add_chain(
    system_prompt="""
You are an English teacher. All of your students are under the age of twelve. You are drafting a notes regarding the usage of Imperatives:

1. Look!
2. Stand up
3. Watch Out
4. Give me
5. Stop!

Please also consider other verbs with its use of imperatives.

Please use triple asterisk to highlight where you have used the the above imperatives. Your output should follow the below format:

Examples:
Please ***keep*** quiet! No one is allowed to talk during the exam!
***Watch out***! A car is coming!
***Give*** me a hand.
***Look at*** me when I talk to you, Leo!

Options:
look,stand up,watch out,give,stop


Please always include both options and examples


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



Output only the examples and options.
""",
    user_prompt="Give {numOfQ} examples. Remarks: {remarks} Theme for the output:{theme}",
)
Imperatives_SEL_FITB.add_json_chain(JSONPrompt.SEL_FITB)
