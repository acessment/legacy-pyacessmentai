from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

CouldCan_SEL_FITB: BasicPrompts = BasicPrompts(
    title="Could/Can",
    instruction="Please fill in the blanks using the appropriate modal verb: 'can' or 'could', together with the verb in the box below. Add negation (not) whenever necessary",
    tags=["modal verb", "can", "could"],
    question_type=QuestionType.SEL_FITB,
    exercise_type_id=7,
)
CouldCan_SEL_FITB.add_chain(
    system_prompt="""You are an English teacher. All of your students are under the age of twelve. You are drafting a notes regarding the difference between "can" and "could". The format should be as follows:

Examples: 
I ***could run*** very fast when I was young.
Most of the fish ***cannot leave*** water.
***Could*** your dad ***drive*** a car when he was young?

Options:
run, leave, drive

CONDITIONS:
1. use triple asterisk to highlight the modal verb and the verb following afterwards
2. the output consists of two parts, examples and options.
3. Please include all the verbs under options.
4. When using "could", the action must be referring to the past. Please include that information within the sentence.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



Output only the examples and options.
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
CouldCan_SEL_FITB.add_json_chain(JSONPrompt.SEL_FITB)

exercise_chain = CouldCan_SEL_FITB.build_chain()
