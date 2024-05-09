#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

from src.view.styling.light_mode.label import get_style
import src.view.constants as constants

from enum import Enum
import re

# class syntax
class Time_format(Enum):
    MONTHS = 1
    YEARS = 2

class Investment_intervall():
    def __init__(self, view, frame):
        self.frame = frame
        self.view = view
        self.view.keyboard_observable.subscribe(self)
        self.value_format = Time_format.YEARS

        self.time_frame = BoxLayout(orientation='vertical', size_hint=(.5, 1))
        label = Label(
                text='Time Investing',
                pos_hint=constants.center,
                size_hint=(1, .8),
                **get_style())
        self.time_frame.add_widget(label)
        self.textinput = TextInput(text='1 Year', multiline=False, size_hint =(1, 1))
        self.textinput.bind(on_text_validate=self.update_years)
        self.time_frame.add_widget(self.textinput)
        self.frame.add_widget(self.time_frame)

    def key_event(self, key, mouse_position):
        if self.time_frame.collide_point(mouse_position[0], mouse_position[1]):
            match key:
                case 273: #Up
                    self.increase_value(5)
                case 275:  #Right
                    self.increase_value(1)
                case 274: #Down
                    self.decrease_value(5)
                case 276: #Left
                    self.decrease_value(1)

    def decrease_value(self, decrease_amount=1):
        old_value = self.get_number_from_text()
        new_value = max(old_value - decrease_amount, 1)
        self.textinput._set_text(self.get_text_from_number(new_value))
        self.update_years(self.textinput)
    
    def increase_value(self, increase_amount=1):
        old_value = self.get_number_from_text()
        new_value = old_value + increase_amount
        self.textinput._set_text(self.get_text_from_number(new_value))
        self.update_years(self.textinput)

    def update_years(self, text_box):
        years = self.get_text_as_years()
        self.view.update_years_histogram_interval(years)

    def get_text_from_number(self, number):
        if self.value_format == Time_format.MONTHS:
            return str(number) + ' Months'
        if self.value_format == Time_format.YEARS:
            return str(number) + ' Years'
        else:
            return str(number)

    def get_number_from_text(self):
        text = self.textinput._get_text()

        if 'm' in text or 'M' in text:
            text = re.sub('\D', '', text) # remove non digits
            if text.isdigit():
                months = int(text)
                self.value_format = Time_format.MONTHS
                return months
            else:
                logging.error('"%r" is not a valid number', text)
                years = 1
                self.value_format = Time_format.YEARS
        elif 'y' in text or 'Y' in text:
            text = re.sub('\D', '', text) # remove non digits
            if text.isdigit():
                years = int(text)
                self.value_format = Time_format.YEARS
                return years
            else:
                logging.error('"%r" is not a valid number', text)
                years = 1
                self.value_format = Time_format.YEARS
        else:
            self.value_format = Time_format.YEARS
            if text.isdigit():
                years = int(text)
            else:
                logging.error('"%r" is not a valid number', text)
                years = 1

        return years

    def get_text_as_years(self):
        text = self.textinput._get_text()

        if 'm' in text or 'M' in text:
            text = re.sub('\D', '', text) # remove non digits
            if text.isdigit():
                monts = int(text)
                years = float(monts)/12
            else:
                logging.error('"%r" is not a valid number', text)
                years = 1
        elif 'y' in text or 'Y' in text:
            text = re.sub('\D', '', text) # remove non digits
            if text.isdigit():
                years = int(text)
            else:
                logging.error('"%r" is not a valid number', text)
                years = 1
        else:
            if text.isdigit():
                years = float(text)
            else:
                logging.error('"%r" is not a valid number', text)
                years = 1

        return years
