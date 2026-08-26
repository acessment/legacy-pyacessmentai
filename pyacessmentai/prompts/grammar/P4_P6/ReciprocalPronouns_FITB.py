from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

ReciprocalPronouns_FITB: BasicPrompts = BasicPrompts(
    title='Reciprocal Pronouns: "one another" and "each other"',
    instruction='Please fill in the blanks with either "one another" or "each other" ',
    tags=["Reciprocal Pronouns", "Pronouns", "each other", "one another"],
    question_type=QuestionType.FITB,
    exercise_type_id=15,
)
ReciprocalPronouns_FITB.add_chain(
    system_prompt="""You are an english teacher. You are teaching english beginners about the difference between "each other" and "one another".
You are going to write some examples for comparisons. 


"Each other": Generally used when referring to two subjects.
"One another": Typically used when referring to more than two subjects.


Example:
1. Jack and Jill helped ***each other*** with their homework.
2. The team members congratulated ***one another*** after winning the match.


Please use triple asterisk to highlight only where you have applied the phrase "each other" and "one another"

You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.


Output only the examples

                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme for the output:{theme}",
)
ReciprocalPronouns_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
