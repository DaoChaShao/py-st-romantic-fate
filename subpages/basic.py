#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/2/25 15:03
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   basic.py
# @Desc     :

from streamlit import empty, sidebar, button

from utilis.tools import parameters, model_caller, Timer

empty_message: empty = empty()

model, api_key, sys_content, temperature, top_p = parameters(empty_message)

prompt = "What is the weather like today?"

if not api_key:
    empty_message.error("Please enter the API key.")
else:
    with sidebar:
        mml = button("Fate Tell", type="primary",
                     help="Click to tell the romantic fate based the information you provide.")

    if mml:
        with Timer(description="Fate Tell process") as timer:
            response = model_caller(model, api_key, temperature, top_p, sys_content, prompt)
