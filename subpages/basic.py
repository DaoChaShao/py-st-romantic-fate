#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/2/25 15:03
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   basic.py
# @Desc     :

from streamlit import (empty, sidebar, button, columns, chat_input, spinner,
                       markdown, balloons, session_state, write, rerun)

from utilis.tools import (parameters, model_caller, Timer,
                          params_couple, prompt_processor)

empty_message: empty = empty()

model_name, api_key, sys_content, temperature, top_p, language, methods = parameters()

command: str = "Can you tell me how strong the romantic fate between us?"
chat_input(command, max_chars=100, disabled=True)

left, right = columns(2)

if not api_key:
    empty_message.error("Please enter the API key.")
else:
    if methods:
        if "couple" not in session_state or not session_state["couple"]:
            couple = params_couple()
            empty_message.warning("Please enter the information below.")
            if couple:
                session_state["couple"] = couple
                # write(session_state["couple"])
                rerun()
        else:
            male = session_state["couple"]["male"]
            female = session_state["couple"]["female"]

            with sidebar:
                llm = button("Fate Tell", type="primary",
                             help="Click to tell the romantic fate based on the information you provide.")

            if llm:
                # write(male, female)
                with spinner("Fate Tell is thinking...", show_time=True):
                    with Timer(description="Fate Tell process") as timer:
                        prompt: str = prompt_processor(sys_content, male, female, command, language, methods)
                        response: str = model_caller(model_name, api_key, temperature, top_p, sys_content, prompt)
                        markdown(response)
                        balloons()
                    empty_message.info(timer)
            else:
                empty_message.info("Please click the button to tell the romantic fate.")
    else:
        empty_message.warning("Please select the method.")
