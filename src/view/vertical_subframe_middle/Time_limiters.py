#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

from src.view.styling.light_mode.label import get_style

class Time_limiters():

    def __init__(self, view, frame):
        self.view = view

        sub_frame = BoxLayout(size_hint=(1, .15))
        sub_frame.add_widget(Widget(size_hint=(.8, 1)))

        start_date_frame = BoxLayout(orientation='vertical', size_hint=(1, 1))
        label = Label(text='Start Date', size_hint=(1, .8), **get_style())
        start_date_frame.add_widget(label)
        view.text_box_from_date = TextInput(text='', multiline=False, size_hint =(1, 1))
        view.text_box_from_date.bind(on_text_validate=self.extract_data)
        start_date_frame.add_widget(view.text_box_from_date)
        sub_frame.add_widget(start_date_frame)

        sub_frame.add_widget(Widget(size_hint=(.7, 1)))


        end_date_frame = BoxLayout(orientation='vertical', size_hint=(1, 1))
        label = Label(text='End Date', size_hint=(1, .8), **get_style())
        end_date_frame.add_widget(label)
        view.text_box_to_date = TextInput(text='', multiline=False, size_hint =(1, 1))
        view.text_box_to_date.bind(on_text_validate=self.extract_data)
        end_date_frame.add_widget(view.text_box_to_date)
        sub_frame.add_widget(end_date_frame)
        
        frame.add_widget(sub_frame)

        sub_frame.add_widget(Widget(size_hint=(.8, 1)))


    def extract_data(self, Text_box):
        time_from = self.view.text_box_from_date._get_text()
        time_to = self.view.text_box_to_date._get_text()
        time_to = self.standardize(time_to)
        time_from = self.standardize(time_from)
        self.view.update_time_limits(time_from, time_to)

    def standardize(self, time_string):
        time_string = time_string.replace('-', '')
        time_string = time_string.replace('/', '')
        time_string = time_string.replace('.', '')
        time_string = time_string.strip()

        default_values = ["", "Start Date:", "End Date:"]

        # If empty do not use limits
        if time_string in default_values:
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
