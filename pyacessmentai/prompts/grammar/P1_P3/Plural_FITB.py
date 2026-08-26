from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

Plural_FITB: BasicPrompts = BasicPrompts(
    title="Plural nouns",
    instruction="Please fill in the blanks with the correct singular or plural noun",
    tags=["countable/uncountable", "Plural"],
    question_type=QuestionType.FITB,
    exercise_type_id=21,
)
Plural_FITB.add_chain(
    system_prompt="""You are an english teacher. Your job is to create some grammar examples regarding singular and plural nouns for english beginner.
You should include examples for different cases like when to add 's', 'es', 'ies' or even change form like from child to children. And also when to keep the singular form.

You should follow the following format
Use triple asterisk to highlight the singular/plural form are in the sentence.
Use bracket to contain the original singular form

Examples:
1. There are four ***apples*** (apple).

You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
Plural_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)
