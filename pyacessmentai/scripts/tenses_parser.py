import re
import nltk
import spacy

nlp = spacy.load("en_core_web_sm")
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("wordnet")
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from .TensesType import TensesType

lemmatizer = WordNetLemmatizer()


def __get_pos_tags(text: str):
    # tokens = nltk.word_tokenize(text)
    # pos_tags = nltk.pos_tag(tokens)

    # print(modified_tags)
    # Process the sentence
    doc = nlp(text)
    print(doc)
    pos_tags = [(token.text, token.tag_) for token in doc]
    modified_tags = __tags_parser(pos_tags)

    return modified_tags


def __tags_parser(pos_tags: list[tuple[str, str]]):
    """
    To further replace certain words or punctuation for further processing since some of the words/punctuation
    are regarded as the same tag, which makes it harder to determine the tenses.

    Example:
    Will is often regarded as 'MD' same as other modal verb.
    apostrophe can be either has or is
    etc.
    """
    tag_replacements = {
        "will": "WILL",
        "’": "APOSTROPHE",
        "'": "APOSTROPHE",
        "is": "BEP",
        "am": "BEP",
        "are": "BEP",
        # "been": "BEEN",
        "have": "HAVE",
        "has": "HAS",
        "had": "HAD",
        "do": "DO",
        "does": "DOZ",
        "did": "DOD",
        "was": "BED",
        "were": "BED",
    }

    # List comprehension to apply the replacements
    modified_pos_tags = [(word, tag_replacements.get(word.lower(), tag)) for word, tag in pos_tags]
    return modified_pos_tags


def tense_detect(tagged_sentence: list[tuple[str, str]]):

    verb_tags = [
        "MD",
        "WILL",
        "BEP",
        "BEEN",
        "BED",
        "HAVE",
        "HAS",
        "HAD",
        "DO",
        "DOZ",
        "DOD",
        "VB",
        "VBP",
        "VBG",
        "VBN",
        "VBD",
        "VBZ",
        "TO",
    ]

    verb_phrase = []
    verb_phrase_index = []  # this is a list storing the index(referring to the tokenized tagged sentence) of the corresponding verb/auxiliary verb/to
    for index, item in enumerate(tagged_sentence):
        if item[1] in verb_tags:
            verb_phrase.append(item)
            verb_phrase_index.append(index)

    TENSES_RULES = r"""
                        past perfect continuous tense:{<HAD><VBN><VBG>+}
                        present perfect continuous tense:{<HAVE|HAS><VBN><VBG>+}
                        past perfect tense:{<HAD><VBN>+}
                        present continuous tense:{<BEP><VBG>+}
                        present perfect tense:{<HAVE|HAS><VBN|VBD>}
                        past continuous tense: {<BED><VBG>+}
                        future continuous tense:{<WILL><VBG>+}
                        simple future tense: {<WILL><VB>+}
                        simple past tense:{<VBD|DOD><DO|VB|VBP|HAVE>+}
                        simple present tense:{<DOZ|DO|VBP|VBZ><VB>+}
                        gerund:{<VBP|VBZ><VBG>+}
                        modal verb: {<MD><VB>+}
                        simple past tense:{<VBD|BED|DOD|HAD>}
                        simple present tense:{<DOZ|DO|VBP|VBZ|BEP|HAVE>}
                        to infinitive:{<TO><VB>}
                        gerund:{<VBG>}
                        to:{<TO>}
                        imperative: {<VB>}
                        single will: {<WILL>}
    """

    cp = nltk.RegexpParser(TENSES_RULES)
    result = cp.parse(verb_phrase)
    # display(result)  # for debug purposes

    return result, verb_phrase_index


