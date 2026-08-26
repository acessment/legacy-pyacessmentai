from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType


ConnectivesAlt_Theref_Since_ART_FITB: BasicPrompts = BasicPrompts(
    title="Connectives: Although, therefore, since",
    instruction="Please fill in the blanks with 'although', 'therefore' or 'since'",
    tags=["Connectives", "although", "since", "therefore"],
    question_type=QuestionType.ARTICLE_FITB,
    exercise_type_id=4,
)
ConnectivesAlt_Theref_Since_ART_FITB.add_chain(
    system_prompt="""You are an english teacher. You are teaching english beginners about connectives: Although, since and therefore. You are going to write a short stroy and integrate the above 3 connectives in the story. Use triple asterisk to highlight the 3 connectives. You should use all the mentioned connectives. You should use those connectives at least 5 times in your story.

Example:
Once upon a time, in a small village, there was a young girl named Lily who loved to explore the forest near her house. ***Although*** everyone in the village warned her about the dangers that lurked in the woods, Lily was brave and adventurous. One day, ***since*** she was determined to find a rare flower that only bloomed deep in the forest, she ignored the warnings and set off on her journey.

As Lily wandered deeper into the woods, she encountered a fierce wolf. ***Although*** she was scared, she remembered her father's advice to stay calm in difficult situations. ***Therefore***, she slowly backed away and managed to escape unharmed.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.

""",
    user_prompt="Theme:{theme}. Write the story in 150 words Remarks: {remarks}",
)
ConnectivesAlt_Theref_Since_ART_FITB.add_json_chain(JSONPrompt.ARTICLE_FITB)

exercise_chain = ConnectivesAlt_Theref_Since_ART_FITB.build_chain()
