from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from dotenv import load_dotenv
import base64
import os

load_dotenv()
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
model4o = AzureChatOpenAI(
    azure_endpoint="https://ACEssmentSponsoredAI1.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview",
    azure_deployment="gpt-4o",
    api_version="2024-08-01-preview",
    api_key=AZURE_API_KEY,
    temperature=0.3,
)

modelDSE = ChatOpenAI(
    model="ft:gpt-4.1-2025-04-14:acessment:dselisteningquestions:C1DcctVH",
    temperature=1.0,
    api_key=OPENAI_API_KEY,
)

listeningQuestionGenSystemPrompt = """You have a tapescript of a conversation among a few people. Your job is to create a listening exercise based on the content of the tapescript.
Use simple vocabularies with the simplest grammar.
Ask about the content and basic information mentioned in the script. Better to ask factual information, numbers, country names, locations, reasons. Ask two types of questions:
Multiple choice questions (mcq) :
Answer that is not a number: multiple choice question. Give four seemingly reasonable options, but among all the 4 options there should be only 1 single correct answer. Paraphrase options so they are not copied from the tapescript.
Short number questions (sq):
Question that could be answered by a year, date, number

Read a few sentences of the tapescript each time, find things that could be asked, ask as many as possible. Then decide whether to ask a multiple choice question or a short number question for each point. Here are the criteria for choosing the type of question:
Multiple choice questions:
Involves descriptions and opinions, a place or name, the view of somebody, the reason of something, the choice someone made, or the description of something.
Short number questions:
If the answer is a year, date, number, it should be a short number question.

Finally, format the questions into the following JSON Array format like the example:
{"questions":[
    {
      "type": "mcq",
      "question": "What is the main difference between electric cars and traditional cars?",
      "options": {
        "a": "Electric cars are quieter",
        "b": "Electric cars run on electricity instead of gasoline",
        "c": "Traditional cars have tailpipe emissions",
        "d": "Traditional cars are more affordable"
      },
      "answer": "B"
    },
    {
        "type": "sq",
        "question": "What year did the Berlin Wall fall?",
        "answer": "1989"
    },
    ... more question objects
]
}

Important notes on making a multiple choice question:
You must avoid the answers being too obvious.
1. The options should be rephrased. Do not copy the sentences from the tapescript directly. 
2. The wrong options should not be an opposite of the correct answer. For example, if the correct answer is "Try to relax", the wrong options should not be "Don't relax", "Don't try to relax", "Try to be nervous", etc.
3. A good wrong option should seem to be like a correct option, but it is not. For example, if the correct answer is "Try to relax", a good wrong option could be "Try to eat more" or "Try to do sports".

After you done all these steps, you should once again paraphrase the questions and options, and improve original sentence structure to make them more concise and different from the tapescript.
Check the questions appear in the same order as the tapescript. If not, re-order them to match the tapescript.
Finally, output the JSON Array without any other message."""

listeningQuestionGenPrompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=listeningQuestionGenSystemPrompt),
        HumanMessagePromptTemplate.from_template("{tapescript}"),
    ]
)

listeningQuestionGenRunnable = listeningQuestionGenPrompt | model4o | JsonOutputParser()


listeningCopyCatInfosheetNonsenseSystemPrompt = """I want to show my love to my crush. She loves textbook exercises. Please help me turn the example exercise in the image into a love exercise. First, change all the content and headers to my love, and express my admiration for her, but keep the structure like the example but more romantic. Finally, there are some blanks in the example, but in your output, you should fill these blanks with appropriate flirting information with her using simple words, but label them as blanks by surrounding the information with square brackets like [this]. Now draw the layout using plain text. Do not output anything besides the layout."""

listeningCopyCatInfosheetSystemPrompt = """You'll receive an example information sheet and a tape script as a part of a listening practice. Your job is to create an information sheet.

You should refer to the layout of the example information sheet. However the example layout is in a heart shape, you should change it back to a normal rectangular shape. 

In the example, blanks are indicated by surrounding the information with a pair of square brackets like [this]. In your information sheet, you should also include same amount of blanks filled with short and simple information, but instead, use <span class='filled_info'> to enclose stuff to be filled. Use exact wording in the script for the filled_info, but use paraphrased text for the rest of the information sheet. Remove redundant or unsuitable parts from the example. One exception is you should not include names and words hard to spell in filled_info.

You should use HTML tables instead of ASCII characters. Output in plain text HTML. start your output with <table> and end with </table>"""


