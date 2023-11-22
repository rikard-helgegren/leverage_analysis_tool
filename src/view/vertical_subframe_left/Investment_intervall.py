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


from src.view.utils import make_text_black

class Investment_intervall():
    def __init__(self, view, frame):
        self.frame = frame
        self.view = view
        self.view.keyboard_observable.subscribe(self)

        self.time_frame = BoxLayout(orientation='vertical', size_hint=(1, 1))
        label = Label(
                text=make_text_black('Time Investing'),
                pos_hint={'center_x': .5, 'center_y': .5},
                markup = True, size_hint=(1, 1))
        self.time_frame.add_widget(label)
        self.textinput = TextInput(text='1', multiline=False, size_hint =(.8, .7))
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
        old_value = int(self.textinput._get_text())
        new_value = max(old_value-decrease_amount, 1)
        self.textinput._set_text(str(new_value))
        self.update_years(self.textinput)
    
    def increase_value(self, increase_amount=1):
        old_value = int(self.textinput._get_text())
        new_value = old_value + increase_amount
        self.textinput._set_text(str(new_value))
        self.update_years(self.textinput)

    def update_years(self, text_box):
        years = text_box._get_text()
        if years.isdigit():
            self.view.update_years_histogram_interval(int(years))
        else:
            logging.error('"%r" is not a number', years)