def highlight_tenses(raw_text: str, tenses_list: list[TensesType]) -> str:
    """
    This function highlights the verb/auxiliary verb according to the given tenses in tenses_list and provide the corresponding bare infinitive in brackets.
    The output is a string that looks like this:
    I ***am*** (be) a boy.

    It is advised to first use sentence tokenizer to separate each dialogue and then call this function dialogue by dialogue because the final result will contain no line breaks.
    """
    tenses_list_value = [tenses_list[i].value for i in range(len(tenses_list))]
    tagged_sentence = __get_pos_tags(raw_text)

    tree, verb_phrase_index = tense_detect(tagged_sentence)

    tenses_and_verb_count = []

    for node in tree.subtrees():
        tenses_and_verb_count.append((node.label(), len(node)))
    tenses_and_verb_count.pop(0)

    counter = 0
    tagged_sentence = [
        list(item) if isinstance(item, tuple) else item for item in tagged_sentence
    ]  # I am directly modifying the values in the tagged_sentence which are tuple

    # to highlight the verb and adding bare infinitive
    for tenses, length in tenses_and_verb_count:
        if tenses in tenses_list_value:  # to know which to highlight and which not to
            for i in range(counter, counter + length):
                verb, tag = tagged_sentence[verb_phrase_index[i]]
                print(tenses)
                print(verb, tag)
                # !!should have changed the tenses into a proper enum first instead of comparing the value
                bare_infinitive = ""
                match tenses:
                    case TensesType.PRESENT_PERFECT.value:
                        if not (tag == "HAVE" or tag == "HAS"):
                            bare_infinitive = f"({lemmatizer.lemmatize(verb,'v')})"
                    case TensesType.SIMPLE_FUTURE.value:
                        if tag not in ["WILL"]:
                            bare_infinitive = f"({lemmatizer.lemmatize(verb,'v')})"
                    case TensesType.PAST_CONTINUOUS.value:
                        if tag not in ["BED"]:
                            bare_infinitive = f"({lemmatizer.lemmatize(verb,'v')})"
                    case TensesType.SIMPLE_PAST.value:
                        if length > 1:
                            if tag not in ["DOD"]:
                                bare_infinitive = f"({lemmatizer.lemmatize(verb,'v')})"
                        else:
                            bare_infinitive = f"({lemmatizer.lemmatize(verb,'v')})"
                    case TensesType.PRESENT_CONTINUOUS.value:
                        if tag not in ["BEP"]:
                            bare_infinitive = f"({lemmatizer.lemmatize(verb,'v')})"
                    case TensesType.PAST_PERFECT_CONTINUOUS.value:
                        if tag not in ["HAD", "VBN"]:
                            bare_infinitive = f"({lemmatizer.lemmatize(verb,'v')})"
                    case TensesType.PRESENT_PERFECT_CONTINUOUS.value:
                        if tag not in ["HAVE", "HAS", "VBN"]:
                            bare_infinitive = f"({lemmatizer.lemmatize(verb,'v')})"
                    case _:
                        bare_infinitive = f"({lemmatizer.lemmatize(verb,'v')})"
                # if tenses == TensesType.PRESENT_PERFECT:
                #     if tag == "HAV"
                tagged_sentence[verb_phrase_index[i]][0] = f"***{verb}*** {bare_infinitive}"
        counter += length

    raw_tokenized_sentence = [word for word, tag in tagged_sentence]
    detokenized_sentence = TreebankWordDetokenizer().detokenize(raw_tokenized_sentence)
    # print(raw_tokenized_sentence)
    # print(detokenized_sentence)
    detokenized_sentence = __fix_detokenize_error(detokenized_sentence)
    return __basic_clean_up(detokenized_sentence)


def __fix_detokenize_error(detokenized_sentence: str):
    detokenized_sentence = detokenized_sentence.replace(" .", ".")
    detokenized_sentence = detokenized_sentence.replace(" ’ ", "’")
    return detokenized_sentence


def __basic_clean_up(text: str):
    return text.replace("***  ***", " ")


def tenses_parser_for_dialogue(text: str, tenses_criteria: list[TensesType]):
    cleaned_dialogue = text.replace("\n", " ")
    # A really nice regex provided by chatGPT to extract each dialog as a single item
    dialogue_list = re.findall(r"\b[A-Z][a-z]+:.*?(?=\b[A-Z][a-z]+:|$)", cleaned_dialogue)
    highlighted_dialogue_list = []
    for dialogue_text in dialogue_list:
        highlighted_dialogue_list.append(highlight_tenses(dialogue_text, tenses_criteria))
    return "\n".join(highlighted_dialogue_list)


def tenses_parser_for_raw_text(text: str, tenses_criteria: list[TensesType]):
    return highlight_tenses(text, tenses_criteria)
