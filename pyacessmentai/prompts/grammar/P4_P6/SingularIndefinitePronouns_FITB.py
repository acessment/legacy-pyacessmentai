from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

SingularIndefinitePronouns_FITB: BasicPrompts = BasicPrompts(
    title="Singular Indefinite Pronoun",
    instruction="Please fill in the blanks with the correct indefinite pronouns: Everyone, someone, nobody, anyone",
    tags=["singular indefinite pronouns"],
    question_type=QuestionType.FITB,
    exercise_type_id=19,
)
SingularIndefinitePronouns_FITB.add_chain(
    system_prompt="""Indefinite Pronouns I
You are an expert in English teaching for more than 2 decades. You are
preparing teaching materials (grammar examples) focusing on grammar
content for Primary 5.
Topic: Singular Indefinite Pronouns
Everyone, someone, anyone, nobody

Format:
1. ***Everyone*** is welcomed to attend this meeting.
2. ***Nobody*** is allowed to get into this building without prior official approval.
3. ***Someone*** help me!' screamed the lady.
4. Is there ***anyone*** who wants to join the group?



You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
SingularIndefinitePronouns_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)

exercise_chain = SingularIndefinitePronouns_FITB.build_chain()
