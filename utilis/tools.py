#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/2/25 15:02
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   tools.py
# @Desc     :

from datetime import datetime, date
from ollama import chat
from ollama import ChatResponse
from openai import OpenAI
from re import sub, DOTALL
from streamlit import (header, selectbox, text_input, caption, slider,
                       sidebar, segmented_control, form, form_submit_button, columns, subheader,
                       date_input, time_input, multiselect, session_state)
from time import perf_counter


def is_api_key(api_key: str) -> bool:
    """ Check the API key format.

    :param api_key: enter the API key of the deepseek
    :return: True if the API key is valid, False otherwise
    """
    if api_key.startswith("sk-") and len(api_key) == 35:
        return True
    return False


def model_deepseek(model: str, api_key: str, temperature: float, top_p: float, content: str, prompt: str) -> str:
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


def text_suber(text: str) -> str:
    """ Remove the special characters from the text.

    :param text: the text to be processed
    :return: the text without special characters
    """
    return sub(r"<think>.*?</think>", "", text, flags=DOTALL)


def model_ollama(content: str, prompt: str):
    response: ChatResponse = chat(
        model="deepseek-r1:8b",
        messages=[
            {
                "role": "system",
                "content": content,
            }, {
                "role": "user",
                "content": prompt,
            }],
        stream=False,
    )
    result = text_suber(response["message"]["content"])
    print(result)
    return result


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
        print(f"{self._description} started.")
        return self

    def __exit__(self, *args):
        self._end = perf_counter()
        self._elapsed = self._end - self._start

    def __repr__(self):
        if self._elapsed is not None:
            return f"{self._description} elapsed: {self._elapsed:.{self._precision}f} seconds"
        else:
            return f"{self._description} is failed to count"


def parameters() -> tuple[str, str, str, float, float, str, list[str]]:
    """ Set the hyperparameters for the Ollama model.

    :return: the model name, temperature, and top P
    """
    role: str = ""
    temp: float = 0.0
    temperature: float = 0.0
    top_p: float = 0.0
    language: str = ""
    methods: list[str] = []

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

                langs: list = ["English", "Chinese"]
                language: str = selectbox("Language", langs, index=1, disabled=False,
                                          help="Select the language used in the conversation.")
                caption(f"The language you selected is: **{language}**")

                multi: list = [
                    "生辰八字合婚",
                    "紫微斗数合婚",
                    "奇门遁甲合婚",
                    "姓名笔画合婚",
                ]
                methods: list = multiselect("Divine Method", multi, default=None, max_selections=None,
                                            help="Select the divine method you want to use.")
                caption(f"You select **{len(methods)}** divine methods.")
            else:
                caption("The API key is invalid. Please enter a valid API key.")
        else:
            caption("Please enter the API key.")
        return model, api_key, role, temperature, top_p, language, methods


def params_male():
    """ Get the parameters from male's information

    :return the parameters of getting from male's information
    """
    with form("Male's Information", clear_on_submit=True, enter_to_submit=True):
        name: str = text_input("MALE's NAME", placeholder="Enter the name", help="Enter the name")
        caption(f"The name you entered is **{name}**")

        options = ["Male", "Female"]
        gender: str = selectbox("GENDER", options, help="Select the gender", index=0, disabled=True)
        caption(f"The gender you selected is **{gender}**")

        birth_date = date_input("The DATE OF MALE's BIRTH", value="today",
                                min_value=date(1925, 1, 1), max_value="today",
                                help="Enter the date of birth")
        caption(f"The date of male's birth is **{birth_date}**")

        birth_time = time_input("THE TIME OF MALE's BIRTH", value="now", help="Enter the time of birth")
        caption(f"The time of male's birth is **{birth_time}**")

        location: str = text_input("MALE's BIRTH LOCATION", placeholder="Enter the location", help="Enter the location")
        caption(f"The location you entered is **{location}**")

        submitted: bool = form_submit_button("Submit")

        if submitted:
            male = {
                "name": name,
                "gender": gender,
                "birth_data": birth_date.isoformat(),
                "birth_time": birth_time.isoformat(),
                "location": location
            }
            return male
        return None


