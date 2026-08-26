from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

ReflexivePronouns_FITB: BasicPrompts = BasicPrompts(
    title="Reflexive Pronouns 1",
    instruction="Please fill in the blanks with the correct reflexive pronoun",
    tags=["Reflexive pronouns"],
    question_type=QuestionType.FITB,
    exercise_type_id=16,
)
ReflexivePronouns_FITB.add_chain(
    system_prompt="""You are an english teacher. You are teaching english beginners about reflexive pronouns. 
                             Please generate some examples. The examples should include all first, second and third person pronouns.
                             highlight where you  have used reflexive pronouns with triple asterisk
                             
                             
You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.


Examples:
The children dressed ***themselves*** before going to school.
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme:{theme}",
)
ReflexivePronouns_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)

exercise_chain = ReflexivePronouns_FITB.build_chain()
