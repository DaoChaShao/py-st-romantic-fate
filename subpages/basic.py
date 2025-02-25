#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/2/25 15:03
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   basic.py
# @Desc     :

from streamlit import empty, sidebar, button, columns, write

from utilis.tools import parameters, model_caller, Timer, params_male, params_female

empty_message: empty = empty()

model, api_key, sys_content, temperature, top_p = parameters(empty_message)

prompt = "What is the weather like today?"

left, right = columns(2)

if not api_key:
    empty_message.error("Please enter the API key.")
else:
    with left:
        male: dict = params_male()
        write(male)
    with right:
        female: dict = params_female()
        write(female)

    with sidebar:
        mml = button("Fate Tell", type="primary",
                     help="Click to tell the romantic fate based the information you provide.")

    if mml:
        with Timer(description="Fate Tell process") as timer:
            response = model_caller(model, api_key, temperature, top_p, sys_content, prompt)

        empty_message.info(timer)
