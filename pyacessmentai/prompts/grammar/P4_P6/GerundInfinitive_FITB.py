from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

GerundInfinitive_FITB: BasicPrompts = BasicPrompts(
    title="Gerund and bare infinitives",
    instruction="Please fill in the blanks with either gerund or bare infinitives.",
    tags=["Gerund", "Bare infinitives"],
    question_type=QuestionType.FITB,
    exercise_type_id=54,
)
GerundInfinitive_FITB.add_chain(
    system_prompt="""You are an english teacher. You are teaching english beginners to determine when they should apply gerund or to infinitive right after a verb. You are going to write some examples to demonstrate these concepts.

1. There is a supermarket near my home. Therefore, during the ride back home, I usually stop there ***to buy*** (buy) some groceries.
2. I have just finished all exams and the results are really bad, so I stop ***playing*** (play) computer games.

Rules:
1. You should use triple asterisk to highlight the corresponding bare infinities and gerund.
2. You should provide again the verb in bare infinitive in the brackets as shown in the above example.
3. Please focus more on verbs that can be followed by either gerund or infinitive, such as
Stop
Remember
Forget
Try
Regret
Mean
Go on
Need
Learn
Prefer
Continue
Propose
Consider
Require
Advise
Recommend
4. Please try to include both examples of gerund and infinitive for one verb in the whole set of examples, so that the teacher can demonstrate the difference.
5. Please add some extra context in each sentence to support the use of gerund or to-infinitive in that case.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the examples
                             """,
    user_prompt="Give {numOfQ} examples. Remarks: {remarks}. Theme: {theme}",
)
GerundInfinitive_FITB.add_json_chain(JSONPrompt.ONE_BY_ONE_FITB)

exercise_chain = GerundInfinitive_FITB.build_chain()
