import re
from datetime import datetime
def extract_from_asterisks(input_array):
    extracted_content = []
    for string in input_array:
        match = re.search(r'\*\*\*(.*?)\*\*\*', string)
        if match:
            extracted_content.append(match.group(1))
    return extracted_content

def split_asterisks(input_string):
    # Split the string by '***'
    parts = input_string.split('***')
    # Remove leading and trailing spaces from each part
    return [part.strip() for part in parts]

def get_id_from_formatted_student(formatted_student: str):
    pattern = r"ID:\s([a-f0-9]{24})"

    # Search for the ID in the input string
    match = re.search(pattern, formatted_student)
    return match.group(1)

def get_formatted_students(student_results: list[dict]) -> dict:
    formatted_student_options = {f"Phone no: {student.get('phone_number')} | Grade: {student.get('grades')} | Instance: {student.get('instance')}" : student.get('_id') for student in  student_results}
    return formatted_student_options

def get_formatted_hw_exid(homework_results: list[dict]) -> dict:
    """Returning a formatted dict with a formatted string and the exercise_id as key"""
    formatted_hw_options = {f'{index}. Date: {hw.get("assigned_date").strftime("%Y-%m-%d")} | Title: {hw.get("title")}' : hw.get('exercise_id') for index, hw in enumerate(homework_results)}
    return formatted_hw_options

def get_formatted_hw(homework_results: list[dict]) -> dict:
    """Returning a formatted dict with a formatted string and the combination of homework_id and exercise_id as key"""
    formatted_hw_options = {
        f'{index}. Date: {hw.get("assigned_date").strftime("%Y-%m-%d")} | Title: {hw.get("title")}': f'{hw.get("_id")}-{hw.get("exercise_id")}'
        for index, hw in enumerate(homework_results)
    }
    return formatted_hw_options

def get_exid_from_hwexid(key: str):
    """Return the exercise id from the string of homework_id-exercise_id
    """
    # Split the key by '-'
    parts = key.split('-')
    # The first part is homework_id, the second part is exercise_id
    return parts[1]
def get_hwid_from_hwexid(key: str):
    """Return the homework id from the string of homework_id-exercise_id
    """
    # Split the key by '-'
    parts = key.split('-')
    # The first part is homework_id, the second part is exercise_id
    return parts[0]

def get_formatted_performance(performance_results):
    formatted_perf_options = {
        f'{index}. Date: { perf.get("assigned_date").strftime("%Y-%m-%d") } | Title: {perf.get("marking_json").get("title")}': perf.get("_id")
        for index, perf in enumerate(performance_results)
    }
    return formatted_perf_options

def get_id_from_formatted_hw(formatted_hw):
    pass
