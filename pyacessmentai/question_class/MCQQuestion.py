from QuestionType import QuestionType
from BasicQuestion import BasicQuestion
import warnings


class MCQOption:
    def __init__(self, identifier: str, text: str):
        self.identifier = identifier
        self.text = text

    def to_dict(self):
        return {self.identifier: self.text}


class MCQQuestion(BasicQuestion):
    type_ = QuestionType.MCQ

    def __init__(
        self,
        question: str,
        answer: str,
        options: list[str],
        is_example: bool = False,
        is_correct: bool = None,
        explanation_text: str = None,
        student_answer: str = None,
    ):
        super().__init__(
            type=self.type_,
            is_example=is_example,
            is_correct=is_correct,
            explanation_text=explanation_text,
            student_answer=student_answer,
        )
        # TODO: In the MCQQuestion and MCQOption classes, now we assume every option identifier starts from 'a' and increments sequentially.
        # However this is not strictly defined in the JSON schema. If any bugs arise related to this, this file is the place to look.
        self.identifier_counter = "a"
        self.question = question
        self.answer = answer
        self.options = []
        for option in options:
            self.add_option(option)

    def add_option(self, text: str):
        """Add option to the end of the option list

        Args:
            text (str): The option text
        """
        option = MCQOption(self.identifier_counter, text)
        self.options.append(option)
        self.identifier_counter = chr(ord(self.identifier_counter) + 1)

    def remove_option(self, mcq_option: MCQOption):
        """remove the corresponding option from the list and reset the a,b,c,... identifier

        Args:
            mcq_option (MCQOption): the MCQOption to be removed
        """
        if mcq_option in self.options:
            self.options.remove(mcq_option)
            self.identifier_counter = (
                "a"  # Reset identifier counter and reassign identifiers
            )
            for option in self.options:
                option.identifier = self.identifier_counter
                self.identifier_counter = chr(ord(self.identifier_counter) + 1)

    def change_option_order(self, mcq_option: MCQOption, order_index: int):
        """Change the order of the mcq_option.

        Args:
            mcq_option (MCQOption): the target mcq_option
            order_index (int): 0 corresponds to 'a', 1 corresponds to 'b'...etc.
        """
        if mcq_option in self.options and 0 <= order_index < len(self.options):
            self.options.remove(mcq_option)
            self.options.insert(order_index, mcq_option)
            self.identifier_counter = "a"
            update_answer = False
            for option in self.options:
                if (
                    option.identifier.lower().strip() == self.answer.lower().strip()
                    and not update_answer
                ):
                    self.answer = self.identifier_counter.upper()
                    update_answer = True
                option.identifier = self.identifier_counter
                self.identifier_counter = chr(ord(self.identifier_counter) + 1)
        else:
            warnings.warn(
                f"Invalid order index {order_index} for option {mcq_option.identifier}: {mcq_option.text}, or option not in the list."
            )

    def to_dict(self):
        question_dict = super().to_dict()
        question_dict["question"] = self.question

        # Note that dictionaries are ordered in Python 3.7+
        question_dict["options"] = {
            option.identifier: option.text for option in self.options
        }
        question_dict["answer"] = self.answer
        return question_dict

    @classmethod
    def from_question_dict(cls, question_dict: dict) -> "MCQQuestion":
        """
        Create MCQQuestion instance from the given json.
        """
        options = list(question_dict["options"].values())
        return cls(
            is_example=question_dict.get("is_example", False),
            is_correct=question_dict.get(
                "is_correct", None
            ),  # fields corresponding to marking are default none
            answer=question_dict["answer"],
            options=options,
            question=question_dict["question"],
            explanation_text=question_dict.get(
                "explanation_text", None
            ),  # fields corresponding to marking are default none
            student_answer=question_dict.get("student_answer", None),
        )  # fields corresponding to marking are default none
