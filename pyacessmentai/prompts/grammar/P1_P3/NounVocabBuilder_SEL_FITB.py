from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

NounVocabBuilder_SEL_FITB: BasicPrompts = BasicPrompts(
    title="Vocabulary builder: Noun",
    instruction="Please fill in the blanks with the appropriate word given in the box below.",
    tags=["vocabulary", "noun"],
    question_type=QuestionType.SEL_FITB,
    exercise_type_id=45,
)
NounVocabBuilder_SEL_FITB.add_chain(
    system_prompt="""You are an English Teacher. You are going to create some grammar examples for english beginners. All the vocabulary use should be for english beginners.


You will be given a theme. Your job is to create sample sentences involving the use of different nouns regarding that theme.


Example:
Theme given: Kitchen

Be careful when using a ***knife*** and not to cut yourself.
You can store the food in the ***fridge*** so that they won't rot that quickly.

Options: knife,fridge

CONDITIONS:
1. use triple asterisk to highlight one special noun in each sample
2. Put all the highlighted nouns in options

output only the sample sentences and options

You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.


                             """,
    user_prompt="Give {numOfQ} sample sentences. Remarks: {remarks}. Theme: {theme}",
)
NounVocabBuilder_SEL_FITB.add_json_chain(JSONPrompt.SEL_FITB)
