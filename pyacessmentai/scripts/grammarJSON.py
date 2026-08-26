from enum import Enum
import json

from . import string_utils
import random
import re
from pyacessmentai.question_class.QuestionType import QuestionType
from datetime import datetime
import hashlib
    
def to_single_json_question(question_type:QuestionType, raw_single_qa):
    """
    Turning raw text into proper json schema according to each question type.
    """
    if question_type == QuestionType.SQ:
        pattern = r'\*\*\*(.*?)\*\*\*'
        match = re.search(pattern, raw_single_qa)
        json_question = {}
        if match:
                answer = match.group(1)
                remaining_text = re.sub(pattern, '', raw_single_qa).strip()
                json_question["type"] = question_type.json_type
                json_question["answer"] = answer
                json_question["question"] = remaining_text
        else:
            json_question["answer"] = None
            json_question["question"] = raw_single_qa
        return json_question
    elif question_type in [QuestionType.FITB,QuestionType.SEL_FITB,QuestionType.ARTICLE_FITB]:
        raw_question_array = string_utils.split_asterisks(raw_single_qa)
        fitb_question_array = []
        for key,raw_text in enumerate(raw_question_array):
            if key % 2 == 1:
                fitb_type = "blank" 
            else:
                fitb_type = "text"
            json_obj = {
                "type": fitb_type,
                "text": raw_text
            }
            fitb_question_array.append(json_obj)
        json_question = {
            "type": question_type.json_type,
            "question": fitb_question_array
        }
        return json_question
        
def to_exercise_json(question_type:QuestionType, raw_exercise_json:list, examples_num:int=0):
    """
    This function converts raw exercise json (raw results from openAI) to legit exercise json object following the schema.
    It also helps add examples if needed.
    """
    exercise_json = []
    for single_qa in raw_exercise_json:
        json_question = to_single_json_question(question_type=question_type, raw_single_qa=single_qa)
        exercise_json.append(json_question)
    return to_example(exercise_json, examples_num)

def shuffle_exercise(raw_exercise_json:list):
    shuffled_exercise = raw_exercise_json[:]
    shuffled_exercise = [remove_number_punctuation_combinations(q) for q in shuffled_exercise]
    random.shuffle(shuffled_exercise)
    return shuffled_exercise

def to_example(exercise_json:dict, examples_num:int) -> dict:
    """
    This function modifies the first <examples_num> of questions into examples by adding an extra true boolean field is_example
    """
    questions_modified = 0  # Counter for the number of blanks modified

    for question in exercise_json:
        if question['type'] == 'fitB':
            fitB_array = question['question'] # traverse to question field if it is fitB
            for item in fitB_array:
                if item['type'] == 'blank': # is_example should always stick with blank
                        item['is_example'] = questions_modified < examples_num # set is_example to true until it reaches the examples_num
                        questions_modified += 1
        else: # just simply add is_example if it is not fitB
                question['is_example'] = questions_modified < examples_num
                questions_modified += 1
    return exercise_json

def remove_number_punctuation_combinations(input_string:str):
    cleaned_string = re.sub(r'\b\d+\.\b', '', input_string)
    return cleaned_string

def insert_images(questions_json, images_base64_list):
    if len(questions_json) == len(images_base64_list):
        for index, question in enumerate(questions_json):
            question['images'] = [images_base64_list[index]]
        return questions_json
    else:
        raise ValueError(f"The number of images provided does not match the number of questions. Questions:{len(questions_json)} Images:{len(images_base64_list)}")
    
def hash_json(json_obj: dict):
    """
    This function calculates the hash of the exercise json based on the json content and the current datetime
    """
    # Add the current date and time to the JSON object
    json_obj["timestamp"] = datetime.now().isoformat()
    json_str = json.dumps(json_obj, sort_keys=True) # for consistent hashing
    json_bytes = json_str.encode('utf-8')
    hash_object = hashlib.sha256(json_bytes)
    hash_hex = hash_object.hexdigest()
    return hash_hex