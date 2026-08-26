from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType


ParticipleAdjectives_ART_FITB: BasicPrompts = BasicPrompts(
    title="Participle Adjectives, '-ed', 'ing'",
    instruction="Please fill in the blanks with the correct form of the adjective",
    tags=["Participle Adjectives"],
    question_type=QuestionType.ARTICLE_FITB,
    exercise_type_id=9,
)
ParticipleAdjectives_ART_FITB.add_chain(
    system_prompt="""You are an english teacher. You are teaching english beginners about the definition between participle adjectives end with "-ed" and "-ing". Typical example would be 'excited' and 'excited' one describes the feeling of a person and one describes the object or event. You are going to write a short story to illustrate this concept

Your story need to satisfy the below two conditions:

1. You need to use triple asterisk to highlight the corresponding adjectives.
2. You need to add the original form of the adjective right next to the participle adjectives

Example of the story:

Sarah was ***excited*** (excite) about her new job. On her first day, she is ***thrilled*** (thrill) to start this new chapter in her life. Her colleagues were ***welcoming***(welcome), which made her feel ***relaxed***(relax). The content of the job is also very ***interesting***(interest).


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.


Output only the story.

""",
    user_prompt="Write the story. Theme:{theme}. Remarks: {remarks}.",
    model=DefinedChatModel.GPT4o,
)
ParticipleAdjectives_ART_FITB.add_json_chain(JSONPrompt.ARTICLE_FITB)

exercise_chain = ParticipleAdjectives_ART_FITB.build_chain()
