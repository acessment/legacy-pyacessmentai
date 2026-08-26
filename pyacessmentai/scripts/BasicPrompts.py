from itertools import chain
import random
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from pyacessmentai.question_class.PFRQuestion import PFRQuestion
from pyacessmentai.question_class.QuestionType import QuestionType

# from . import common_parser as cp
from .GraphicsSettings import GraphicsSettings
from .PromptTemplate import *
from .TensesType import TensesType
from .GraphicsGeneration import *
from .grammarJSON import insert_images
from .grammarJSON import to_exercise_json, hash_json
from .DefinedChatModel import DefinedChatModel
from typing import List, Callable, Any, Dict
import hashlib

# from .QuestionBank import QuestionBank
from enum import Enum
import json
from datetime import datetime
import re

from pyacessmentai.question_class.CategoryType import Category

json_parser = JsonOutputParser()
str_parser = StrOutputParser()


class PromptTemplate:
    ONE_BY_ONE_FITB = "Give {numOfQ} examples. Remarks: {remarks}. Theme for the examples:{theme}"
    REMARKS = """
    You may be given some wrong answers from students in remarks. Please consider those remarks customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.
    """


class JSONPrompt(Enum):
    __STANDARD_USER_PROMPT = "{result}"
    SYSTEM_PROMPT1 = """You are going to receive a set of exercises with indexes.
convert it to the json array format. Remove any number indexes.
Example:

Input: 
1. He does that intentionally.
2. I like eating apples.

Output:
["He does that intentionally.","I like eating apples."]"""
    SYSTEM_PROMPT2 = "You are going to receive a piece of text. Just put the whole string as a single item in a json array. output the array"

    SYSTEM_PROMPT3 = """You are going to receive a set of text in such format:
1. some text 
***other text***

2.
some text
***other text***

and so on....

Please reformat them into a json array. Simply put the whole string from each as a single item in a json array. Remove the number index.
Example:

["some text ***other text***", "some text ***some other text***"]"""

    SYSTEM_PROMPT4 = """You are a very accurate robot. You are going to receive a text that have two major parts: 
1. Examples
2. Options

Each part can have multiple items in it. Your job is to form a JSON Object with two json array named 'examples' and 'options'. Remove any number index.

INPUT demo:
Examples:
1. The dog barked ***loudly*** at the stranger.
2. She finished her homework ***quickly*** before dinner.

Options: loud, quick

OUTPUT demo:
{"examples":['The dog barked ***loudly*** at the stranger.', 'She finished her homework ***quickly*** before dinner.'], "options":['loud','quick']}

Output only the final json object."""

    ONE_BY_ONE_FITB = ChatPromptTemplate.from_messages(
        [SystemMessage(content=SYSTEM_PROMPT1), HumanMessagePromptTemplate.from_template(__STANDARD_USER_PROMPT)]
    )
    ARTICLE_FITB = ChatPromptTemplate.from_messages(
        [SystemMessage(content=SYSTEM_PROMPT2), HumanMessagePromptTemplate.from_template(__STANDARD_USER_PROMPT)]
    )
    SQ = ChatPromptTemplate.from_messages([SystemMessage(content=SYSTEM_PROMPT3), HumanMessagePromptTemplate.from_template(__STANDARD_USER_PROMPT)])
    SEL_FITB = ChatPromptTemplate.from_messages(
        [SystemMessage(content=SYSTEM_PROMPT4), HumanMessagePromptTemplate.from_template(__STANDARD_USER_PROMPT)]
    )


