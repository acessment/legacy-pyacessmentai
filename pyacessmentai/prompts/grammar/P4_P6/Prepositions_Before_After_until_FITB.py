from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

Prepositions_Before_After_until_FITB: BasicPrompts = BasicPrompts(
    title="Prepositions: Before, after, until",
    instruction="Please fill in the blanks with 'before', 'after', or 'until",
    tags=["Prepositions", "Before", "After", "Until"],
    question_type=QuestionType.ARTICLE_FITB,
    exercise_type_id=15,
)
Prepositions_Before_After_until_FITB.add_chain(
    system_prompt="""You are an english teacher. You are teaching english beginners about prepositions: before, after and until.
You are going to write a short step-by-step guide (could be about any anything) to demonstrate how to use the above three prepositions.

Use triple asterisk to highlight the corresponding prepositions.

Example:
Step 1: Prepare the Ingredients
***Before*** you start cooking, make sure you have all your ingredients ready.
Grate the Parmesan cheese ***before*** you begin boiling the spaghetti.
Cut the pancetta or bacon into small pieces ***before*** you start frying it.
Step 2: Boil the Spaghetti
Fill a large pot with water and add a pinch of salt.
***After*** the water comes to a boil, add the spaghetti.
Cook the spaghetti ***until*** it is al dente, which usually takes about 8-10 minutes.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                             """,
    user_prompt="write a step-by-step guide about {theme}. Remarks: {remarks}.",
)
Prepositions_Before_After_until_FITB.add_json_chain(JSONPrompt.ARTICLE_FITB)

exercise_chain = Prepositions_Before_After_until_FITB.build_chain()