def params_female():
    """ Get the parameters from male's information

    :return: the parameters of getting from female's information
    """
    with form("Female's Information", clear_on_submit=True, enter_to_submit=True):
        name: str = text_input("FEMALE's NAME", placeholder="Enter the name", help="Enter the name")
        caption(f"The name you entered is **{name}**")

        options = ["Male", "Female"]
        gender: str = selectbox("GENDER", options, help="Select the gender", index=1, disabled=True)
        caption(f"The gender you selected is **{gender}**")

        birth_date = date_input("The DATE OF FEMALE's BIRTH", value="today",
                                min_value=date(1925, 1, 1), max_value="today",
                                help="Enter the date of birth")
        caption(f"The date of male's birth is **{birth_date}**")

        birth_time = time_input("THE TIME OF FEMALE's BIRTH", value="now", help="Enter the time of birth")
        caption(f"The time of male's birth is **{birth_time}**")

        location: str = text_input("FEMALE's BIRTH LOCATION", placeholder="Enter the location",
                                   help="Enter the location")
        caption(f"The location you entered is **{location}**")

        submitted: bool = form_submit_button("Submit")

        if submitted:
            male = {
                "name": name,
                "gender": gender,
                "birth_data": birth_date.isoformat(),
                "birth_time": birth_time.isoformat(),
                "location": location
            }
            return male
        return None


def params_couple():
    """ Get the parameters from male and female's information """
    with form("Couple's Information", border=True, clear_on_submit=False):
        col_male, col_female = columns(2)

        with col_male:
            subheader("Male's Information")
            name_male: str = text_input("MALE's NAME", value="许仙", placeholder="Enter the name",
                                        help="Enter the name")
            caption(f"The name you entered is **{name_male}**")
            birth_date_male = date_input("The DATE OF MALE's BIRTH", value="today",
                                         min_value=date(1925, 1, 1), max_value="today",
                                         help="Enter the date of birth")
            caption(f"The date of male's birth is **{birth_date_male}**")
            birth_time_male = time_input("THE TIME OF MALE's BIRTH", value="now", help="Enter the time of birth")
            caption(f"The time of male's birth is **{birth_time_male}**")
            location_male: str = text_input("MALE's BIRTH LOCATION", value="内蒙古", placeholder="Enter the location",
                                            help="Enter the location")
            caption(f"The location you entered is **{location_male}**")

        with col_female:
            subheader("Female's Information")
            name_female: str = text_input("FEMALE's NAME", value="白素贞", placeholder="Enter the name",
                                          help="Enter the name")
            caption(f"The name you entered is **{name_female}**")
            birth_date_female = date_input("The DATE OF FEMALE's BIRTH", value="today",
                                           min_value=date(1925, 1, 1), max_value="today",
                                           help="Enter the date of birth")
            caption(f"The date of male's birth is **{birth_date_female}**")
            birth_time_female = time_input("THE TIME OF FEMALE's BIRTH", value="now",
                                           help="Enter the time of birth")
            caption(f"The time of male's birth is **{birth_time_female}**")
            location_female: str = text_input("FEMALE's BIRTH LOCATION", value="北京", placeholder="Enter the location",
                                              help="Enter the location")
            caption(f"The location you entered is **{location_female}**")

        submitted = form_submit_button("Submit")

    if submitted:
        session_state["couple"] = {
            "male": {
                "name": name_male,
                "birth_date": birth_date_male.isoformat(),
                "birth_time": birth_time_male.isoformat(),
                "location": location_male
            },
            "female": {
                "name": name_female,
                "birth_date": birth_date_female.isoformat(),
                "birth_time": birth_time_female.isoformat(),
                "location": location_female
            }
        }
        return session_state["couple"]
    return None


def prompt_processor(role: str, male: dict, female: dict, command: str, language: str, methods: list[str]) -> str:
    """ Process the prompt based on the all information we get """
    context: str = (f"You have obtained information about the male, including {male}. "
                    f"ou have also obtained information about the female, including {female}.")

    words_limit: int = 150

    instructions: str = (f"As a professional Fortune Teller,"
                         f"you should strive to provide the best analysis with all the methods in {methods}, "
                         f"but should not mention their names explicitly. "
                         f"Your analysis should be based on {command} and {context}, "
                         f"and should be tailored for the couples. "
                         f"You should give logical and reasonable points and suggestions, "
                         f"depending on the number of methods used in {methods} "
                         f"Each paragraph should be limited to {words_limit} words.")

    formate: str = "Use Markdown format, and paragraph titles should be bold."

    constraints: str = (f"You can get today’s date and time information using {datetime.now()}.. "
                        f"If you find that either person in the couple is under 18, "
                        f"you should terminate the analysis process. "
                        f"Instead, you should provide suggestions encouraging them to focus on their studies and career， "
                        f" rather than romantic relationships.")

    prompt: str = (f"{role} "
                   f"{instructions} "
                   f"When giving suggestions, you should follow the {formate} and {constraints}. "
                   f"You should give the feedback in {language}.")
    return prompt
