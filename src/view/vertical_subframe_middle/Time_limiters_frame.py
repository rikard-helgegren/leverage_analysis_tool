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
from src.view.vertical_subframe_left.Investment_intervall import Investment_intervall
from datetime import datetime
from datetime import datetime, timedelta

class Time_limiters_frame():

    def __init__(self, view, super_frame):
        self.view = view
        self.view.keyboard_observable.subscribe(self)

        frame = BoxLayout(size_hint=(1, .15))


        frame.add_widget(Widget(size_hint=(.5, 1)))  # Space

        view.investment_intervall = Investment_intervall(view, frame)

        frame.add_widget(Widget(size_hint=(.5, 1)))  # Space

        self.start_date_frame = BoxLayout(orientation='vertical', size_hint=(1, 1))
        label = Label(text='Start Date', size_hint=(1, .8), **get_style())
        self.start_date_frame.add_widget(label)
        view.text_box_start_date = TextInput(text='', multiline=False, size_hint =(1, 1))
        view.text_box_start_date.bind(on_text_validate=self._extract_data)
        self.start_date_frame.add_widget(view.text_box_start_date)
        frame.add_widget(self.start_date_frame)

        self.in_between_dates_frame = BoxLayout(orientation='vertical', size_hint=(.6, 1))
        self.in_between_dates_frame.add_widget(Widget(size_hint=(.6, 1))) # Space
        frame.add_widget(self.in_between_dates_frame)

        self.end_date_frame = BoxLayout(orientation='vertical', size_hint=(1, 1))
        label = Label(text='End Date', size_hint=(1, .8), **get_style())
        self.end_date_frame.add_widget(label)
        view.text_box_end_date = TextInput(text='', multiline=False, size_hint =(1, 1))
        view.text_box_end_date.bind(on_text_validate=self._extract_data)
        self.end_date_frame.add_widget(view.text_box_end_date)
        frame.add_widget(self.end_date_frame)
        
        super_frame.add_widget(frame)

        frame.add_widget(Widget(size_hint=(.5, 1))) # Space

    def _extract_data(self, Text_box):
        self.extract_data()

    def extract_data(self):
        time_start = self.view.text_box_start_date._get_text()
        time_end = self.view.text_box_end_date._get_text()
        time_end = self.standardize(time_end)
        time_start = self.standardize(time_start)
        self.view.update_time_limits(time_start, time_end)
        self.set_date(time_start, self.view.text_box_start_date)
        self.set_date(time_end, self.view.text_box_end_date)

    def standardize(self, time_string):
        time_string = time_string.replace('-', '')
        time_string = time_string.replace('/', '')
        time_string = time_string.replace('.', '')
        time_string = time_string.strip()

        default_values = ["", "Start Date:", "End Date:"]

        # If empty do not use limits
        if time_string in default_values:
            return 0

        #TODO: Error prone
        if len(time_string) < 5:  # If only year is set
            time_string = time_string + "0101"
        elif len(time_string) < 7:  # If only year and month is set
            time_string = time_string + "01"

        try:
            time_string = int(time_string)
        except:
            logging.error("Input to limiters is in wrong format")
            # Standardizing failed do not use limits
            time_string = 0

        return time_string

    def key_event(self, key, mouse_position):
        text_boxes = []

        if self.start_date_frame.collide_point(mouse_position[0], mouse_position[1]):
            text_boxes.append(self.view.text_box_start_date)
        elif self.end_date_frame.collide_point(mouse_position[0], mouse_position[1]):
            text_boxes.append(self.view.text_box_end_date)
        elif self.in_between_dates_frame.collide_point(mouse_position[0], mouse_position[1]):
            text_boxes.append(self.view.text_box_start_date)
            text_boxes.append(self.view.text_box_end_date)

        for text_box in text_boxes:  
            match key:
                case 273: #Up
                    self._update_date(365,text_box)
                case 275:  #Right
                    self._update_date(1,text_box)
                case 274: #Down
                    self._update_date(-365, text_box)
                case 276: #Left
                    self._update_date(-1, text_box)
        
    def _update_date(self, update_amount, text_box):
        """ Only for key_event"""
        old_value = text_box._get_text()

        if old_value == '':
            logging.debug("No date value is set, a change by key is not possible")
        else:
            old_value = self.standardize(old_value)
            new_value = self.smooth_step(old_value, update_amount)
            self.set_date(new_value, text_box)
            self.extract_data()

    def smooth_step(self, date_int, update_amount):
        # Convert the integer to a string and then to a datetime object
        if update_amount == 365:
            date_int = date_int + 10000 #change year
            return date_int
        elif update_amount == -365:
            date_int = date_int - 10000 #change year
            return date_int
        else:
            date_str = str(date_int)
            date_obj = datetime.strptime(date_str, '%Y%m%d')
            new_date = date_obj + timedelta(days=update_amount)
            result_int = int(new_date.strftime('%Y%m%d'))
            return result_int

    def set_date(self, start_date, text_box):
        if start_date == 0:
            date_string = ''
        else:
            date_string = self.date_int_to_string(start_date)

        text_box._set_text(date_string)

    def date_int_to_string(self, date_integer):
        """Change format from 20220101 to 2022-01-01"""
        string_version = str(date_integer)

        string_version = string_version[0:4] + "-" + string_version[4:6] + "-" + string_version[6:8]
        return str(string_version)
    