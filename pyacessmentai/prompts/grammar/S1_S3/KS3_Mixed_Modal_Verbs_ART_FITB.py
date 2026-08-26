from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType

KS3_Mixed_Modal_Verbs_ART_FITB: BasicPrompts = BasicPrompts(
    title="Mixed Modal Verb (can, should, would, must, could)",
    instruction="Please fill in the blanks using appropriate modal verbs (can, could, should, must, would)",
    tags=["modal verbs", "mixed modal verbs", "can", "should", "could", "would", "must"],
    question_type=QuestionType.ARTICLE_FITB,
    exercise_type_id=1,
)
KS3_Mixed_Modal_Verbs_ART_FITB.add_chain(
    system_prompt="""You are an english teacher. Your job is to create one grammar examples regarding how to use different modal verbs such as "can", "should", "must", "would", "could". 
The example should be a conversation or a a short story for any theme.

Highlight where you have used the modal verbs by encapsulating them inside triple asterisk.

Anna: Hey, Ben! ***Can*** you help me with something?

Ben: Of course, what do you need?

Anna: I’m trying to decide if I ***should*** buy a new phone or just fix my old one. What ***would*** you do in my situation?

Ben: Hmm, that’s tricky. ***Can*** your current phone still work for a while, or is it completely broken?

Anna: It’s not totally broken. I ***can*** still use it, but the battery dies quickly, and the screen is cracked. So, I could get by, but it’s pretty frustrating.

Ben: I understand. Well, if the phone still works, you ***could*** keep using it for a bit, but you ***should*** definitely think about how long that’ll be comfortable. ***Would*** you feel okay using a phone that keeps dying all the time?

Anna: Not really. It's been annoying, and I don’t want it to suddenly stop working when I need it. But then again, I don’t want to rush into buying a new one.

Ben: Yeah, you ***shouldn't*** rush, but you ***should*** also think about how much the repairs will cost. Sometimes fixing it ***could*** be more expensive than getting a new phone altogether. If you think it’s close to dying, you ***must*** consider replacing it sooner than later.

Anna: True. I guess I ***could*** wait for a sale or something. But I’m not sure if I ***should*** deal with it breaking completely before I do anything.

Ben: Exactly. If it stops working at the wrong time, it ***could*** cause a lot of trouble, especially if you need it for an emergency. I ***would*** suggest starting to look for deals now, even if you're not ready to buy right away. That way, if a good one pops up, you ***can*** jump on it.

Anna: Good idea! I guess I ***should*** be more proactive about it. But I ***must*** admit, I’ve been putting it off because I don’t really want to deal with all the new phone options out there. Anyways, thanks, Ben! You always have good advice. I ***could*** definitely use a second opinion when I’m ready to buy.

Ben: No problem! Just let me know when you're ready to make the decision.


You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.

output only the examples

                             """,
    user_prompt="Give 1 examples. Remarks: {remarks}. Theme: {theme}.",
)
KS3_Mixed_Modal_Verbs_ART_FITB.add_json_chain(JSONPrompt.ARTICLE_FITB)
