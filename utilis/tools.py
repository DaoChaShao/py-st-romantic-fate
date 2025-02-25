#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/2/25 15:02
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   tools.py
# @Desc     :

from openai import OpenAI
from streamlit import (empty, header, selectbox, text_input, caption, slider,
                       sidebar, segmented_control, form, form_submit_button, number_input,
                       )
from time import perf_counter


def is_api_key(api_key: str) -> bool:
    """ Check the API key format.

    :param api_key: enter the API key of the deepseek
    :return: True if the API key is valid, False otherwise
    """
    if api_key.startswith("sk-") and len(api_key) == 35:
        return True
    return False


def model_caller(model: str, api_key: str, temperature: float, top_p: float, content: str, prompt: str) -> str:
    """ Call the Ollama model locally via requests package.

    :param model: the model name
    :param api_key: the API key for the model
    :param temperature: the randomness of the output
    :param top_p: the probability of the output
    :param content: the instruction of the system role
    :param prompt: the input from the user
    :return: the response from the model
    """
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": content},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        top_p=top_p,
        stream=False,
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content


class Timer(object):
    """ A simple timer class to measure the elapsed time.

    :param precision: the number of decimal places to round the elapsed time
    :param description: the description of the timer
    """

    def __init__(self, precision: int = 5, description: str = None):
        self._precision = precision
        self._description = description
        self._start = None
        self._end = None
        self._elapsed = None

    def __enter__(self):
        self._start = perf_counter()
        return self

    def __exit__(self, *args):
        self._end = perf_counter()
        self._elapsed = self._end - self._start

    def __repr__(self):
        if self._elapsed is None:
            return f"{self._description} elapsed: {self._elapsed:.{self._precision}f} seconds"
        else:
            return f"{self._description} is failed to count"


def parameters(message: empty) -> tuple[str, str, str, float, float]:
    """ Set the hyperparameters for the Ollama model.

    :param message: the message to display with empty placeholder of the streamlit
    :return: the model name, temperature, and top P
    """
    role: str = ""
    temp: float = 0.0
    temperature: float = 0.0
    top_p: float = 0.0

    with sidebar:
        header("Hyperparameters")

        options: list = ["deepseek-chat"]
        model: str = selectbox("Model", options, disabled=True, help="Select a model")
        caption(f"The model you selected is: **{model}**")

        api_key: str = text_input("API Key", placeholder="Enter your API key",
                                  type="password", max_chars=40, help="The API key for the model.")

        if api_key:
            if is_api_key(api_key):
                caption(f"The **{len(api_key)}**-digit API key is valid.")

                controls: list = ["General", "Math/Code", "Translation"]
                category: str = segmented_control(
                    "Role", controls, default=controls[0], selection_mode="single", disabled=True,
                    help="The instruction of the system role."
                )
                match category:
                    case "General":
                        role: str = "You are a professional Fortune Teller."
                        temp: float = 1.5
                    case "Math/Code":
                        role: str = "You are a helpful mathematician and programmer."
                        temp: float = 0.0
                    case "Translation":
                        role: str = "You are a translator between English and Chinese."
                        temp: float = 1.3

                temperature: int = slider("Temperature", 0.0, 2.0, temp, disabled=True,
                                          help="The randomness of the output.")
                caption(f"The temperature you selected is: **{temperature}**")

                top_p: int = slider("Top P", 0.0, 1.0, 0.9, disabled=True, help="The probability of the output.")
                caption(f"The top P you selected is: **{top_p}**")
            else:
                caption("The API key is invalid. Please enter a valid API key.")
        else:
            caption("Please enter the API key.")

        return model, api_key, role, temperature, top_p


def params_male():
    """ Get the parameters from male's information """
    with form("Male's Information", clear_on_submit=True, enter_to_submit=True):
        name: str = text_input("NAME", placeholder="Enter the name", help="Enter the name")
        caption(f"The name you entered is **{name}**")

        options = ["Male", "Female"]
        gender: str = selectbox("GENDER", options, help="Select the gender", index=0, disabled=True)
        caption(f"The gender you selected is **{gender}**")

        age: int = number_input("AGE", min_value=1, max_value=120, value=18, step=1, help="Enter the male's age")
        caption(f"The age you entered is **{age}**")

        location: str = text_input("LOCATION", placeholder="Enter the location", help="Enter the location")
        caption(f"The location you entered is **{location}**")

        submitted: bool = form_submit_button("Submit")

        if submitted:
            male = {
                "name": name,
                "gender": gender,
                "age": age,
                "location": location
            }
            return male
        return None


def params_female():
    """ Get the parameters from male's information """
    with form("Female's Information", clear_on_submit=True, enter_to_submit=True):
        name: str = text_input("NAME", placeholder="Enter the name", help="Enter the name")
        caption(f"The name you entered is **{name}**")

        options = ["Male", "Female"]
        gender: str = selectbox("GENDER", options, help="Select the gender", index=1, disabled=True)
        caption(f"The gender you selected is **{gender}**")

        age: int = number_input("AGE", min_value=1, max_value=120, value=18, step=1, help="Enter the male's age")
        caption(f"The age you entered is **{age}**")

        location: str = text_input("LOCATION", placeholder="Enter the location", help="Enter the location")
        caption(f"The location you entered is **{location}**")

        submitted: bool = form_submit_button("Submit")

        if submitted:
            male = {
                "name": name,
                "gender": gender,
                "age": age,
                "location": location
            }
            return male
        return None
