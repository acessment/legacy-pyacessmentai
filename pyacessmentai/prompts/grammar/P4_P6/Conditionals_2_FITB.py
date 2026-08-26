from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

LOGIT_BIAS = {30: -5}
Conditionals_2_FITB: BasicPrompts = BasicPrompts(
    title="Conditionals Type 2",
    instruction="Please fill in the blanks with the correct verb form using conditionals type 2.",
    tags=["Conditionals", "type2"],
    question_type=QuestionType.FITB,
    exercise_type_id=3,
)
Conditionals_2_FITB.add_chain(
    system_prompt="""You are an english teacher. You are teaching english beginners about type 2 conditionals.
You are going to write several different short passages using type 2 conditionals to demonstrate to students the usage of this grammar item. Each short passages should be roughly 20-40 words.

Whenever you use type 2 conditionals, you should use triple asterisk to highlight the verbs within the sentence (including all modal verbs)

also add the bare infinitive of the verb next to the highlighted verb for all cases

you have to customize the examples according to the remarks if provided.

Example:
1. You are so talented in art. Additionally you have won so many competitions. You need to have more faith in yourselves and not giving in to the social expectations. If I ***were*** (be) you, I ***would study*** (study) art.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.

""",
    user_prompt="Give {numOfQ} short passages. Remarks: {remarks}. Theme for the examples:{theme}",
)
Conditionals_2_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)

exercise_chain = Conditionals_2_FITB.build_chain()
