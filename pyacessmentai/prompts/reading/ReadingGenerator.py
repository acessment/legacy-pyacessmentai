from datetime import datetime
import re
import json

from pydantic import ValidationError

from pyacessmentai.question_class.CategoryType import Category


from .Difficulty import Difficulty
from .ReadingQuestionType import ReadingQuestionType
from .ReadingPrompts import *
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from .LLMModelType import LLMModelType
from typing import TypedDict, Optional
from .ResponseType import (
    ArticleResponse,
    MCSQResponse,
    ParagraphJSONResponse,
    TFNGResponse,
)
from . import Arithmetic as af
from . import StringParser as sp  # whatever this name should be

from langchain_core.runnables import RunnableParallel, RunnableLambda

import math

json_parser = JsonOutputParser()
str_parser = StrOutputParser()


class ReadingGenerator:
    class __ArticleDict(TypedDict):
        title: str
        content: str

    def __init__(
        self,
        article_model: LLMModelType = LLMModelType.Offline_GPT4o,
    ):
        """Questions are generated based on section. Section is a group consisting multiple paragraphs.
        Users should specify the number of paragraphs in one section and how many questions they want in 1 paragraph.
        If the number of questions is too high, the questions may become repetitive.


        """

        self.article_model = article_model.value

    def __parse_fitB(self, fitBstr: str):
        """parsing fitB text to fitB type json object"""
        raw_question_array = sp.split_asterisks(fitBstr)
        fitb_question_array = []
        for key, raw_text in enumerate(raw_question_array):
            fitb_type = "blank" if key % 2 == 1 else "text"
            json_obj = {"type": fitb_type, "text": raw_text}
            fitb_question_array.append(json_obj)
        json_question = {
            "type": ReadingQuestionType.FITB.value,
            "question": fitb_question_array,
        }
        return json_question

    def __parse_html(self, html_str: str) -> str:
        """parse html string"""
        return re.sub(r"html```|```|html`|`|html", "", html_str)

    def __parse_article_response(self, article_str: str) -> __ArticleDict:
        """Parse string response from LLM into proper JSON format"""
        try:
            # Try to parse as JSON first
            if article_str.strip().startswith("{"):
                return json.loads(article_str)

            # If not JSON, parse the string format (this can be deprecated cuz json formatting is allowed for perplexity again)
            # Updated regex to handle escaped quotes within content
            title_match = re.search(r'"title"\s*:\s*"((?:[^"\\]|\\.)*)"', article_str)
            content_match = re.search(r'"content"\s*:\s*"((?:[^"\\]|\\.)*)"', article_str, re.DOTALL)

            if title_match and content_match:
                # Unescape the captured content
                title = title_match.group(1).replace('\\"', '"').replace('\\n', '\n')
                content = content_match.group(1).replace('\\"', '"').replace('\\n', '\n')
                return {"title": title, "content": content}
            else:
                # Fallback: try to extract content between quotes
                lines = article_str.strip().split("\n")
                title = ""
                content = ""

                for line in lines:
                    if "title" in line.lower():
                        title_match = re.search(r'"((?:[^"\\]|\\.)*)"', line)
                        if title_match:
                            title = title_match.group(1).replace('\\"', '"').replace('\\n', '\n')
                    elif "content" in line.lower():
                        content_match = re.search(r'"((?:[^"\\]|\\.)*)"', line)
                        if content_match:
                            content = content_match.group(1).replace('\\"', '"').replace('\\n', '\n')

                return {"title": title, "content": content}

        except Exception as e:
            print(f"Error parsing article response: {e}")
            # Fallback to simple parsing
            return {"title": "Generated Article", "content": article_str}

    def create_article_outline(
        self,
        theme: str,
        word_count: int,
        level: Difficulty,
        vocab_list: list[str] = ["none"],
    ) -> str:
        """generate article outline before generating article for better, richer content"""
        print("generating outline")
        vocab_list = ",".join(vocab_list)

        if level == Difficulty.S1_S3 or level == Difficulty.S4_S6:
            llm_chain = ArticleOutlineSecondaryPrompt | self.article_model | str_parser
        else:
            llm_chain = ArticleOutlinePrimaryPrompt | self.article_model | str_parser
        outline = llm_chain.invoke(
            {
                "word_count": word_count,
                "level": level,
                "vocab_list": vocab_list,
                "theme": theme,
            }
        )
        print(outline)
        return outline

    def create_article(
        self,
        outline: str,
        theme: str,
        word_count: int,
        level: Difficulty,
        vocab_list: list[str] = ["none"],
        stream: bool = False,
    ) -> __ArticleDict:
        """This function returns a dict containing the title and the body text"""
        print("generating article")
        vocab_list = ",".join(vocab_list)
        # structured_model = self.article_model.with_structured_output(ArticleResponse)
        llm_chain = ArticleGenerationPrompt | self.article_model | str_parser
        if True:
            try:
                article_response = llm_chain.invoke(
                    {
                        "word_count": word_count,
                        "level": level,
                        "vocab_list": vocab_list,
                        "theme": theme,
                        "outline": outline,
                    }
                )
            except Exception as e:
                print(e)
                raise ValueError("failed to produce results from AI, please try again, or switch to OpenAI")

            # Parse the string response into proper JSON format
            print(article_response)
            article_response = self.__parse_article_response(article_response)
            print(article_response["title"])
            print(article_response["content"])
            return article_response
        else:
            return llm_chain.stream(
                {
                    "word_count": word_count,
                    "level": level,
                    "vocab_list": vocab_list,
                    "theme": theme,
                    "outline": outline,
                }
            )

    def create_html(self, paragraph_array: list[str]) -> str:
        """returns html string"""
        print("generating html")
        llm_chain = ArticleHTMLPrompt | LLMModelType.Offline_GPT4oMini.value | str_parser
        article_html = llm_chain.invoke({"article": af.join_paragraph(paragraph_array)})
        return self.__parse_html(article_html)

    def get_paragraph_array(self, article: str) -> list[str]:
        """
        feed in an article and get an array of paragraphs
        This function operates on AI so no specific requirements for the format of the article
        """
        print("generating paragraph array")
        structured_model = LLMModelType.Offline_GPT4o.value.with_structured_output(ParagraphJSONResponse)
        llm_chain = ReadingParagraphJSONPrompt | structured_model
        paragraphJSON_response = llm_chain.invoke({"article": article})
        paragraph_array = [f"[{index+1}] {paragraph}" for index, paragraph in enumerate(paragraphJSON_response.paragraphs)]
        return paragraph_array

    def __create_section(self, article: str, paragraph_array: list[str], level: Difficulty) -> list[list[str]]:
        """create section by grouping several paragraphs together, no grouping of paragraphs when word_count is under 500 words
        section size will be equal to one when difficulty == KS1,KS2
        or when word_count < 450
        """
        if level == Difficulty.P1_P3 or level == Difficulty.P4_P6:
            return paragraph_array
        else:
            article_word_count = af.count_words(article)
            section_size = af.get_section_size(
                article_word_count=article_word_count,
                num_paragraphs=len(paragraph_array),
            )
            section_array = af.chunk_array(array=paragraph_array, size=section_size)
            return section_array

    def create_question(
        self,
        question_type: ReadingQuestionType,
        section_text: str,
        numOfQ: int,
        level: Difficulty,
    ) -> list | dict:
        """
        return a either a json object of the question with the given question type and number of questions.
        """
        print(f"creating question: {question_type.value}")
        if question_type == ReadingQuestionType.MC:
            structured_model = LLMModelType.Offline_GPT4o.value.with_structured_output(MCSQResponse, method="function_calling")
            if level == Difficulty.S1_S3 or level == Difficulty.S4_S6:
                llm_chain = MCSecondaryPrompt | structured_model
                mc_res = llm_chain.invoke({"section": section_text, "numOfQ": numOfQ})
                return json.loads(mc_res.json())  # returning a json obj containing a list {questions:[{'question':...,'type':'mcq',...},{...}]}
            elif level == Difficulty.P1_P3 or level == Difficulty.P4_P6:
                llm_chain = MCPrimaryPrompt | structured_model
                mc_res = llm_chain.invoke({"section": section_text, "numOfQ": numOfQ})
                return json.loads(mc_res.json())  # returning a json obj containing a list {questions:[{'question':...,'type':'mcq',...},{...}]}

        elif question_type == ReadingQuestionType.FITB:
            llm_chain1 = readingFitBPrompt1 | LLMModelType.Offline_GPT4o.value | str_parser
            llm_chain2 = readingFitBPrompt2 | LLMModelType.Offline_GPT4o.value | str_parser
            complete_chain = llm_chain1 | llm_chain2
            fitBString = complete_chain.invoke({"section": section_text, "numOfQ": int})
            return self.__parse_fitB(fitBString)  # returning a dict {"type": "fitB","question": [{"type": "text",...}]}

        elif question_type == ReadingQuestionType.SQ:
            structured_model = LLMModelType.Offline_GPT4o.value.with_structured_output(MCSQResponse, method="function_calling")
            if level == Difficulty.S1_S3 or level == Difficulty.S4_S6:
                llm_chain = SQSecondaryPrompt | structured_model
                sq_res = llm_chain.invoke({"section": section_text, "numOfQ": numOfQ})
                return json.loads(sq_res.json())  # returning a json obj containing a list {questions:[{'question':...,'type':'sq',...},{...}]}
            elif level == Difficulty.P1_P3 or level == Difficulty.P4_P6:
                llm_chain = SQPrimaryPrompt | structured_model
                sq_res = llm_chain.invoke({"section": section_text, "numOfQ": numOfQ})
                return json.loads(sq_res.json())  # returning a json obj containing a list {questions:[{'question':...,'type':'sq',...},{...}]}

        elif question_type == ReadingQuestionType.MCSQ_MIXED:
            structured_model = LLMModelType.Offline_GPT4o.value.with_structured_output(MCSQResponse, method="function_calling")
            if level == Difficulty.S1_S3 or level == Difficulty.S4_S6:
                llm_chain = MCSQSecondaryPrompt | structured_model
                mcsq_res = llm_chain.invoke({"section": section_text, "numOfQ": numOfQ})
                return json.loads(mcsq_res.json())  # returning a json obj containing a list {questions:[{'question':...,'type':'mcq',...},{...}]}
            else:
                llm_chain = MCSQPrimaryPrompt | structured_model
                try:
                    mcsq_res = llm_chain.invoke({"section": section_text, "numOfQ": numOfQ})
                except ValidationError:
                    raise ValidationError("The AI model failed to adhere to the json schema, please try again.")
                return json.loads(mcsq_res.json())  # returning a json obj containing a list {questions:[{'question':...,'type':'mcq',...},{...}]}

        elif question_type == ReadingQuestionType.TFNG:
            structured_model = LLMModelType.Offline_GPT4o.value.with_structured_output(TFNGResponse, method="function_calling")
            llm_chain = TFNGPrompt | structured_model
            tfng_response = llm_chain.invoke({"section": section_text, "numOfQ": numOfQ})
            statements = json.loads(tfng_response.json()).get("statements")
            tfng_json = {
                "type": ReadingQuestionType.TFNG.value,
                "instruction": "Decide the following statements are (True) F(False) or NG(Not given).",
                "statements": statements,
            }
            return tfng_json  # returning a dict {'type':tfng,'statements':[...]...}
        else:
            raise ValueError("Unknown question type")

    def __post_article_process(
        self,
        article: str,
        level: Difficulty,
        paragraph_array: list,
        hasFitB: bool = True,
        hasTFNG: bool = True,
        hasSQ: bool = True,
        totalNumOfQ: int = -1,
    ):
        """this function focus on generating questions after creating the article html and the paragraph array"""

        if level == Difficulty.P1_P3 or level == Difficulty.P4_P6:
            if hasSQ:
                numOfQ = af.get_numOfQ_for_whole_article(level=level, full_article=article)
                questions = self.create_question(
                    question_type=ReadingQuestionType.MCSQ_MIXED,
                    section_text=article,
                    numOfQ=numOfQ,
                    level=level,
                )
                return self.parse_question(
                    question_response=questions,
                    question_type=ReadingQuestionType.MCSQ_MIXED,
                )
            else:
                numOfQ = af.get_numOfQ_for_whole_article(level=level, full_article=article)
                questions = self.create_question(
                    question_type=ReadingQuestionType.MC,
                    section_text=article,
                    numOfQ=numOfQ,
                    level=level,
                )
                return self.parse_question(
                    question_response=questions,
                    question_type=ReadingQuestionType.MC,
                )
        else:
            # divide section and set numOfQ based on default setting
            section_array = self.__create_section(article=article, paragraph_array=paragraph_array, level=level)
            mcsq_numOfQ = totalNumOfQ - 2
            if not hasFitB:
                mcsq_numOfQ += 1
            if not hasTFNG:
                mcsq_numOfQ += 1

            if totalNumOfQ == -1:
                numOfQ_each_section = [af.get_numOfQ_by_word_count(af.count_words(af.join_paragraph(section))) for section in section_array]
            else:
                if (totalNumOfQ - 2) >= len(
                    section_array
                ):  # make sure the requested totalNumOfQ is not smaller than the number of sections, each section would have at least one question
                    numOfQ_each_section = af.distribute_questions(
                        total_numOfQ=(mcsq_numOfQ), section_num=len(section_array)
                    )  # simply distribute the questions evenly on all sections
                else:
                    numOfQ_each_section = [1] * len(section_array)  # each section has at least one question
            print(f"num of section {len(section_array)} numQ per section: {numOfQ_each_section[0]}")

            question_runnables = {
                f"section{index}": RunnableLambda(
                    lambda _, x=section, y=numOfQ_each_section[index]: self.create_question(
                        question_type=(ReadingQuestionType.MCSQ_MIXED if hasSQ else ReadingQuestionType.MC),  # check if user request SQ
                        section_text=af.join_paragraph(x),
                        numOfQ=y,
                        level=level,
                    )
                )
                for index, section in enumerate(section_array)
            }  # runnable for mcsq

            tfng_section_index, fitB_section_index = af.get_section_index_TFNG_FITB(
                len(section_array)
            )  # we allow overlapping of tfng/ fitB with some mcsq

            if hasTFNG:
                question_runnables[f"tfng"] = RunnableLambda(
                    lambda _, x=tfng_section_index: self.create_question(
                        question_type=ReadingQuestionType.TFNG,
                        section_text=af.join_paragraph(section_array[tfng_section_index]),
                        numOfQ=numOfQ_each_section[tfng_section_index],
                        level=level,
                    )
                )
            if hasFitB:
                question_runnables[f"fitB"] = RunnableLambda(
                    lambda _, x=fitB_section_index: self.create_question(
                        question_type=ReadingQuestionType.FITB,
                        section_text=af.join_paragraph(section_array[fitB_section_index]),
                        numOfQ=numOfQ_each_section[fitB_section_index],
                        level=level,
                    )
                )

            question_parallel = RunnableParallel(question_runnables)
            question_response = question_parallel.invoke(None)
            return self.__parse_parallel_question_response(
                question_response,
                tfng_section_index=tfng_section_index,
                fitB_section_index=fitB_section_index,
                section_array=section_array,
                hasFitB=hasFitB,
                hasTFNG=hasTFNG,
                singleThread=False,
            )

    def create_exercise_from_article(self, title: str, article: str, level: Difficulty, hasSQ: bool = False) -> dict:
        """create full exercise json from article given by user using default setting

        Reminder(default setting):
        For primary school students only mcsq will be created.
        """
        exercise_json = {
            "title": title,
            "instruction": "Please read the article and answer the questions.",
            "reading": "",
            "questions": [],
            "category": Category.READING.value,
        }
        paragraph_array = self.get_paragraph_array(article)
        article_html = self.create_html(paragraph_array=paragraph_array)
        exercise_json["reading"] = article_html
        if level == Difficulty.P1_P3 or level == Difficulty.P4_P6:
            exercise_json["questions"] = self.__post_article_process(article=article, level=level, paragraph_array=[], hasSQ=hasSQ)
            return exercise_json
        else:
            exercise_json["questions"] = self.__post_article_process(article=article, level=level, paragraph_array=paragraph_array)
            return exercise_json

    def create_exercise(
        self,
        theme: str,
        word_count: int,
        level: Difficulty,
        vocab_list: list[str] = ["none"],
    ) -> dict:
        """create full exercise json with ai generated article using default setting: number of paragraphs in section, number of question in each section etc...
        returning directly usable exercise dictionary

        Reminder(default setting):
        For primary school students only mcsq will be created.
        """
        exercise_json = {
            "title": "",
            "instruction": "Please read the article and answer the questions.",
            "reading": "",
            "questions": [],
            "category": Category.READING.value,
        }
        # generate article from outline
        outline = self.create_article_outline(theme=theme, word_count=word_count, level=level, vocab_list=vocab_list)
        article_response = self.create_article(
            outline=outline,
            theme=theme,
            word_count=word_count,
            level=level,
            vocab_list=vocab_list,
        )
        article = article_response["content"]
        exercise_json["title"] = article_response["title"]

        if level == Difficulty.P1_P3 or level == Difficulty.P4_P6:
            # generate only the article html. Paragraph array is not necessary here for short article.
            paragraph_array = self.get_paragraph_array(article)
            article_html = self.create_html(paragraph_array=paragraph_array)
            exercise_json["reading"] = article_html
            try:
                exercise_json["questions"] = self.__post_article_process(article=article, level=level, paragraph_array=[])
            except ValidationError:
                raise ValidationError("The AI model failed to adhere to the json schema, please try again.")
            return exercise_json
        else:
            # get paragraph array and generate html
            paragraph_array = self.get_paragraph_array(article)
            article_html = self.create_html(paragraph_array=paragraph_array)
            exercise_json["reading"] = article_html
            try:
                exercise_json["questions"] = self.__post_article_process(article=article, level=level, paragraph_array=paragraph_array)
            except ValidationError:
                raise ValidationError("The AI model failed to adhere to the json schema, please try again.")
            return exercise_json

    def __parse_parallel_question_response(
        self,
        question_response: dict,
        tfng_section_index: int,
        fitB_section_index: int,
        section_array: list[list[str]],
        hasFitB: bool = True,
        hasTFNG: bool = True,
        singleThread: bool = False,
    ):
        """this function helps rearrange all questions according to the order of the paragraph/section by:
        1. rearranging mcsq
        2. inserting tfng and fitB into appropriate section
        """
        if not singleThread:
            questions = []
            if hasTFNG:
                tfng = question_response.pop("tfng")
                tfng["paragraph"] = af.get_paragraph_index_str(section_array=section_array, section_index=tfng_section_index)
            if hasFitB:
                fitB = question_response.pop("fitB")
                fitB["paragraph"] = af.get_paragraph_index_str(section_array=section_array, section_index=fitB_section_index)

            sorted_keys = sorted(question_response.keys(), key=lambda x: int(x.replace("section", "")))
            ordered_list = [question_response[key] for key in sorted_keys]
            ordered_list = [question_obj["questions"] for question_obj in ordered_list]
            if hasTFNG:
                ordered_list.insert(
                    tfng_section_index,
                    [
                        {
                            "type": "instruction",
                            "text": f"Decide the following statements are (True) F(False) or NG(Not given) {tfng.pop('paragraph')}",
                        },
                        tfng,
                    ],
                )
            if hasFitB:
                ordered_list.insert(
                    fitB_section_index,
                    [
                        {
                            "type": "instruction",
                            "text": f"Please fill in the blanks with the suitable words or phrases {fitB.pop('paragraph')}",
                        },
                        fitB,
                    ],
                )

            questions = self.__flatten_2d_array(ordered_list)
            return questions

        else:
            questions = question_response["questions"]
            print(questions)
            return questions

    def parse_question(
        self,
        question_response: dict,
        question_type: ReadingQuestionType,
        section_array: list[list[str]] = [[]],
        tfng_or_fitB_section_index: int = -1,
        isWholeArticle: bool = False,
    ) -> list:
        """the return object from MCSQ Mixed is structured as follows:
        [{'question':...,'type':'mc',...},{...}]

        for other question type it returns a directly appendable question json object.

        this function remove the "questions" key convert it into just a list
        """
        if question_type == ReadingQuestionType.MC or question_type == ReadingQuestionType.MCSQ_MIXED or question_type == ReadingQuestionType.SQ:
            return question_response["questions"]
        elif question_type == ReadingQuestionType.TFNG or question_type == ReadingQuestionType.FITB:
            if isWholeArticle:
                if question_type == ReadingQuestionType.FITB:
                    resp = [
                        {"type": "instruction", "text": "Please fill in the blanks with the suitable words or phrases according to the article."},
                        question_response,
                    ]
                    return resp
                else:
                    resp = [
                        {
                            "type": "instruction",
                            "text": "Decide the following statements are (True) F(False) or NG(Not given) based on the article.",
                        },
                        question_response,
                    ]
                    return resp
            else:
                paragraph = af.get_paragraph_index_str(
                    section_array=section_array,
                    section_index=tfng_or_fitB_section_index,
                )
                if question_type == ReadingQuestionType.FITB:
                    resp = [
                        {
                            "type": "instruction",
                            "text": f"Please fill in the blanks with the suitable words or phrases {paragraph}",
                        },
                        question_response,
                    ]
                    return resp
                elif question_type == ReadingQuestionType.TFNG:
                    resp = [
                        {
                            "type": "instruction",
                            "text": f"Decide the following statements are (True) F(False) or NG(Not given) {paragraph}",
                        },
                        question_response,
                    ]
                    return resp
        return question_response

    def __flatten_2d_array(self, array: list[list]) -> list:
        flattened = [item for sublist in array for item in sublist]
        return flattened

    def save_json_file(self, path: str, exercise_json: dict):
        """save the exercise json file.
        The file name would be a combination of title and the datetime at the moment
        reminder: path must have the suffix "\\" or "/"
        <yourpath>/
        """
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        title = re.sub(r"[^a-zA-Z0-9]", "_", exercise_json["title"])
        filepath = path + title + now + ".json"
        with open(filepath, "w") as fp:
            json.dump(exercise_json, fp)
            return filepath

    def mcq_text2pic(mcq_json_object: dict) -> dict:
        """pass a mcq and change all the options into graphics (for primary school reading)"""
        raise NotImplementedError("give me some time for this")

    def paraphrase_mcq_tfng(question_type: ReadingQuestionType, question_json_object: dict) -> str:
        """paraphrase the mcq question if the user found it too straightforward
        (basically asking AI to "regen" the question)
        """
        raise NotImplementedError("give me some time for this")

    def mc2sq(self, mcq_json_object: dict) -> dict:
        """pass a mcq and change to sq"""
        sq_question = mcq_json_object["question"]
        sq_answer = mcq_json_object["options"][mcq_json_object["answer"]]
        sq_json_obj = {"question": sq_question, "answer": sq_answer, "type": "sq"}
        return sq_json_obj

    def sq2mc(self, section_text: str, sq_json_object: dict) -> dict:
        structured_model = LLMModelType.Offline_GPT4o.value.with_structured_output(MCSQResponse, method="function_calling")
        llm_chain = SQ2MCPrompt | structured_model
        res = llm_chain.invoke({"section": section_text, "sq_content": json.dumps(sq_json_object)})
        res = json.loads(res.json())
        return res["questions"][0]

    def custom_create_exercise_fr_article(
        self,
        title: str,
        level: Difficulty,
        article: str,
        hasFitB: bool,
        hasTFNG: bool,
        hasSQ: bool,
        totalNumOfQ: int,
    ):
        """free customize numOfQ and question type, generate questions from a pre-defined article"""
        exercise_json = {
            "title": title,
            "instruction": "Please read the article and answer the questions.",
            "reading": "",
            "questions": [],
        }
        paragraph_array = self.get_paragraph_array(article)
        print(len(paragraph_array))
        art_text_w_pNum = af.join_paragraph(paragraph_array)
        article_html = self.create_html(paragraph_array=paragraph_array)
        exercise_json["reading"] = article_html
        mcsq_numOfQ = totalNumOfQ - 2 if totalNumOfQ > 2 else af.get_numOfQ_for_whole_article(level=level, full_article=art_text_w_pNum)

        if level == Difficulty.P1_P3 or level == Difficulty.P4_P6:
            word_count = af.count_words(art_text_w_pNum)
            questions = []
            if hasFitB:
                fitB_question_dict = self.create_question(
                    ReadingQuestionType.FITB,
                    section_text=art_text_w_pNum,
                    numOfQ=af.get_numOfQ_by_word_count(word_count),
                    level=level,
                )
                fitB_question = self.parse_question(
                    question_response=fitB_question_dict,
                    question_type=ReadingQuestionType.FITB,
                    isWholeArticle=True,
                )
                questions.extend(fitB_question)
            else:
                mcsq_numOfQ += 1
            if hasTFNG:
                tfng_question_dict = self.create_question(
                    ReadingQuestionType.TFNG,
                    section_text=art_text_w_pNum,
                    numOfQ=af.get_numOfQ_by_word_count(word_count),
                    level=level,
                )
                tfng_question = self.parse_question(
                    question_response=tfng_question_dict,
                    question_type=ReadingQuestionType.TFNG,
                    isWholeArticle=True,
                )
                questions.extend(tfng_question)
            else:
                mcsq_numOfQ += 1
            if hasSQ:
                mcsq_question_dict = self.create_question(
                    ReadingQuestionType.MCSQ_MIXED,
                    section_text=art_text_w_pNum,
                    numOfQ=mcsq_numOfQ,
                    level=level,
                )
                mcsq_question = self.parse_question(
                    question_response=mcsq_question_dict,
                    question_type=ReadingQuestionType.MCSQ_MIXED,
                )
            else:
                mcsq_question_dict = self.create_question(
                    ReadingQuestionType.MC,
                    section_text=art_text_w_pNum,
                    numOfQ=mcsq_numOfQ,
                    level=level,
                )
                mcsq_question = self.parse_question(
                    question_response=mcsq_question_dict,
                    question_type=ReadingQuestionType.MC,
                )
            questions.extend(mcsq_question)

            exercise_json["questions"] = questions
            exercise_json["category"] = Category.READING.value
            return exercise_json

        else:
            exercise_json["questions"] = self.__post_article_process(
                article=article,
                level=level,
                paragraph_array=paragraph_array,
                hasFitB=hasFitB,
                hasTFNG=hasTFNG,
                hasSQ=hasSQ,
                totalNumOfQ=totalNumOfQ,
            )
            exercise_json["category"] = Category.READING.value
            return exercise_json