def get_nonsense_infosheet_chain(reference):
    return (
        ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=listeningCopyCatInfosheetNonsenseSystemPrompt),
                HumanMessagePromptTemplate.from_template(
                    template=[
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpg;base64,{base64.b64encode(reference).decode('utf-8')}"},
                        }
                    ]
                ),
            ]
        )
        | model4o
        | StrOutputParser()
    )


listeningCopyCatInfosheetHumanPrompt = """Presenting a plain text information sheet to my crush using my love:
{infosheet}

tapescript:
{tapescript}

Presenting an HTML information sheet to students to fill in information from the tapescript:
"""


listeningCopyCatInfosheetRunnable = (
    ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=listeningCopyCatInfosheetSystemPrompt),
            HumanMessagePromptTemplate.from_template(listeningCopyCatInfosheetHumanPrompt),
        ]
    )
    | model4o
    | StrOutputParser()
)

listeningDSEQuestionsSystemPrompt = """You are creating questions of listening exercises for students.
You will be given the instructions to generate a listening exercise, as well as a tapescript. You job is to create a listening exercise based on the content of the tapescript and output the questions in JSON format
Ask about the content and basic information mentioned in the script. Better to ask factual information, numbers, country names, locations, reasons. Your output can contain these three objects:
Instruction/text (instruction):
The JSON field name is always 'instruction'. There are text only items such as instructions or headers of fill in the blanks questions.
Multiple choice questions (mcq):
Answer that is not a number: multiple choice question. Give four seemingly reasonable options, but among all the 4 options there should be only 1 single correct answer. Paraphrase options so they are not copied from the tapescript.
Fill in the blanks (fitB):
Contains a combination of texts and blanks for the students to fill in. Common items to be filled are year, date, number, facts and reasons in the recording.
Short questions (sq):
Question that could be answered by a year, date, number, facts and reasons in the recording. Usually more challenging.

Only ask questions based on the tapescript. Any information outside the tapescript (e.g. in the user instruction) should be ignored.
It is important to ensure the order of the questions follows the order of occurence in the recording.
Question types can appear in any order and mixed inside the exercise.

Finally, format the questions into the following JSON Object format like the example:
{
    "title": "Listening Task",
    "instruction": "...Situtation of the listening task... Listen to their conversation and complete the information in the spaces below.",
    "questions":[
    {
      "type": "mcq",
      "question": "What is the main difference between electric cars and traditional cars?",
      "options": {
        "a": "Electric cars are quieter",
        "b": "Electric cars run on electricity instead of gasoline",
        "c": "Traditional cars have tailpipe emissions",
        "d": "Traditional cars are more affordable"
      },
      "answer": "B"
    },
    {
        "type": "sq",
        "question": "What year did the Berlin Wall fall?",
        "answer": "1989"
    },
    {
        "type": "instruction",
        "text": "What Iris, Dan and Kaity did at the weekend"
    },
    {
        "type": "fitB",
        "question": [
            {
                "type": "text",
                "text": "Iris had a "
            },
            {
                "type": "blank",
                "text": "terrible",
            },
            {
                "type": "text",
                "text": " weekend because her "
            },
            {
                "type": "blank",
                "text": "dog was sick",
            },
            {
                "type": "text",
                "text": "."
            }
        ]
    },
    ... more questions
]
}

Important notes on making a multiple choice question:
You must avoid the answers being too obvious.
1. The options should be rephrased. Do not copy the sentences from the tapescript directly. 
2. The wrong options should not be an opposite of the correct answer. For example, if the correct answer is "Try to relax", the wrong options should not be "Don't relax", "Don't try to relax", "Try to be nervous", etc.
3. A good wrong option should seem to be like a correct option, but it is not. For example, if the correct answer is "Try to relax", a good wrong option could be "Try to eat more" or "Try to do sports".

After you done all these steps, you should once again paraphrase the questions and options, and improve original sentence structure to make them more concise and different from the tapescript.
Check the questions appear in the same order as the tapescript. If not, re-order them to match the tapescript.
Finally, output the JSON Object without any other message."""
listeningDSEQuestionsPrompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=listeningDSEQuestionsSystemPrompt),
        HumanMessagePromptTemplate.from_template(
            "Tapescript:\n{tapescript}\n\nUser prompt:\nAround {length} words. DSE listening comprehension exercise:\n{theme}."
        ),
    ]
)
listeningDSEQuestionsRunnable = listeningDSEQuestionsPrompt | modelDSE | JsonOutputParser()
