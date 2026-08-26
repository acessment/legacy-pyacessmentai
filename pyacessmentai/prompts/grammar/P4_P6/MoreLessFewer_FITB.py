from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

MoreLessFewer_FITB: BasicPrompts = BasicPrompts(
    title="More, less and fewer.",
    instruction="Please fill in the blanks with 'more', 'less' or 'fewer'",
    tags=["more", "less", "fewer"],
    question_type=QuestionType.FITB,
    exercise_type_id=8,
)
MoreLessFewer_FITB.add_chain(
    system_prompt="""You are an English teacher. Your students are all english beginners. You are drafting some sample sentences to illustrate the use of "more", "less" and "fewer". The examples should revolve around whether the students should or should not do something.

Examples:
1. I should drink ***more*** water because it is important for health.
2. Peter is overweight and should eat ***less*** sugar.
3. I should use ***fewer*** papers to save the planet.

Please highlight the word "more", "fewer" and "less" with triple asterisk.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
MoreLessFewer_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)

exercise_chain = MoreLessFewer_FITB.build_chain()
