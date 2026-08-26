from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType


Connectives_If_Unless_FITB: BasicPrompts = BasicPrompts(
    title="Connectives: If & Unless",
    instruction="Please fill in the blanks with either 'if' or 'unless'",
    tags=["Connectives", "If", "If-Clauses", "Unless"],
    question_type=QuestionType.FITB,
    exercise_type_id=6,
)
Connectives_If_Unless_FITB.add_chain(
    system_prompt="""You are an english teacher. You are teaching english beginners about the difference between 'if' and 'unless'. 

Examples:
1. ***Unless*** you practice regularly, you will not improve your skills. 
2. ***If*** you take the first step, you will have a chance to succeed
 

use triple asterisk to highlight where you have used 'unless' and 'if'


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



Output only the examples. 
Shuffle the order of the examples before output.
Shuffle the order of the examples before output.
""",
    user_prompt="Give {numOfQ} examples. Remarks: {remarks} Theme for the output:{theme}",
)
Connectives_If_Unless_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)

exercise_chain = Connectives_If_Unless_FITB.build_chain()
