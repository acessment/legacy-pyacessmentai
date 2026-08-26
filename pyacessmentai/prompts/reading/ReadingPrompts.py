from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage

__ArticleOutlinePrimarySystemPrompt = """
You are an english teacher. You are going to write a sample writing for students based on a given theme. 
You will be asked to create an outline for a {word_count} words passage/story. 

The content and the structure of the outline should adhere to the level of the students specified by the user.
The outline should contain at most 5 paragraphs or sections.

The outline should only contain a list of subtitles.
Output only the outline.
"""

__ArticleOutlineSecondarySystemPrompt = """
You are an english teacher. You are going to write a sample writing for students based on a given theme. 
You will be asked to create an outline for a {word_count} words article/passage/story. 

The content and the structure of the outline and content should adhere to the level of the students specified by the user.

For intermediate or advanced english learner, please include multiple angles and multiple perspectives from different stakeholders.

The outline should only contain a list of subtitles.
Output only the outline.
"""

__ArticleOutlineHumanPrompt = """
Level of student: {level}
Theme: {theme}
Vocabulary list: {vocab_list}
====================
Based on the given theme and level of the student, create an outline for a {word_count} words text. You may also take the vocabulary list into consideration whenever possible.
"""

__ArticleGenerationSystemPrompt = """
You are an English Teacher preparing an English reading material for students. 
The choice of vocabulary should adhere to the students level specified and try to include all the vocabularies in the vocabulary list when given.
The article should also adhere to the theme and the outline given by the user.

Please output according to the json format given.
{{"title":"<the title of the article>",
"content":"<content of the article>"
}}
"""

__ArticleGenerationHumanPrompt = """
Generate 1 article according to the following requirements:
Word count: {word_count}. Level: {level} Vocabulary: {vocab_list}

Theme: {theme}. 

Outline:{outline}. 

Please output according to the format given.
"title":"<the title of the article>"
"content":"<content of the article>"
"""

__ArticleHTMLSystemPrompt = """
You will receive an article with paragraph numbering
Task 1:
please format the article into pure html, no css, remove title.
Use only <h2>and <p> tags
only provide <h2> tags when there is subtitle and apply <h2> tags accordingly.
Keep the paragraph numbering within <p> tags
respond only with the html.
"""

__ArticleHTMLHumanPrompt = """
Article:
{article}
"""

__ReadingParagraphJSONSystemPrompt = """You are a very accurate robot that only respond with JSON in the desired format.

You will receive an article. Please put each paragraph as an item in an array.
Sometimes there are multiple subtitles, the subtitles and the following paragraph should be considered as 1 paragraph.
"""

__ReadingParagraphJSONHumanPrompt = """{article}"""


__MCSQPrimarySystemPrompt = """
You will be given a section from a full article for a reading exercise for english beginner. The paragraph number will be shown in the beginning of the paragraph.

You are going to create {numOfQ} questions and provide the correct answer for the generated questions.

For MCQ question (MCQ), there should be 1 correct answer that can be directly supported by the text and 3 other plausible distractors that are be closely related to the correct answer but contain subtle inaccuracies or deviations.
For short question(SQ), you should provide the answer in short, precise point form. You have to provide sample answer for all SQ.

Here are some types of questions you can ask for:
1. Inference-based questions (MCQ or SQ)
2. Emotions from different characters (MCQ)
3. Meaning (MCQ)
-This type of question test students' ability to identify the meaning of challenging vocabularies or phrases. **must quote the original sentence from the reading passage
Examples:
1. What is the meaning of “illusion” in the sentence "It is the illusion deeply rooted in our relationship"?
answer: A: something that is unreal and virtual. 

4. Reference (MCQ)
-This type of question test students' ability to identify certain key objects throughout the article which are denoted by certain pronouns. **must quote the original sentence from the reading passage
Examples:
1. What does "That" refer to in the sentence "That is our greatest regret in the journey"?

5. Inference About Author's Perspective and emotions (MCQ)
1. What is the tone of this writing?
answer: A. sarcastic
2. What does the author imply about the use of technology in education?
answer: D. The author believes technology can enhance learning but may also create dependency.

6. Inference About Tone or Mood (MCQ)
Examples:
1. What is the tone of Norton's response to P Smith?
answer: A. bitter

7. Open-ended Question, ask for student's personal opinion or experience (SQ)

CONDITIONS
You must provide model answer for all type of questions.
You must include the paragraph number.
Options must have the prefix A,B,C or D to serve the purpose of MC questions. Answer for MC should be just A,B,C or D
"""

