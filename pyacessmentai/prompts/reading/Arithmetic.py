import random
from .Difficulty import Difficulty


def count_words(text: str) -> int:
    words = text.split()
    return len(words)


def get_numOfQ_by_word_count(section_word_count: int) -> int:
    if section_word_count <= 50:
        return 3
    elif section_word_count > 50 and section_word_count <= 140:
        return 4
    elif section_word_count > 140 and section_word_count <= 250:
        return 5
    elif section_word_count > 250:
        return 6


def get_numOfQ_for_whole_article(level: Difficulty, full_article: str) -> int:
    if level == Difficulty.S4_S6:  # level == Difficulty.S1_S3
        raise ValueError(
            "This function is only for Primary school students cuz it assumes the article is short."
        )
    elif level == Difficulty.P1_P3 or level == Difficulty.P4_P6:
        article_word_count = count_words(full_article)
        if article_word_count <= 100:
            return 5
        elif article_word_count > 100 and article_word_count <= 150:
            return 7
        elif article_word_count > 150 and article_word_count <= 250:
            return 9
        elif article_word_count > 250:
            return 11


def get_section_size(article_word_count: int, num_paragraphs: int) -> int:
    """no grouping of paragraphs when the article is under 500 words"""
    if article_word_count > 450:
        if num_paragraphs <= 4:
            return 1
        elif num_paragraphs <= 10:
            return 2
        else:
            return 3
    else:
        return 1


def chunk_array(array: list, size: int) -> list[list[str]]:
    return [array[i : i + size] for i in range(0, len(array), size)]


def get_section_index_TFNG_FITB(num_sections: int) -> tuple[int, int]:
    """pick two random sections to generate TFNG and FITB"""
    if num_sections < 2:
        raise ValueError("invalid number of sections: must be greater than 1")

    num1 = random.randint(0, num_sections - 1)
    num2 = random.randint(0, num_sections - 1)

    while num1 == num2:
        num2 = random.randint(1, num_sections - 1)

    return num1, num2


def get_section_string_by_index(section_array: list[list[str]], index: int) -> str:
    return join_paragraph(section_array[index])


def join_paragraph(paragraph_array: list[str]) -> str:
    return "\n\n".join(paragraph_array)


def get_paragraph_index_str(section_array: list[list[str]], section_index: int, isFullArticle:bool=False) -> str:
    """returns a paragraph string
    example return: based on the paragraph 3,4,5
    if isFullArticle (which means the tfng or fitB is generated based on the full article)
    """
    if not isFullArticle:
        current_position = 0
        for i in range(section_index):
            current_position += len(section_array[i])
        subarray_positions = range(
            current_position + 1, current_position + len(section_array[section_index]) + 1
        )
        return "based on the paragraph " + ",".join(map(str, subarray_positions))
    else:
        return "based on the article"


def transform_options(options_list: list[str]) -> dict:
    options_dict = {}
    for option in options_list:
        key, value = option.split(".", 1)
        key = key.strip()
        value = value.strip()
        options_dict[key] = value
    return options_dict

def distribute_questions(total_numOfQ:int, section_num:int):
    """distributes questions evenly among sections, extra added to each section starting from the front"""
    numOfQ_each_section = [total_numOfQ // section_num] * section_num
    
    extra_question = total_numOfQ % section_num
    
    for i in range(extra_question):
        numOfQ_each_section[i] += 1
    
    return numOfQ_each_section
# def get_texts(paragraph_array:list[str], section_array:list[list[int]], index):
#     if index < 1 or index > len(section_array):
#         return "Invalid index"

#     indices = section_array[index - 1]
#     result = [paragraph_array[i - 1] for i in indices]
#     return "\n".join(result)
