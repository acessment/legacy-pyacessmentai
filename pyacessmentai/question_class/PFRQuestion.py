import json
import os
from enum import Enum
from typing import List, Dict, Any, Optional, Union
from .QuestionType import QuestionType  # Assuming QuestionType is in the same directory


class PFRtype(Enum):
    TEXT = "text"
    CORRECT = "correct"
    WRONG = "wrong"


class PFRComp:
    def __init__(
        self,
        text: str,
        type: PFRtype,
    ):
        self.text = text
        self.type = type

    def to_dict(self):
        return {"type": self.type.value, "text": self.text}


class PFRQuestionComp(PFRComp):
    def __init__(
        self,
        type: PFRtype,
        text: str,
        is_example: bool = False,
        is_correct: bool = None,
        student_answer: str = None,
    ):
        super().__init__(text, type)
        self.is_example = is_example
        self.is_correct = is_correct
        self.student_answer = student_answer

    def to_dict(self):
        question_dict = super().to_dict()
        question_dict["is_example"] = self.is_example
        question_dict["is_correct"] = self.is_correct
        question_dict["student_answer"] = self.student_answer
        return question_dict


class PFRQuestion:
    type_ = QuestionType.PFR  # Assuming QuestionType has a PFR member
    
    def __init__(self, question: list[list[PFRComp]]):
        self.question = question
        self.type = self.type_
    
    @staticmethod
    def pfr_factory(single_pfr_component: dict) -> PFRComp:
        """
        This function helps to create the corresponding instance based on the given json.
        
        Args:
            single_pfr_component (dict): A component dictionary from the question list
        
        Returns:
            PFRComp: An instance of PFRComp or its subclass
        """
        component_copy = single_pfr_component.copy()  # Create a copy to avoid modifying the original
        pfr_type_str = component_copy.pop('type', None)
        
        # Map string type to enum
        pfr_type = None
        for t in PFRtype:
            if t.value == pfr_type_str:
                pfr_type = t
                break
                
        if pfr_type is None:
            raise ValueError(f"Unknown PFR component type: {pfr_type_str}")
            
        # Create the component instance based on type
        if pfr_type in [PFRtype.CORRECT, PFRtype.WRONG]:
            return PFRQuestionComp(
                type=pfr_type,
                text=component_copy.get('text', ''),
                is_example=component_copy.get('is_example', False),
                is_correct=component_copy.get('is_correct', None),
                student_answer=component_copy.get('student_answer', None)
            )
        else:  # TEXT type
            return PFRComp(
                text=component_copy.get('text', ''),
                type=pfr_type
            )
    
    @staticmethod
    def pfr_factory_multiple(pfr_components: list[list[dict]]) -> list[list[PFRComp]]:
        """
        Create all corresponding instances for all the items in the question components
        
        Args:
            pfr_components (list): List of lists of component dictionaries
            
        Returns:
            list: List of lists of PFRComp instances
        """
        pfr_component_instances = []
        for line in pfr_components:
            line_instances = []
            for comp in line:
                line_instances.append(PFRQuestion.pfr_factory(comp))
            pfr_component_instances.append(line_instances)
        return pfr_component_instances
    
    @classmethod
    def from_question_dict(cls, question_dict: dict):
        """
        Create a PFRQuestion instance from a question dictionary
        
        Args:
            question_dict (dict): Dictionary representation of a PFRQuestion
            
        Returns:
            PFRQuestion: An instance of PFRQuestion
        """
        question = PFRQuestion.pfr_factory_multiple(question_dict.get('question', []))
        return cls(question=question)
    
    @classmethod
    def from_json(cls, json_data: Union[str, List[List[Dict[str, Any]]]]):
        """
        Create a PFRQuestion instance from JSON data (either a file path or a parsed list of components)
        
        Args:
            json_data: Either a file path to a JSON file or a list of lists of component dictionaries
            
        Returns:
            PFRQuestion: An instance of PFRQuestion
        """
        components = []
        
        if isinstance(json_data, str):
            # Treat as file path
            with open(json_data, 'r') as f:
                components = json.load(f)
        else:
            # Already a parsed JSON list
            components = json_data
            
        pfr_components = PFRQuestion.pfr_factory_multiple(components)
        
        return cls(question=pfr_components)
    
    def to_dict(self):
        """
        Convert the PFRQuestion instance to a dictionary
        
        Returns:
            dict: Dictionary representation of the PFRQuestion
        """
        return {
            'type': self.type.value,
            'question': [[comp.to_dict() for comp in line] for line in self.question]
        }
    
    def get_components_by_type(self, comp_type: PFRtype) -> list[list[PFRComp]]:
        """
        Get all components of a specific type
        
        Args:
            comp_type (PFRtype): The type of components to retrieve
            
        Returns:
            list: List of lists of components matching the specified type
        """
        return [[comp for comp in line if comp.type == comp_type] for line in self.question]
    
    def get_wrong_components(self) -> list[list[PFRQuestionComp]]:
        """
        Get all wrong components in the question
        
        Returns:
            list: List of lists of PFRQuestionComp components with type WRONG
        """
        return [[comp for comp in line if isinstance(comp, PFRQuestionComp) and comp.type == PFRtype.WRONG] for line in self.question]
    
    def get_correct_components(self) -> list[list[PFRQuestionComp]]:
        """
        Get all correct components in the question
        
        Returns:
            list: List of lists of PFRQuestionComp components with type CORRECT
        """
        return [[comp for comp in line if isinstance(comp, PFRQuestionComp) and comp.type == PFRtype.CORRECT] for line in self.question]
    
    def get_summary(self) -> Dict[str, int]:
        """
        Get a summary of the components in this PFRQuestion
        
        Returns:
            Dict[str, int]: Summary statistics
        """
        total_components = sum(len(line) for line in self.question)
        text_components = sum(len(self.get_components_by_type(PFRtype.TEXT)))
        wrong_components = sum(len(self.get_wrong_components()))
        correct_components = sum(len(self.get_correct_components()))
        return {
            "total_components": total_components,
            "text_components": text_components,
            "wrong_components": wrong_components,
            "correct_components": correct_components
        }
    
    def __str__(self) -> str:
        """
        String representation of the PFRQuestion
        
        Returns:
            str: A readable string representation
        """
        summary = self.get_summary()
        return (f"PFRQuestion with {summary['total_components']} components: "
                f"{summary['text_components']} text, "
                f"{summary['wrong_components']} wrong, "
                f"{summary['correct_components']} correct")
    
    def set_examples(self, num_examples: int) -> None:
        """
        Sets a specified number of error-correction pairs as examples.
        
        Args:
            num_examples (int): The number of error-correction pairs to set as examples
            
        Returns:
            None
        """
        # Find all wrong-correct component pairs
        wrong_components = [comp for line in self.get_wrong_components() for comp in line]
        correct_components = [comp for line in self.get_correct_components() for comp in line]
        
        # Ensure we don't try to set more examples than we have pairs
        num_pairs = min(len(wrong_components), len(correct_components))
        num_examples_to_set = min(num_examples, num_pairs)
        
        # Set the specified number of pairs as examples
        for i in range(num_examples_to_set):
            wrong_components[i].is_example = True
            correct_components[i].is_example = True
        
        print(f"Set {num_examples_to_set} error-correction pairs as examples")


