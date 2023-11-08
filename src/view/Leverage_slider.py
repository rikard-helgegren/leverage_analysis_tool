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
from kivy.uix.slider import Slider

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from src.view.utils import make_text_black

class Leverage_slider():
    def __init__(self, view, frame):
        self.view = view
        sub_frame = GridLayout(size_hint=(1, .4), cols=1, )

        label = Label(text=make_text_black('Percent Leverage'),
        markup = True, size_hint=(1, 1))
        sub_frame.add_widget(label)

        sub_sub_frame = BoxLayout(size_hint=(1, .2) )
        self.slider = Slider(value=10, size_hint =(1, 1))
        self.slider.bind(value=self.on_slider_change)
        sub_sub_frame.add_widget(self.slider)

        self.slide_counter = Label(text=make_text_black('10'),
        markup = True, size_hint=(.1, 1))
        sub_sub_frame.add_widget(self.slide_counter)

        sub_frame.add_widget(sub_sub_frame)
        frame.add_widget(sub_frame)

    def decrease_value(self):
        old_value = self.slider.value
        new_value = max(old_value-1, 0)
        self.slider.value = new_value
    
    def increase_value(self):
        old_value = self.slider.value
        new_value = min(old_value+1, 100)
        self.slider.value = new_value

    def on_slider_change(self, instance, value):
        self.slide_counter.text=make_text_black(str(int(value)))
        self.view.update_amount_leverage(int(value))
