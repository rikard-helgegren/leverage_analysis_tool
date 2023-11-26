#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

from src.view.utils import make_text_black


class Rebalance_strategy():
    def __init__(self, view):
        self.view = view
        self.view.keyboard_observable.subscribe(self)

        self.rebalance_time_frame = BoxLayout(
                orientation='vertical',
                size_hint=(0.4, 0.2),
                pos_hint={'center_x': .5, 'center_y': .5})
        self.rebalance_time_frame.add_widget(Widget(size_hint=(1, .2))) #Space
        label = Label(text=make_text_black('Rebalance period (Months)'),
                markup = True, size_hint=(1, .8))
        self.rebalance_time_frame.add_widget(label)
        self.text_box = TextInput(
                text='6',
                multiline=False,
                size_hint =(.3, 1),
                pos_hint={'center_x': .5, 'center_y': .5})
        self.text_box.bind(on_text_validate=self.update_rebalance_point)
        self.rebalance_time_frame.add_widget(self.text_box)

    def get_frame(self):
        return self.rebalance_time_frame
    
    def key_event(self, key, mouse_position):
        if self.rebalance_time_frame.collide_point(mouse_position[0], mouse_position[1]):
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
        old_value = int(self.text_box._get_text())
        new_value = max(old_value-decrease_amount, 1)
        self.text_box._set_text(str(new_value))
        self.update_rebalance_point(self.text_box)
    
    def increase_value(self, increase_amount=1):
        old_value = int(self.text_box._get_text())
        new_value = old_value+increase_amount
        self.text_box._set_text(str(new_value))
        self.update_rebalance_point(self.text_box)

    def update_rebalance_point(self, text_box):
        rebalnce_intervall = text_box._get_text()
        if rebalnce_intervall.isdigit():
            self.view.update_rebalnce_intervall(int(rebalnce_intervall))
        else:
            logging.error('"%r" is not a number', rebalnce_intervall)
