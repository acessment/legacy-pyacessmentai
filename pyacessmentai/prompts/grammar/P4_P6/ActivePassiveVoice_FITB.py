from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

ActivePassiveVoice_FITB: BasicPrompts = BasicPrompts(
    title="Active and Passive Voice",
    instruction="Identify whether each sentence is in active or passive voice. Please fill in the blanks using the correct form of the verb. Be careful of the tenses.",
    tags=["active voice", "passive voice"],
    question_type=QuestionType.SEL_FITB,
    exercise_type_id=86,
)

ActivePassiveVoice_FITB.add_chain(
    system_prompt="""
You are an English teacher. Prepare a grammar notes for active and passive voice by writing several sample sentences using either active voice or passive voice.
Try to include only the following tenses (Future tense, simple present tense and simple past tense). Use triple asterisks to highlight the verbs in the sentences.
Write the sentence under the subtitle of "Examples".
Write the bare infinitive form of the verbs used in the sentences under the subtitle of "Options".

Example OUTPUT:

Examples:
1. The report ***was written*** by the students yesterday.
2. The government ***is building*** a new bridge.
3. The movie ***was directed*** by a famous filmmaker.
4. Everyday a pack of milk ***is delivered*** to my house.
5. The cake ***will be eaten*** by the children in the next hour.
6. The shopkeeper ***sells*** the best fruits in town.

Options:
write, build, direct, deliver, eat, sell
""",
    user_prompt="Generate {numOfQ} examples. Remarks: {remarks} Theme for the output:{theme}",
    model=DefinedChatModel.GPT4o,
)
ActivePassiveVoice_FITB.add_json_chain(JSONPrompt.SEL_FITB)
