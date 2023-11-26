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

from src.view.styling.light_mode.label import get_style

class Harvest_refill_strategy():
    def __init__(self, view):
        self.view = view
        self.view.keyboard_observable.subscribe(self)

        self.harvest_refill_frame = BoxLayout(size_hint=(.5, 0.2), pos_hint={'center_x': .5, 'center_y': .5})

        self.harvest_frame = BoxLayout(orientation='vertical', size_hint=(1, 1))
        self.harvest_frame.add_widget(Widget(size_hint=(1, .2))) #Space
        label = Label(text='Harvest', size_hint=(1, .8), **get_style())
        self.harvest_frame.add_widget(label)
        self.text_box_harvest_point = TextInput(text='150',
                                                multiline=False,
                                                size_hint =(1, .7))
        self.text_box_harvest_point.bind(on_text_validate=self.update_harvest_point)
        self.harvest_frame.add_widget(self.text_box_harvest_point)
        self.harvest_refill_frame.add_widget(self.harvest_frame)

        self.harvest_refill_frame.add_widget(Widget(size_hint=(.3, 1)))  #Space

        self.refill_frame = BoxLayout(orientation='vertical', size_hint=(1, 1))
        self.refill_frame.add_widget(Widget(size_hint=(1, .2))) #Space
        label = Label(text='Refill', size_hint=(1, .8), **get_style())
        self.refill_frame.add_widget(label)
        self.text_box_refill_point = TextInput(text='50',
                                               multiline=False,
                                               size_hint =(1, .7))
        self.text_box_refill_point.bind(on_text_validate=self.update_refill_point)
        self.refill_frame.add_widget(self.text_box_refill_point)
        self.harvest_refill_frame.add_widget(self.refill_frame)

    def get_frame(self):
        return self.harvest_refill_frame
    
    def key_event(self, key, mouse_position):
        if self.harvest_frame.collide_point(mouse_position[0], mouse_position[1]):
            match key:
                case 273: #Up
                    self.increase_harvest_value(10)
                case 275:  #Right
                    self.increase_harvest_value(1)
                case 274: #Down
                    self.decrease_harvest_value(10)
                case 276: #Left
                    self.decrease_harvest_value(1)
        elif self.refill_frame.collide_point(mouse_position[0], mouse_position[1]):
            match key:
                case 273: #Up
                    self.increase_refill_value(10)
                case 275:  #Right
                    self.increase_refill_value(1)
                case 274: #Down
                    self.decrease_refill_value(10)
                case 276: #Left
                    self.decrease_refill_value(1)

    def decrease_harvest_value(self, decrease_amount=1):
        old_value = int(self.text_box_harvest_point._get_text())
        new_value = max(old_value-decrease_amount, 100)
        self.text_box_harvest_point._set_text(str(new_value))
        self.update_harvest_point(self.text_box_harvest_point)
    
    def increase_harvest_value(self, increase_amount=1):
        old_value = int(self.text_box_harvest_point._get_text())
        new_value = old_value+increase_amount
        self.text_box_harvest_point._set_text(str(new_value))
        self.update_harvest_point(self.text_box_harvest_point)

    def decrease_refill_value(self, decrease_amount=1):
        old_value = int(self.text_box_refill_point._get_text())
        new_value = max(old_value-decrease_amount, 0)
        self.text_box_refill_point._set_text(str(new_value))
        self.update_refill_point(self.text_box_refill_point)
    
    def increase_refill_value(self, increase_amount=1):
        old_value = int(self.text_box_refill_point._get_text())
        new_value = min(old_value+increase_amount,99)
        self.text_box_refill_point._set_text(str(new_value))
        self.update_refill_point(self.text_box_refill_point)

    
    def update_harvest_point(self, text_box):
        harvest_point = text_box._get_text()
        if harvest_point.isdigit():
            self.view.update_harvest_point(int(harvest_point))
        else:
            logging.error('"%r" is not a number', harvest_point)

    def update_refill_point(self, text_box):
        refill_point = text_box._get_text()
        if refill_point.isdigit():
            self.view.update_refill_point(int(refill_point))
        else:
            logging.error('"%r" is not a number', refill_point)
    