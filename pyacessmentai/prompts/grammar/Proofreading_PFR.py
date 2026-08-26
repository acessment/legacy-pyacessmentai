from typing import Any, Dict
from pyacessmentai.generation.document import renderPDFdoc
from pyacessmentai.models.ProofreadingResponseSchema import PFRPassageResponse, PFRoutputList
from pyacessmentai.question_class.QuestionType import QuestionType
from pyacessmentai.scripts.BasicPrompts import BasicPrompts
from pyacessmentai.scripts.DefinedChatModel import DefinedChatModel
from pyacessmentai.scripts.pdf_preprocess import get_line_number
import re

PROOFREADING_SYSTEM_PROMPT1 = """
You are going to generate a grammar proofreading exercise. But before that, first generate a fully correct passage for me. The passage is written for Primary School students.

The passage should involves using various grammar items such as different tenses, prepositions, adverbs and adjectives etc.

Output in json format:
{
  "text": "The passage text"
}

output only the json
"""

PROOFREADING_USER_PROMPT1 = """
Generate a 130-word fully correct proofreading passage. The passage theme should be: {theme}. Specific focus on the following grammar items: {remarks}
"""

PROOFREADING_SYSTEM_PROMPT2 = """
You are going to generate a grammar proofreading exercise. You will receive a passage with line number information. Each line is explicitly defined, please respect the definition and the content of each line.

Your task is to generate one intentional grammar error for each single line and format them in a specific structure. The error should be exactly one word.
EACH LINE MUST HAVE AN ERROR. EACH LINE MUST HAVE ONLY ONE ERROR.

1. Choose from these error types:
   - Spelling mistakes
   - Tense errors
   - Preposition errors
   - Adjective/Adverb confusion
   - Plural/singular errors
   - Subject-verb agreement

EXAMPLE: 
line 1: The quick brown fox jumps over the
line 2: lazy dog. The dog is very sleepy. The

STEP1: decide the error for each line, use brackets to quote the original correct word, and use underscore to encapsulate the error word
line 1: The quick brown fox _jumping_ (jump) over the
line 2: lazy dog. The dog _am_ (is) very sleepy. The

STEP2: put each line with both error and the correct word as an item of an array, keep those underscores and brackets
["The quick brown fox _jumping_ (jump) over the","lazy dog. The dog _am_ (is) very sleepy. The"]
"""

PROOFREADING_USER_PROMPT2 = """
Here is the correct passage with line numbers:
{passage}

focusing on these grammar items: {remarks}

Format your response as specified in the instructions, and decide on the errors to introduce for each line.
"""


PFR_model = DefinedChatModel.GPT4oT08.value.with_structured_output(PFRoutputList)
PFR_passage_model = DefinedChatModel.GPT4o.value.with_structured_output(
    PFRPassageResponse
)


def create_proofreading_chain() -> BasicPrompts:
    """
    Create a complete chain for generating proofreading exercises.

    Args:
        theme: The theme for the passage
        grammar_items: Grammar items to focus on

    Returns:
        BasicPrompts: The configured chain
    """
    prompts = BasicPrompts(
        title=f"Proofreading Exercise",
        instruction="Find and correct the errors in the passage.",
        tags=["grammar", "proofreading"],
        question_type=QuestionType.PFR,
        exercise_type_id=1,
    )

    # Step 1: Generate a correct passage
    prompts.add_chain_with_custom_parser(
        system_prompt=PROOFREADING_SYSTEM_PROMPT1,
        user_prompt=PROOFREADING_USER_PROMPT1,
        custom_model=PFR_passage_model,
    )

    # Step 2: Custom function to get line number information using pdf_preprocess
    def get_line_info(res: PFRPassageResponse) -> Dict[str, Any]:
        """
        Use the PDF renderer and pdf_preprocess.get_line_number to extract line information.
        """
        # Extract the passage text from the structured output
        print(res)
        passage = res.get("result").text # remember singular result

        print("\n--- Generated Passage ---\n")
        print(passage)
        print("\n--- Getting line information ---")

        # Create test JSON for rendering
        test_json = [
            {
                "questions": [
                    {"type": "pfr", "question": [[{"type": "text", "text": passage}]],"isTesting":True}
                ]
            }
        ]

        doc = renderPDFdoc(test_json, isSolution=False, show_index=True)
        line_texts = get_line_number(doc, "pfr-article-div")

        # Format the passage with line numbers for the next step
        passage_with_lines = "\n".join(
            [f"Line {i+1}: {line}" for i, line in enumerate(line_texts)]
        )

        # Return the necessary information for the next step
        return {
            "passage": passage_with_lines,
        }

    def extract_parts(result):
        """
        Extract parts from PFRoutputList result for PFR questions using regex.
        
        Handles different possible structures of the result object.
        """
        # Extract errors array - handle both object and dictionary access patterns
        if hasattr(result, "get"):
            # Dictionary-like access
            result_obj = result.get("result", result)
        else:
            # Object access
            result_obj = result
            
        print(result_obj)
        
        lines = []
        # Handle different result formats
        if hasattr(result_obj, "lines"):
            lines = result_obj.lines
        elif isinstance(result_obj, dict) and "lines" in result_obj:
            lines = result_obj["lines"]
        
        parts_list = []
        
        # Process each line with marked errors (_wrong_) (correct)
        for line_text in lines:
            line_parts = []
            has_error_pair = False
            
            # Define regex pattern to match both wrong word and correct word patterns
            # _wrong_ (correct) pattern
            pattern = r'_(.*?)_\s*\((.*?)\)'
            
            # Split the line by the wrong-correct patterns
            segments = re.split(pattern, line_text)
            
            # Process segments and matches
            i = 0
            while i < len(segments):
                # Regular text segment
                if segments[i].strip():
                    line_parts.append({"type": "text", "text": segments[i]})
                
                # If we have a wrong-correct pair
                if i + 2 < len(segments):
                    # Wrong word segment
                    wrong_word = segments[i+1]
                    line_parts.append({"type": "wrong", "text": wrong_word})
                    
                    # Correct word segment
                    correct_word = segments[i+2]
                    line_parts.append({"type": "correct", "text": correct_word})
                    
                    has_error_pair = True  # Mark that we found an error pair
                    i += 2  # Skip the wrong and correct segments since we've processed them
                
                i += 1
            
            # Handle case where no matches were found
            if not line_parts:
                line_parts.append({"type": "text", "text": line_text})
                
            # If no error pair was found in this line, add a correct component with text "CORR"
            if not has_error_pair:
                line_parts.append({"type": "wrong", "text": ""})
                line_parts.append({"type": "correct", "text": "CORR"})
                
            parts_list.append(line_parts)
        
        print(f"Extracted {len(parts_list)} lines of parts")
        return parts_list

    prompts.add_custom_function("get_line_info", get_line_info)
    prompts.add_chain_with_custom_parser(
        system_prompt=PROOFREADING_SYSTEM_PROMPT2,
        user_prompt=PROOFREADING_USER_PROMPT2,
        custom_model=PFR_model,
    )
    prompts.add_custom_function("extract_parts", extract_parts)
    return prompts

Proofreading_exercise = create_proofreading_chain()