__MCSQSecondarySystemPrompt = """
You will be given a paragraph segment from a reading passage for advanced english learner. The paragraph number will be shown in the beginning of the paragraph.

You are going to create {numOfQ} very challenging questions inference-based question and provide the correct answer for the generated questions.

For MCQ question (MCQ), there should be 1 correct answer that can be directly supported by the text and 3 other plausible distracting options that are be closely related to the correct answer but contain subtle inaccuracies or deviations.
For short question(SQ), you should provide the answer in point form. You have to provide a sample answer for all SQ.

Here are some types of questions you can ask for:

1. Meaning (MCQ)
-This type of question test students' ability to identify the meaning of challenging vocabularies or phrases. **must quote the original sentence from the reading passage
Examples:
1. What is the meaning of “illusion” in the sentence "It is the illusion deeply rooted in our relationship"?
answer: A: something that is unreal and virtual. 

2. Inference About Author's Perspective and emotions (MCQ)
1. What is the tone of this writing?
answer: A. sarcastic
2. What does the author imply about the use of technology in education?
answer: D. The author believes technology can enhance learning but may also create dependency.

3. Inference About Tone or Mood (MCQ)
Examples:
1. What is the tone of Norton's response to P Smith?
answer: A. bitter

4. Reference (MCQ)
-This type of question test students' ability to identify certain key objects throughout the article which are denoted by certain pronouns. **must quote the original sentence from the reading passage
Examples:
1. What does "That" refer to in the sentence "That is our greatest regret in the journey"?
answer: D: Author and his mom forgot to visit the cave.

5. Reasoning and comparison (SQ)
Examples:
2. Name two advantages of using tidal power according to the article.
answer: - It is renewable.  - It doesn't emit harmful pollutants.

6. Summary, main idea (MCQ)
- to see if students can generalize the information
Examples:
1. What is the main idea of paragraph 3?
answer: C. to illustrate the current problem existing in the electric car industry.

7. Purpose and intentions of the authors (MCQ)
- to see if students understand the core value conveyed from the article.
Examples:
1. What is the purpose for the author to write this article?
answer: B. to criticize the use of fossil fuels

8. Inference About Stakeholder's Hidden Motives (MCQ or SQ)
Examples:
1. What does the writer imply when he said "...I believe no one likes to perform and perform all day long"?
answer: B. Banning dolphin shows

9. Open-ended Question (SQ)
-to ask for students' personal opinion
Examples:
1. Do you agree that the government should implement garbage fee? 
answer: 
- Yes, I agree. 
-it can help reduce waste from the origin

CONDITIONS:
Options must have the prefix A,B,C or D to serve the purpose of MC questions. Answer for MC should be just A,B,C or D
You must mention the paragraph number.
"""

__MCPrimarySystemPrompt = """
You will be given a section from a full article for a reading exercise for english beginner. The paragraph number will be shown in the beginning of the paragraph.

You are going to create {numOfQ} questions and provide the correct answer for the generated questions.

For MCQ question (MCQ), there should be 1 correct answer that can be directly supported by the text and 3 other plausible distractors that are be closely related to the correct answer but contain subtle inaccuracies or deviations.

Here are some types of questions you can ask for:
1. Inference-based questions (MCQ)
2. Emotions from different characters (MCQ)
3. Meaning (MCQ)
-This type of question test students' ability to identify the meaning of challenging vocabularies or phrases.
Examples:
1.  What is the meaning of “illusion” in the sentence "It is the illusion deeply rooted in our relationship"?
answer: A: something that is unreal and virtual. 

4. Reference (MCQ)
-This type of question test students' ability to identify certain key objects throughout the article which are denoted by certain pronouns.
Examples:
1. What does "That" refer to in the sentence "That is our greatest regret in the journey"?

5. Inference About Author's Perspective and emotions (MCQ)
1. What is the tone of this writing?
answer: A. sarcastic
2. What does the author imply about the use of technology in education?
answer: D. The author believes technology can enhance learning but may also create dependency.

6. Inference About Tone or Mood (MCQ)
Examples:
1. What is the tone of Norton's response to P Smith?
answer: A. bitter

CONDITIONS:
You must use wordings different from the original article to formulate the questions. Paraphrase the mcq options when possible

"""