class BasicPrompts:
    def __init__(
        self,
        title: str,
        instruction: str,
        tags: List[str],
        question_type: QuestionType,
        exercise_type_id: int,
        graphics_setting: GraphicsSettings = GraphicsSettings.NO_GRAPHICS,
    ):
        self.title = title
        self.instruction = instruction
        self.tags = tags
        self.exercise_type_id = exercise_type_id
        self.question_type = question_type
        self.chains = []
        self.graphics_setting = graphics_setting
        self.question_num = 0

    def _parse_sel_fitB_raw_json(self, raw_exercise_json):
        options = raw_exercise_json.get("options")
        raw_exercise_json = raw_exercise_json.get("examples")
        return options, raw_exercise_json

    def add_chain(
        self, system_prompt: str, user_prompt: str, custom_model=None, model: DefinedChatModel = DefinedChatModel.GPT4oMini, isJson: bool = False
    ):
        if custom_model:
            model = custom_model
        else:
            model = model.value
        if isJson:
            parser = json_parser
        else:
            parser = str_parser
        grammar_prompt1 = ChatPromptTemplate.from_messages(
            [SystemMessage(content=system_prompt), HumanMessagePromptTemplate.from_template(user_prompt)]
        )
        llm_chain = grammar_prompt1 | model | parser
        self.chains.append(llm_chain)

    def add_chain_with_custom_parser(
        self,
        system_prompt: str,
        user_prompt: str,
        custom_model=None,
        model: DefinedChatModel = DefinedChatModel.GPT4oMini,
        custom_parser=None,
    ):
        if custom_model:
            model = custom_model
        else:
            model = model.value
        grammar_prompt1 = ChatPromptTemplate.from_messages(
            [SystemMessage(content=system_prompt), HumanMessagePromptTemplate.from_template(user_prompt)]
        )
        if custom_parser:
            llm_chain = grammar_prompt1 | model | custom_parser
        else:
            llm_chain = grammar_prompt1 | model
        self.chains.append(llm_chain)

    def add_custom_function(self, name: str, func: Callable[[Dict[str, Any]], Dict[str, Any]]):
        """
        Add a custom function as RunnableLambda to the chain.

        Args:
            name (str): The name of the function in the chain
            func (Callable): The function to add to the chain. Function should take a dictionary as input and return a dictionary.

        Returns:
            BasicPrompts: The instance for method chaining
        """
        runnable_function = RunnableLambda(func)
        self.chains.append(runnable_function)
        return self

    def build_chain(self):
        if self.question_type == QuestionType.PFR:
            return self.build_chain_with_runnable_passthrough()

        else:
            if len(self.chains) == 0:
                raise Exception("Please add at least one chain using add_chain function")

            # If there's only one chain, just return it
            if len(self.chains) == 1:
                return self.chains[0]

            # For multiple chains, we chain them together
            chain = self.chains[0]
            for next_chain in self.chains[1:]:
                chain = chain | next_chain

        return chain

    def build_chain_with_runnable_passthrough(self):
        """
        Builds the chain while ensuring all input parameters are preserved throughout the chain
        using RunnablePassthrough. This allows subsequent chains to access the initial input parameters.

        Returns:
            A runnable chain that preserves all input parameters
        """
        if len(self.chains) == 0:
            raise Exception("Please add at least one chain using add_chain function")

        # If there's only one chain, just return it
        if len(self.chains) == 1:
            return self.chains[0]

        # For multiple chains, use RunnablePassthrough to preserve inputs

        # Create a function to merge new outputs with original inputs
        def merge_with_inputs(outputs, inputs):
            """Merge chain outputs with original inputs, preserving both."""
            # If outputs is not a dictionary, wrap it
            if not isinstance(outputs, dict):
                outputs = {"result": outputs}  # always call for get("result")

            # Create a new dict with original inputs
            result = dict(inputs)

            # Update with new outputs (outputs take precedence)
            result.update(outputs)

            return result

        # Start with the first chain
        first_chain = self.chains[0]

        # Create a chain that will:
        # 1. Pass the original inputs to the first chain
        # 2. Take the output and merge it with the original inputs
        chain = (
            RunnablePassthrough()
            | {"outputs": first_chain, "inputs": RunnablePassthrough()}
            | (lambda x: merge_with_inputs(x["outputs"], x["inputs"]))
        )

        # For each subsequent chain, we preserve inputs in the same way
        for next_chain in self.chains[1:]:
            chain = chain | {"outputs": next_chain, "inputs": RunnablePassthrough()} | (lambda x: merge_with_inputs(x["outputs"], x["inputs"]))

        return chain

    def add_json_chain(self, json_type):
        json_chain = json_type.value | DefinedChatModel.GPT4oMini.value | json_parser
        self.chains.append(json_chain)

    def full_exercise_dict(self, raw_exercise_json, haveExamples: bool = False):
        options = []
        if self.question_type is QuestionType.SEL_FITB:
            # extract options and examples aka questions from raw_exercise_json
            options = raw_exercise_json.get("options")
            random.shuffle(options)  # shuffling options so that it wont give hints to students
            raw_exercise_json = raw_exercise_json.get("examples")

        if self.question_type is QuestionType.PFR:
            pfr_question = PFRQuestion.from_json(raw_exercise_json)
            if haveExamples:
                pfr_question.set_examples(2)
            exercise_json = [pfr_question.to_dict()]
        else:
            if haveExamples:
                exercise_json = to_exercise_json(
                    question_type=self.question_type, raw_exercise_json=raw_exercise_json, examples_num=2
                )  # 2 examples per exercise
            else:
                exercise_json = to_exercise_json(question_type=self.question_type, raw_exercise_json=raw_exercise_json)
                if not self.graphics_setting == GraphicsSettings.NO_GRAPHICS:
                    image_base64_list = generate_graphics(raw_exercise_json)
                    exercise_json = insert_images(exercise_json, image_base64_list)
        # SHOWCASE WHEN OPTIONS ARE INSIDE THE QUESTIONS ARRAY
        # if len(options) > 0:
        #     options_obj = {"type":"options", "options": options}
        #     exercise_json.insert(0, options_obj)

        print(exercise_json)

        exercise_dict = {
            "title": self.title,
            "instruction": self.instruction,
            "tags": self.tags,
            "reading": "",  # template required, can be removed later
            "options": options,  # options for sel_fitB
            "questions": exercise_json,
            "questions_str": "\n".join(raw_exercise_json) if self.question_type != QuestionType.PFR else "",
            "exercise_id": "",
            "category": Category.GRAMMAR.value,
            "prompt": f"please generate a grammar {self.question_type.to_full_string()} exercise about {self.title}.",
        }
        exercise_hash = hash_json(exercise_dict)
        exercise_dict["exercise_id"] = exercise_hash  # adding hash as exercise_id
        return exercise_dict

    def build_chain_and_invoke(
        self,
        tenses: list[TensesType] = [TensesType.ANY_TENSES],
        word_count: int = 150,
        theme: str = "",
        remarks: str = "none",
        numOfQ: int = 10,
        grammar_items: str = "spelling, adverbs/adjectives, tenses, prepositions, articles",
    ):
        print("this function is deprecated and is only for debug purposes, will be removed in the future")
        tenses = [tense.value for tense in tenses]
        tenses = ", ".join(tenses)
        exercise_chain = self.build_chain()
        print("invoking chain")
        result = exercise_chain.invoke(
            {"numOfQ": numOfQ, "theme": theme, "remarks": remarks, "tenses": tenses, "word_count": word_count, "grammar_items": grammar_items}
        )
        return result

    def shuffle_parser(self, chain_result):
        if not (self.question_type == QuestionType.SEL_FITB or self.question_type == QuestionType.ARTICLE_FITB):

            def remove_numbering(text):
                # Use regex to match and remove the pattern of <number>.
                return re.sub(r"^\d+\.\s*", "", text)

            chain_result = [remove_numbering(question) for question in chain_result]
            random.shuffle(chain_result)
            chain_result = [f"{index+1}. {question}" for index, question in enumerate(chain_result)]
            return chain_result
        else:
            return chain_result

    def gen_save_json_file(self, path: str, raw_exercise_json, haveExamples: bool = False):
        exercise_dict = self.full_exercise_dict(raw_exercise_json=raw_exercise_json, haveExamples=haveExamples)
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        title = re.sub(r"[^a-zA-Z0-9]", "_", self.title)
        filepath = path + title + now + ".json"
        with open(filepath, "w") as fp:
            json.dump(exercise_dict, fp)
            return filepath

    # def gen_save_json_and_update_database(self, path:str, raw_exercise_json):
    #     qb = QuestionBank()
    #     exercise_id = qb.get_max_question_id() + 1
    #     filepath = self.gen_save_json_file(path=path, raw_exercise_json=raw_exercise_json, exercise_id=exercise_id)
    #     exercise_dict = self.full_exercise_dict(raw_exercise_json=raw_exercise_json, exercise_id=exercise_id)
    #     qb.save_full_exercise_to_mongo(exercise_dict=exercise_dict)
    #     return filepath
