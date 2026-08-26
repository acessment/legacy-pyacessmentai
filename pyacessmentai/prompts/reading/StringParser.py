import re
def extract_from_asterisks(input_array):
    extracted_content = []
    for string in input_array:
        match = re.search(r'\*\*\*(.*?)\*\*\*', string)
        if match:
            extracted_content.append(match.group(1))
    return extracted_content

def split_asterisks(input_string:str):
    # Split the string by '***'
    parts = input_string.split('***')
    # Remove leading and trailing spaces from each part
    return [part.strip() for part in parts]
