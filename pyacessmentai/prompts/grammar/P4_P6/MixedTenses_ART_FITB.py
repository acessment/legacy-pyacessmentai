from pyacessmentai.scripts.BasicPrompts import *
from pyacessmentai.question_class.QuestionType import QuestionType
from pyacessmentai.scripts.DefinedChatModel import DefinedChatModel

"""this module uses only gpt-4o-mini"""
MixedTenses_ART_FITB: BasicPrompts = BasicPrompts(
    title="Mixed Tenses",
    instruction="Please fill in the blanks with the correct tenses of the verb.",
    tags=["Tenses", "mixed tenses"],
    question_type=QuestionType.ARTICLE_FITB,
    exercise_type_id=39,
)
MixedTenses_ART_FITB.add_chain(
    system_prompt="""You are an expert in English teaching for more than 2 decades. You are preparing teaching materials focusing on grammar content for Primary 5.

Possible tenses: 
1. simple present Tense
2. simple past tense
3. present perfect tense
4. simple future tense
5. present continuous tense
6. past continuous tense
7. past perfect tense
8. present perfect continuous
9. past perfect continuous tense
10. future continuous tense

The material should be a set of dialogues that revolves around the given theme by user. The dialogues should only involve the tenses specified in the user prompt

Example:
Specified tenses in the below dialogue:
{simple present tense, simple past tense, present perfect tense, simple future tense}

Alice: Hi John! How are you doing today?

John: Hi Alice! I’m good, thanks. I have just finished a meeting at work. What about you?

Alice: I’m great. I have also just left my work place. By the way, I got a book yesterday. It’s called The Silent Patient. Have you ever heard of it?

John: Yes, I have. I read it last year. It’s a gripping story. Where are you in the book?

Alice: I am about halfway through it. I can’t put it down. Every night, I stay up late to read it.

John: That’s awesome. I remember I did the same too back then. What else is new with you?

Alice: Nothing else. I will go to the library afterwards. Peter will be with me. He really loves reading books.

Requirements:
1. You should add more adverbs of time to specify the time background for each tenses. The below adverbs of time should be used exclusively for that corresponding sentence
1.1 Present perfect tense: {since xxx, just, already, yet, for xx months/years, ever, never...}
1.2 Simple Present tense: {every day, always, usually, often, every week...}
1.3 Simple Past tense:{yesterday, last week/month/Saturday, back then...}
1.4 Simple Future Tense: {tomorrow, next week/month, upcoming...}
1.5 Past Continuous Tense: can use with time adverb like {at that time, at that moment, all night, when, etc.} Focus on an action that was happening at a specific moment in the past.
Or two actions happening at the same time in the past.
1.6 Present Continuous Tense:{right now, at the moment, currently, at the present moment...}
1.7 Past Perfect Tense: time up to a certain point in the past.
1.8 Present Perfect Continuous
1.9 Past Perfect Continuous Tense
1.10 Future Continuous Tense
2. Time setting must be clearly expressed within the dialogue whenever the tenses change
3. Avoid using abbreviation like I'll, they're
4. mention all tenses involved in the last line like this:
Tenses Used:['simple present tense','simple past tense','present perfect tense','simple future tense']




You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.



output only the dialogue""",
    user_prompt="Generate 1 full set of dialogue. The dialogue should be at least {word_count} words long. Tenses specification:{tenses}. The output should be customized according to remarks:{remarks} Theme: {theme}",
    model=DefinedChatModel.GPT4o,
)
MixedTenses_ART_FITB.add_json_chain(JSONPrompt.ARTICLE_FITB)
