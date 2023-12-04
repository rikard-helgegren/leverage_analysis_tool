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
from kivy.uix.widget import Widget

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from src.view.styling.light_mode.label import get_style


class Leverage_slider():
    def __init__(self, view, frame):
        self.view = view
        self.view.keyboard_observable.subscribe(self)
        self.sub_frame = GridLayout(size_hint=(1, .2), cols=1, )


        self.sub_frame.add_widget(Widget(size_hint=(.3, .4)))  #Space

        label = Label(text='Percent Leverage', size_hint=(1, .3), **get_style())
        self.sub_frame.add_widget(label)

        self.sub_frame.add_widget(Widget(size_hint=(.3, .15)))  #Space

        sub_sub_frame = BoxLayout(size_hint=(1, .1) )
        self.slider = Slider(value=10, size_hint =(1, 1))
        self.slider.bind(value=self.on_slider_change)
        sub_sub_frame.add_widget(self.slider)

        self.slide_counter = Label(text='10', size_hint=(.1, 1), **get_style())
        sub_sub_frame.add_widget(self.slide_counter)

        self.sub_frame.add_widget(sub_sub_frame)
        self.sub_frame.add_widget(Widget(size_hint=(.3, .1)))  #Space
        frame.add_widget(self.sub_frame)
    
    def key_event(self, key, mouse_position):
        if self.sub_frame.collide_point(mouse_position[0], mouse_position[1]):
            match key:
                case 273: #Up
                    self.increase_value(10)
                case 275:  #Right
                    self.increase_value(1)
                case 274: #Down
                    self.decrease_value(10)
                case 276: #Left
                    self.decrease_value(1)

    def decrease_value(self, decrease_amount=1):
        old_value = self.slider.value
        new_value = max(old_value - decrease_amount, 0)
        self.slider.value = new_value
    
    def increase_value(self, increase_amount=1):
        old_value = self.slider.value
        new_value = min(old_value + increase_amount, 100)
        self.slider.value = new_value

    def on_slider_change(self, instance, value):
        self.slide_counter.text=str(int(value))
        self.view.update_amount_leverage(int(value))