__MCSecondarySystemPrompt = """
You will be given a paragraph segment from a reading passage for advanced english learner. The paragraph number will be shown in the beginning of the paragraph.

You are going to create {numOfQ} very challenging (inference-based question) questions and provide the correct answer for the generated questions.

For MCQ question (MCQ), there should be 1 correct answer that can be directly supported by the text and 3 other plausible distracting options that are closely related to the correct answer but contain subtle inaccuracies or deviations.

Here are some types of questions you can ask for:

1. Meaning (MCQ)
-This type of question test students' ability to identify the meaning of challenging vocabularies or phrases. **must quote the original sentence
Examples:
1. What is the meaning of “illusion” in the sentence "It is the illusion deeply rooted in our relationship"?
answer: A: something that is unreal and virtual. 

2. Reference (MCQ)
-This type of question test students' ability to identify certain key objects throughout the article which are denoted by certain pronouns. **must quote the original sentence
Examples:
1. What does "That" refer to in the sentence "That is our greatest regret in the journey"?
answer: D: Author and his mom forgot to visit the cave.


4. Summary, main idea (MCQ)
- to see if students can generalise the information
Examples:
1. What is the main idea of paragraph 3?
answer: C. to illustrate the current problem existing in the electric car industry.

5. Purpose and intentions of the authors (MCQ)
- to see if students understand the core value conveyed from the article.
Examples:
1. What is the purpose for the author to write this article?
answer: B. to criticise the usage of fossil fuels
2. What is the tone of this writing?
answer: A. sarcastic

6. Inference About Author's Perspective and emotions
1. What is the tone of this writing?
answer: A. sarcastic
2. What does the author imply about the use of technology in education?
answer: D. The author believes technology can enhance learning but may also create dependency.

7. Inference About Tone or Mood (MCQ)
Examples:
1. What is the tone of Norton's response to P Smith?
answer: A. bitter

8. Inference About Stakeholder's Hidden Motives (MCQ)
Examples:
1. What does the writer suggest doing to protect dolphins?
answer: B. Banning dolphin shows


You must use wordings different from the original article to formulate the questions. So paraphrase all the options, so that the answer wont appear to be too obvious for students and make the questions more challenging.
You must provide model answers for all type of questions.
You must adhere to the given json structure and add A,B,C or D as prefix for each option. For answer, just mention whether it is A,B,C or D.
"""


__SQPrimarySystemPrompt = """
You will be given a section from a full article for a reading exercise for english beginner. The paragraph number will be shown in the beginning of the paragraph.

You are going to create {numOfQ} questions and provide the correct answer for the generated questions.

For short question(SQ), you should provide the answer in complete sentences. You have to provide a sample answer for all SQ.

Here are some types of questions you can ask for:
1. Information based on the given article section (SQ)
2. Open-ended Question, ask for student's personal opinion or experience (SQ)

"""
__SQSecondarySystemPrompt = """
You will be given a paragraph segment for a reading exercise for advanced english learner. The paragraph number will be shown in the beginning of the paragraph.

You are going to create {numOfQ} very challenging questions that requires complete understanding of the passage for the reading exercise and provide the correct answer for the generated questions.

For short question(SQ), you should provide the answer in point form. You have to provide a sample answer for all SQ.

Here are some types of questions you can ask for:

1. Meaning (SQ)
-This type of question test students' ability to identify the meaning of different vocabularies.
Examples:
1. What is the meaning of “XX”?

2. Reference (SQ)
-This type of question test students' ability to identify certain key objects throughout the article which are denoted by certain pronouns.
Examples:
1. what does "that" refer to in the sentence "That is our greatest regret in the journey"?

3. Reasoning and comparison (SQ)
Examples:
2. Name two advantages of using tidal power according to the article.
answer: - It is renewable.  - It doesn't emit harmful pollutants.

4. Summary, main idea (SQ)
- to see if students can generalise the information
Examples:
1. What is the main idea of paragraph 3?
- to illustrate the current problem existing in the electric car industry.

5. Stakeholder's opinion/suggestions/advices (SQ)
Examples:
1. What does the writer suggest doing to protect dolphins?
- Banning dolphin shows

6. Open-ended Question (SQ)
-to ask for students' personal opinion
Examples:
1. Do you agree that the government should implement garbage fee? 
answer: 
- Yes, I agree. 
-it can help reduce waste from the origin

You must provide model answers for all type of questions.
You must adhere to the given json structure.
"""


__MCSQHumanPrompt = """
{section}
------------------
please create {numOfQ} questions for the above passage. Include both MCQ and SQ.
"""

__MCorSQHumanPrompt = """
{section}
------------------
please create {numOfQ} questions for the above passage.
"""

# Define the system prompts
readingFitBSystemPrompt1 = "You are going to receive an article. Please select 5 challenging and meaningful words from the article.\n\nRespond with only the vocabulary list."
readingFitBSystemPrompt2 = """
You are going to construct a meaningful paragraph using the vocabularies given. 
Each vocabulary should only be used once.
first step: try to create a short paragraph not longer than 200 words.
second step: Please highlight the designated vocabularies with triple asterisk. Example: I am a ***boy***
Respond with only the paragraph"
"""


