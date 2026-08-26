ONE_BY_ONE_FITB = "Give {numOfQ} examples. Remarks: {remarks}. Theme for the examples:{theme}"
REMARKS = """
    You may be given some wrong answers from students in remarks. Please consider those remarks and customize your examples by generating something similar. You should tweak some of the wordings and make the new examples look different from the remarks. Do not keep the exact same wording.
"""
IMAGE_TRANSFORM_SYSTEM_PROMPT = """You are an image prompt writer. Your job is to transform the input text into a proper image prompt so that the image generation AI can better understand and produce accurate image.

The image style should be black and white.
The prompt should not contain extra information outside the context."""

IMAGE_TRANSFORM_USER_PROMPT = """{question}"""
    