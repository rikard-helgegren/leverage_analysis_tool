#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging
import tkinter as tk


def setup_time_limiters(view, super_frame):
    frame_limiters = tk.Frame(super_frame, padx=5, pady=5)
    frame_limiters.pack()

    # Left text box with label
    frame_limiter_left = tk.Frame(frame_limiters, padx=5, pady=5)
    frame_limiter_left.pack(side=tk.LEFT)
    label_tame_from = tk.Label(frame_limiter_left, text='Start Date:')
    label_tame_from.pack(side=tk.TOP)
    view.text_box_left = Text_Box(frame_limiter_left, '')

    # Right text box with label
    frame_limiter_right = tk.Frame(frame_limiters, padx=5, pady=5)
    frame_limiter_right.pack(side=tk.LEFT)
    label_tame_to = tk.Label(frame_limiter_right, text='End Date:')
    label_tame_to.pack(side=tk.TOP)
    view.text_box_right = Text_Box(frame_limiter_right, '')

    def extract_data():
        time_from = view.text_box_left.get_text()
        time_to = view.text_box_right.get_text()
        time_to = standardize(time_to)
        time_from = standardize(time_from)
        view.update_time_limits(time_from, time_to)

    def standardize(time_string):
        time_string = time_string.replace('-', '')
        time_string = time_string.replace('/', '')
        time_string = time_string.replace('.', '')
        time_string = time_string.strip()

        # If empty do not use limits
        if time_string == "":
            return 0

        if len(time_string) < 5:  # If only year is set
            time_string = time_string + "0101"
        elif len(time_string) < 7:  # If only year and month is set
            time_string = time_string + "01"

        try:
            time_string = int(time_string)
        except:
            logging.error(" Input to limiters is in wrong format")
            # Standardizing failed do not use limits
            time_string = 0

        return time_string


    tk.Button(
        frame_limiters,
        text='Update Limits',
        command=extract_data
    ).pack(side=tk.BOTTOM)


class Text_Box:
    def __init__(self, frame, text):

        height = 1
        width = 10

        self.text_box = tk.Text(frame, height=height, width=width)
        self.text_box.insert("end", text)
        self.text_box.pack(side=tk.TOP)

    def get_text(self):
        return self.text_box.get(1.0, 'end')

    def set_text(self, text):
        self.text_box.delete(1.0, 'end')
        self.text_box.insert(1.0, text)
