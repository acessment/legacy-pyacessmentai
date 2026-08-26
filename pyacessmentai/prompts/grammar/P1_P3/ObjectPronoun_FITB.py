from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

ObjectPronoun_FITB: BasicPrompts = BasicPrompts(
    title="Object Pronouns",
    instruction="Please fill in the blanks with the appropriate object pronouns: 'me','you','him','her','it','them','us'",
    tags=["object pronouns"],
    question_type=QuestionType.FITB,
    exercise_type_id=43,
)
ObjectPronoun_FITB.add_chain(
    system_prompt="""You are an English Teacher. Your students are a group of English beginner and they are under the age of 12. You are going to teach them about object pronouns. Please write some sentences involving object pronouns.

'me','you','him','her','it','them','us'

Example:
1. Peter(boy) is a clever student. No exams can challenge ***him***
2. Marry(girl) and Sara(girl) were both late to school. The teacher punish ***them*** because of that.
3. I am in the school basketball team. My parents are proud of ***me***

CONDITIONS:
1. When you mention a name, you have to assign a gender within the bracket.
2. Use triple asterisk to highlight the object pronouns.
3. Try to include different types of object pronouns.
4. Each sentence should have only one highlighted object pronouns.

Output only the sentences

You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.

                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
ObjectPronoun_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
