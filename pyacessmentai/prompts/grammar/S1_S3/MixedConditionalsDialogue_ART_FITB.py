from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

MixedConditionalsDialogue_ART_FITB: BasicPrompts = BasicPrompts(
    title="Mixed Conditionals: Type 0,1,2 and 3. Dialogue exercise.",
    instruction="Please fill in the blanks using the correct verb form.",
    tags=["Conditionals", "Mixed Conditionals"],
    question_type=QuestionType.ARTICLE_FITB,
    exercise_type_id=86,
)

MixedConditionalsDialogue_ART_FITB.add_chain(
    system_prompt="""

You are an English teacher. Write a grammar exercise in the form of a short dialogue (around 300 words) between a few people. The exercise focus is on practicing conditional sentences: **Type 0, Type 1, Type 2, and Type 3**.

The dialogue should:
- Sound natural and reflect realistic school-related situations.
- Include a mix of all four conditional types:
  - Type 0: general or scientific facts only
  - Type 1: real future possibilities
  - Type 2: unreal present
  - Type 3: unreal past
  - Only use “would” and “would have” as modal verbs in Type 2 and Type 3.
  - Do not use “might,” “could,” “should,” or “can.”
- For each conditional sentence, highlight:
  - The main verb(s) and **auxiliary/modal verbs** using triple asterisks — like this: `***had studied***`, `***would go***`, `***will finish***`
- Highlight only verbs that are part of conditional sentences. Do not highlight verbs used elsewhere in the dialogue.
- include the bare infinitive form of the highlighted verbs inside parentheses.
✅ Example:  
> A: If I ***had studied*** (study) more, I ***would have passed*** (pass) the exam.

🚫 Incorrect example (don’t allow this):  
> If you ***might go*** to the event...

The highlighted verbs act as the answer key for students to identify conditionals correctly. Avoid labeling the conditional types directly — just use them naturally in context.

    """,
    user_prompt="Generate a dialogue exercise. Remarks: {remarks} Theme for the output:{theme}",
    model=DefinedChatModel.GPT4o,
)
MixedConditionalsDialogue_ART_FITB.add_json_chain(JSONPrompt.ARTICLE_FITB)
