from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

IrregularVerbPastTense_SEL_FITB: BasicPrompts = BasicPrompts(
    title="Irregular verbs, Past Tense",
    instruction="Please fill in the blanks with the appropriate verb from the box and change the verb into past tense.",
    tags=["tenses", "simple past tense", "irregular verbs"],
    question_type=QuestionType.SEL_FITB,
    exercise_type_id=44,
)
IrregularVerbPastTense_SEL_FITB.add_chain(
    system_prompt="""You are an English teacher. Your students are complete beginner and under the age of 12.

You are going to teach them about irregular verb in past tense. Your task is to create some sentences using irregular verb in past tense.

Output example:

Example:
I ***bought*** a really tasty cake from the bakery yesterday.
Peter ***took*** away my pencil last week.

Options:
buy,take

CONDITIONS:
1. Use triple asterisk to highlight the irregular verb.
2. At the last part of the output, you should include the bare infinitive of the verbs you used.
3. Mention the time setting clearly in every sentences using phrases like last week, yesterday etc.
4. Output only the example and options


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.

                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
IrregularVerbPastTense_SEL_FITB.add_json_chain(JSONPrompt.SEL_FITB)
