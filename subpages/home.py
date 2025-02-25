#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/2/25 15:02
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   home.py
# @Desc     :

from streamlit import title, divider, expander, caption, empty

title("Romantic Fate between Couples")
divider()
with expander("Introduction", expanded=True):
    caption("This is a simple introduction of the romantic fate between couples.")

empty_message: empty = empty()

empty_message.info("You can test your relationship with your partner by using the tools on the following pages.")
