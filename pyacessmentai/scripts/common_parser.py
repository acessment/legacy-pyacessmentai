import random
from .BasicPrompts import BasicPrompts
from .TensesType import TensesType
from pyacessmentai.question_class.QuestionType import QuestionType

import re
import ast


def exercise_parser(exercise: BasicPrompts, raw_exercise_json):
    from .tenses_parser import tenses_parser_for_dialogue

    if exercise.exercise_type_id == 39 and exercise.question_type:
        mixed_tenses_article = remove_tenses_used_text(raw_exercise_json[0])
        tenses_criteria = extract_tenses_from_text(raw_exercise_json[0])
        print(mixed_tenses_article)
        raw_exercise_json[0] = tenses_parser_for_dialogue(text=mixed_tenses_article, tenses_criteria=tenses_criteria)
        return raw_exercise_json
    elif exercise.question_type == QuestionType.PFR:
        return raw_exercise_json.get("result", [])
    else:
        return __shuffle_parser(exercise, raw_exercise_json)


def __shuffle_parser(exercise: BasicPrompts, chain_result):
    if not (
        exercise.question_type == QuestionType.SEL_FITB
        or exercise.question_type == QuestionType.ARTICLE_FITB
        or exercise.question_type == QuestionType.PFR
    ):

        def remove_numbering(text):
            # Use regex to match and remove the pattern of <number><.>
            return re.sub(r"^\d+\.\s*", "", text)

        chain_result = [remove_numbering(question) for question in chain_result]
        random.shuffle(chain_result)
        return chain_result
    else:
        return chain_result


def extract_tenses_from_text(text: str) -> list[TensesType]:
    text = text.lower()
    text = text.split("tenses used:")[1]
    print(text)
    list_tenses = ast.literal_eval(text)
    print(list_tenses)
    list_tenses = [TensesType(tenses_str) for tenses_str in list_tenses]
    return list_tenses


def remove_tenses_used_text(input_text):
    # Use regex to find "tenses used:" (case-insensitive) followed by any text until the end
    pattern = re.compile(r"\b(tenses used:).*$", re.IGNORECASE)
    # Substitute the found pattern with a period
    cleaned_text = re.sub(pattern, ".", input_text)
    return cleaned_text
