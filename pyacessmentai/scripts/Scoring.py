from pyacessmentai.question_class.PFRQuestion import PFRQuestion
def get_score(exercise_json: dict, isMarking:bool=False) -> tuple[int, list]:
    questions = exercise_json.get("questions")
    wrong_question_index = []
    question_index = 0
    for q in questions:
        if q["type"] == "fitB":
            for text_blank in q["question"]:
                if text_blank["type"] == "blank" and not text_blank.get("is_example",False):
                    if not text_blank.get("is_correct") and isMarking:
                        wrong_question_index.append(question_index)
                    question_index += 1
        else:
            if not q.get("is_example",False):
                if not q.get("is_correct") and isMarking:
                    wrong_question_index.append(question_index)
                question_index += 1
    return question_index, wrong_question_index

def count_question(exercise_json) -> int:
    questions = exercise_json.get("questions")
    print(questions)
    wrong_question_index = []
    question_index = 0
    for q in questions:
        if q.get("type","") == "fitB":
            for text_blank in q["question"]:
                if text_blank["type"] == "blank" and not text_blank.get(
                    "is_example", False
                ):
                    question_index += 1
        elif q.get("type","") == "pfr":
            # TODO: if in the future marking supports identifying underline, the number of questions may have to adjust
            pfr_question = PFRQuestion.from_question_dict(q)
            correct_pfr = pfr_question.get_correct_components()
            for line in correct_pfr:
                for pfr_comp in line:
                    if not pfr_comp.is_example:
                        question_index += 1
        else:
            if not q.get("is_example", False):
                question_index += 1
    return question_index
