import random
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda
from .DefinedChatModel import DefinedChatModel
from pyacessmentai.scripts.PromptTemplate import *
import requests
import json

import base64
from PIL import Image
from io import BytesIO

str_parser = StrOutputParser()


# Function to compress image to black and white from base64 input
def compress_image_to_bw_base64(base64_str):
    # Decode the base64 string into bytes
    img_data = base64.b64decode(base64_str)

    # Open the image from the decoded bytes
    img = Image.open(BytesIO(img_data))

    # Convert image to black and white
    bw_img = img.convert("1")  # '1' for 1-bit pixels (black and white)

    # Save to a BytesIO object
    buffer = BytesIO()
    bw_img.save(buffer, format="JPEG", optimize=True)

    # Get the compressed image as base64
    bw_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return bw_base64


def __graphic_prompt_creator(content: list):
    prompt_list = [ChatPromptTemplate.from_messages([("system", IMAGE_TRANSFORM_SYSTEM_PROMPT), ("user", question)]) for question in content]

    chain_list = [prompt | DefinedChatModel.GPT4oMini.value | str_parser for prompt in prompt_list]
    print(prompt_list)
    chain_dict = {f"{i}": chain for i, chain in enumerate(chain_list)}
    return chain_dict


def __get_image(image_prompt: str):
    url = "https://api.ideogram.ai/generate"

    payload = {"image_request": {"prompt": image_prompt, "aspect_ratio": "ASPECT_1_1", "model": "V_2", "magic_prompt_option": "AUTO"}}
    headers = {
        "Api-Key": "aw293_Wmq8zzIi_wt0nlnbKPAQAI5TkrxEKLYdqww1hSC5_8DaR5R9pBLLheC3bLL7c5ka6hKTr-YkpI2JA7EA",
        "Content-Type": "application/json",
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    res_json = response.json()
    data = res_json["data"]
    image_url = data[0]["url"]
    return image_url


def __image_to_base64(url: str):
    # Send a GET request to the URL
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Convert the image content to base64
        image_base64 = base64.b64encode(response.content).decode("utf-8")
        bw_image_base64 = compress_image_to_bw_base64(image_base64)
        return bw_image_base64
    else:
        print(f"Error: Unable to fetch image. Status code: {response.status_code}")
        return None


def generate_graphics(raw_exercise_json: dict):
    graphics_URL = []
    parallel_chain = __graphic_prompt_creator(content=raw_exercise_json)
    runnable = RunnableParallel(parallel_chain)

    res = runnable.invoke({})
    print(type(res))
    image_prompt_list = [res[str(i)] for i in range(len(res))]
    print(image_prompt_list)

    image_gen_runnables = {
        f"{index}": RunnableLambda(lambda _, x=image_prompt: __get_image(image_prompt=x)) for index, image_prompt in enumerate(image_prompt_list)
    }
    image_gen_parallel = RunnableParallel(image_gen_runnables)
    images_URL = image_gen_parallel.invoke(None)
    images_URL_list = [images_URL[str(i)] for i in range(len(images_URL))]
    print(images_URL_list)
    images_base64_runnables = {f"{index}": RunnableLambda(lambda _, x=url: __image_to_base64(url=x)) for index, url in enumerate(images_URL_list)}
    images_base64_parallel = RunnableParallel(images_base64_runnables)

    images_base64_dict = images_base64_parallel.invoke(None)
    images_base64_list = [images_base64_dict[str(i)] for i in range(len(images_base64_dict))]

    return images_base64_list
