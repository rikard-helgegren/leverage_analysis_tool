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

from src.view.styling.light_mode.label import get_style_no_font_size
from src.view.utils import is_number
import src.view.constants as constants


class Variance_strategy():
    def __init__(self, view):
        self.view = view
        self.view.keyboard_observable.subscribe(self)

        self.variance_frame = BoxLayout(size_hint=(.8, 0.2), pos_hint=constants.center)

        self.set_sample_size_variance_frame()

        self.variance_frame.add_widget(Widget(size_hint=(.3, 1)))  #Space

        self.set_sample_size_decisoin_frame()
        
        self.variance_frame.add_widget(Widget(size_hint=(.3, 1)))  #Space

        self.set_volatillaty_trigger_frame()


    def set_sample_size_variance_frame(self):
        self.sample_size_variance_frame = BoxLayout(orientation='vertical', size_hint=(1, 1))
        self.sample_size_variance_frame.add_widget(Widget(size_hint=(1, .2))) #Space
        label = Label(text='Sample size\nvariance',
                size_hint=(1, .8),
                **get_style_no_font_size())
        self.sample_size_variance_frame.add_widget(label)
        self.text_box_sample_size_variance = TextInput(text='10', multiline=False, size_hint =(1, .7))
        self.text_box_sample_size_variance.bind(on_text_validate=self.update_sample_size_variance)
        self.sample_size_variance_frame.add_widget(self.text_box_sample_size_variance)
        self.variance_frame.add_widget(self.sample_size_variance_frame)

    def set_sample_size_decisoin_frame(self):
        self.sample_size_decision_frame = BoxLayout(orientation='vertical', size_hint=(1, 1))
        self.sample_size_decision_frame.add_widget(Widget(size_hint=(1, .2))) #Space
        label = Label(text='Sample size\ndecision',
                size_hint=(1, .8),
                **get_style_no_font_size())
        self.sample_size_decision_frame.add_widget(label)
        self.text_box_sample_size_decision_point = TextInput(text='50', multiline=False, size_hint =(1, .7))
        self.text_box_sample_size_decision_point.bind(on_text_validate=self.update_sample_size_decision_point)
        self.sample_size_decision_frame.add_widget(self.text_box_sample_size_decision_point)
        self.variance_frame.add_widget(self.sample_size_decision_frame)

    def set_volatillaty_trigger_frame(self):
        self.volatillaty_trigger_frame = BoxLayout(orientation='vertical', size_hint=(1, 1))
        self.volatillaty_trigger_frame.add_widget(Widget(size_hint=(1, .2))) #Space
        label = Label(text='Volatillaty trigger',
                size_hint=(1, .8),
                **get_style_no_font_size())
        self.volatillaty_trigger_frame.add_widget(label)
        self.text_box_volatillaty_trigger_point = TextInput(text='0.010', multiline=False, size_hint =(1, .7))
        self.text_box_volatillaty_trigger_point.bind(on_text_validate=self.update_volatillaty_trigger)
        self.volatillaty_trigger_frame.add_widget(self.text_box_volatillaty_trigger_point)
        self.variance_frame.add_widget(self.volatillaty_trigger_frame)

    def get_frame(self):
        return self.variance_frame
    
    def key_event(self, key, mouse_position):
        if self.sample_size_variance_frame.collide_point(mouse_position[0], mouse_position[1]):
            match key:
                case 273: #Up
                    self.increase_sample_size_variance_value(10)
                case 275:  #Right
                    self.increase_sample_size_variance_value(1)
                case 274: #Down
                    self.decrease_sample_size_variance_value(10)
                case 276: #Left
                    self.decrease_sample_size_variance_value(1)
        elif self.sample_size_decision_frame.collide_point(mouse_position[0], mouse_position[1]):
            match key:
                case 273: #Up
                    self.increase_sample_size_decision_value(10)
                case 275:  #Right
                    self.increase_sample_size_decision_value(1)
                case 274: #Down
                    self.decrease_sample_size_decision_value(10)
                case 276: #Left
                    self.decrease_sample_size_decision_value(1)
        elif self.volatillaty_trigger_frame.collide_point(mouse_position[0], mouse_position[1]):
            match key:
                case 273: #Up
                    self.increase_volatillaty_trigger_value(0.01)
                case 275:  #Right
                    self.increase_volatillaty_trigger_value(0.001)
                case 274: #Down
                    self.decrease_volatillaty_trigger_value(0.01)
                case 276: #Left
                    self.decrease_volatillaty_trigger_value(0.001)

    def decrease_sample_size_variance_value(self, decrease_amount=1):
        old_value = int(self.text_box_sample_size_variance._get_text())
        if is_number(old_value):
            new_value = old_value-decrease_amount
            self.text_box_sample_size_variance._set_text(str(new_value))
            self.update_sample_size_variance(self.text_box_sample_size_variance)
        else:
            logging.error('"%r" is not a valid number', old_value)
       
    
    def increase_sample_size_variance_value(self, increase_amount=1):
        old_value = int(self.text_box_sample_size_variance._get_text())
        if is_number(old_value):
            new_value = old_value + increase_amount
            self.text_box_sample_size_variance._set_text(str(new_value))
            self.update_sample_size_variance(self.text_box_sample_size_variance)
        else:
            logging.error('"%r" is not a valid number', old_value)
        

    def decrease_sample_size_decision_value(self, decrease_amount=1):
        old_value = int(self.text_box_sample_size_decision_point._get_text())
        if is_number(old_value):
            new_value = max(old_value-decrease_amount, 0)
            self.text_box_sample_size_decision_point._set_text(str(new_value))
            self.update_sample_size_decision_point(self.text_box_sample_size_decision_point)
        else:
            logging.error('"%r" is not a valid number', old_value)
    
    def increase_sample_size_decision_value(self, increase_amount=1):
        old_value = int(self.text_box_sample_size_decision_point._get_text())
        if is_number(old_value):
            new_value = old_value + increase_amount
            self.text_box_sample_size_decision_point._set_text(str(new_value))
            self.update_sample_size_decision_point(self.text_box_sample_size_decision_point)
        else:
            logging.error('"%r" is not a valid number', old_value)

    def decrease_volatillaty_trigger_value(self, decrease_amount=1):
        old_value = float(self.text_box_volatillaty_trigger_point._get_text().replace(",","."))
        if is_number(old_value):
            new_value = round(max(old_value - decrease_amount, 0),3)
            self.text_box_volatillaty_trigger_point._set_text(str(new_value))
            self.update_volatillaty_trigger(self.text_box_volatillaty_trigger_point)
        else:
            logging.error('"%r" is not a valid number', old_value)
    
    def increase_volatillaty_trigger_value(self, increase_amount=1):
        old_value = float(self.text_box_volatillaty_trigger_point._get_text().replace(",","."))
        if is_number(old_value):
            new_value = round(old_value + increase_amount,3)
            self.text_box_volatillaty_trigger_point._set_text(str(new_value))
            self.update_volatillaty_trigger(self.text_box_volatillaty_trigger_point)
        else:
            logging.error('increase_volatillaty_trigger_value: "%r" is not a valid number', old_value)

    def set_sample_size_variance(self, new_value):
        if is_number(new_value):
            self.text_box_sample_size_variance._set_text(str(new_value))
        else:
            logging.error('set_sample_size_variance_value: "%r" is not a valid number', new_value)

    def set_volatillaty_trigger(self, new_value):
        if is_number(new_value):
            self.text_box_volatillaty_trigger_point._set_text(str(new_value))
        else:
            logging.error('set_volatillaty_trigger_value: "%r" is not a valid number', new_value)
    
    def set_sample_size_decision(self, new_value):
        if is_number(new_value):
            self.text_box_sample_size_decision_point._set_text(str(new_value))
        else:
            logging.error('set_sample_size_decision_value: "%r" is not a valid number', new_value)
        
    
    def update_sample_size_variance(self, text_box):
        sample_size_variance_point = text_box._get_text()
        if sample_size_variance_point.isdigit():
            self.view.update_variance_calc_sample_size(int(sample_size_variance_point))
        else:
            logging.error('"%r" is not a valid number', sample_size_variance_point)

    def update_sample_size_decision_point(self, text_box):
        sample_size_decision_point = text_box._get_text()
        if sample_size_decision_point.isdigit():
            self.view.update_volatility_strategie_sample_size(int(sample_size_decision_point))
        else:
            logging.error('"%r" is not a valid number', sample_size_decision_point)

    def update_volatillaty_trigger(self, text_box):
        volatillaty_trigger = text_box._get_text().replace(",",".")
        if is_number(volatillaty_trigger):
            self.view.update_volatility_strategie_level(float(volatillaty_trigger))
        else:
            logging.error('"%r" is not a valid number', volatillaty_trigger)