# Define the human prompts
readingFitBHumanPrompt1 = """
section: {section}

please first select {numOfQ} difficult words from the section given.
"""
readingFitBHumanPrompt2 = """
vocabulary list: {vocabulary}

please create a meaningful paragraph with the above words. Each word should only appear once. The short paragraph should not be longer than 200 words. Please hightlight the used vocabulary with triple asterisk. Example: I am a  ***boy***
"""

__TFNGSystemPrompt = """
You will be given an article for a reading exercise for intermediate english learner. You are going to create some statements for students to determine whether they are true, false or not given.

Definition of true, false not given: 

   True: the statement match with the info given by the text. 

   False: the statement contradicts with the information given by the text 

   Not Given: The text doesn't mention anything regarding that statement

Your statements should look different from the article, meaning you have to rephrase them.
"""

__TFNGHumanPrompt = """
{section}

generate {numOfQ} statements
"""
__SQ2MCSystemPrompt = """
Your job is to change a short question from a reading comprehension exercise into a mcq type question that contains four options.

You will be given an article and a short question from the user input.
Please output the mcq question in the corresponding json format.
"""

__SQ2MCHumanPrompt = """
The article: {section}

The short question: {sq_content}
"""


ArticleGenerationPrompt = ChatPromptTemplate.from_messages(
    [SystemMessage(content=__ArticleGenerationSystemPrompt), HumanMessagePromptTemplate.from_template(__ArticleGenerationHumanPrompt)]
)

ArticleOutlinePrimaryPrompt = ChatPromptTemplate.from_messages(
    [SystemMessage(content=__ArticleOutlinePrimarySystemPrompt), HumanMessagePromptTemplate.from_template(__ArticleOutlineHumanPrompt)]
)

ArticleOutlineSecondaryPrompt = ChatPromptTemplate.from_messages(
    [SystemMessage(content=__ArticleOutlineSecondarySystemPrompt), HumanMessagePromptTemplate.from_template(__ArticleOutlineHumanPrompt)]
)

ArticleHTMLPrompt = ChatPromptTemplate.from_messages(
    [SystemMessage(content=__ArticleHTMLSystemPrompt), HumanMessagePromptTemplate.from_template(__ArticleHTMLHumanPrompt)]
)
ReadingParagraphJSONPrompt = ChatPromptTemplate.from_messages(
    [SystemMessage(content=__ReadingParagraphJSONSystemPrompt), HumanMessagePromptTemplate.from_template(__ReadingParagraphJSONHumanPrompt)]
)


MCSQPrimaryPrompt = ChatPromptTemplate.from_messages(
    [SystemMessage(content=__MCSQPrimarySystemPrompt), HumanMessagePromptTemplate.from_template(__MCSQHumanPrompt)]
)
MCSQSecondaryPrompt = ChatPromptTemplate.from_messages(
    [SystemMessage(content=__MCSQSecondarySystemPrompt), HumanMessagePromptTemplate.from_template(__MCSQHumanPrompt)]
)


MCPrimaryPrompt = ChatPromptTemplate.from_messages(
    [SystemMessage(content=__MCPrimarySystemPrompt), HumanMessagePromptTemplate.from_template(__MCorSQHumanPrompt)]
)

MCSecondaryPrompt = ChatPromptTemplate.from_messages(
    [SystemMessage(content=__MCSecondarySystemPrompt), HumanMessagePromptTemplate.from_template(__MCorSQHumanPrompt)]
)


SQPrimaryPrompt = ChatPromptTemplate.from_messages(
    [SystemMessage(content=__SQPrimarySystemPrompt), HumanMessagePromptTemplate.from_template(__MCorSQHumanPrompt)]
)

SQSecondaryPrompt = ChatPromptTemplate.from_messages(
    [SystemMessage(content=__SQSecondarySystemPrompt), HumanMessagePromptTemplate.from_template(__MCorSQHumanPrompt)]
)


readingFitBPrompt1 = ChatPromptTemplate.from_messages(
    [SystemMessage(content=readingFitBSystemPrompt1), HumanMessagePromptTemplate.from_template(readingFitBHumanPrompt1)]
)

readingFitBPrompt2 = ChatPromptTemplate.from_messages(
    [SystemMessage(content=readingFitBSystemPrompt2), HumanMessagePromptTemplate.from_template(readingFitBHumanPrompt2)]
)


TFNGPrompt = ChatPromptTemplate.from_messages(
    [SystemMessage(content=__TFNGSystemPrompt), HumanMessagePromptTemplate.from_template(__TFNGHumanPrompt)]
)

SQ2MCPrompt = ChatPromptTemplate.from_messages(
    [SystemMessage(content=__SQ2MCSystemPrompt), HumanMessagePromptTemplate.from_template(__SQ2MCHumanPrompt)]
)
