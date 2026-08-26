from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

OnceTwiceNeverEver_FITB: BasicPrompts = BasicPrompts(
    title="Frequency: Once, Twice, Never , Ever",
    instruction="Please fill in the blanks with the appropriate number of frequency: Once, Twice, Never, Ever",
    tags=["number", "frequency", "never", "ever"],
    question_type=QuestionType.FITB,
    exercise_type_id=8,
)
OnceTwiceNeverEver_FITB.add_chain(
    system_prompt="""You are an English teacher. All of your students are under the age of twelve. You are drafting a notes regarding the use of "once","twice","never","ever". The format should be as follows:

Examples:
1. Have you ***ever*** been to Paris?
2. I have ***never*** tried swimming. (0)
3. He played drama ***once*** in Primary 3. (1)
4. They went to the mountain ***twice*** last year. (2)

CONDITIONS:
1. please use triple asterisk to highlight the "once","twice","never","ever".
2. mark the number of the action done within the brackets.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



Output only the examples and options.
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
OnceTwiceNeverEver_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)

exercise_chain = OnceTwiceNeverEver_FITB.build_chain()
