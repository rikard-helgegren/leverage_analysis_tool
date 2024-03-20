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

class Loan():
    def __init__(self, view, frame):
        logging.debug('Loan: __init__')
        self.view = view
        self.view.keyboard_observable.subscribe(self)
        self.frame = frame

        self.loan_frame = BoxLayout(orientation='vertical', size_hint=(1, 1))
        label = Label(
                text='Loan',
                pos_hint=constants.center,
                **get_style())
        self.loan_frame.add_widget(label)
        self.textinput = TextInput(
                text='0',
                multiline=False,
                size_hint =(.8, .7),
                pos_hint=constants.center)
        self.textinput.bind(on_text_validate=self.update_loan)
        self.loan_frame.add_widget(self.textinput)
        self.frame.add_widget(self.loan_frame)

    def key_event(self, key, mouse_position):
        logging.debug('Loan: key_event')
        if self.loan_frame.collide_point(mouse_position[0], mouse_position[1]):
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
        logging.debug('Loan: decrease_value')
        old_value = int(self.textinput._get_text())
        new_value = max(old_value - decrease_amount, 0)
        self.textinput._set_text(str(new_value))
        self.update_loan(self.textinput)
    
    def increase_value(self, increase_amount=1):
        logging.debug('Loan: increase_value')
        old_value = int(self.textinput._get_text())
        new_value = old_value + increase_amount
        self.textinput._set_text(str(new_value))
        self.update_loan(self.textinput)

    def update_loan(self, text_box):
        logging.debug('Loan: update_loan')
        loan = text_box._get_text()
        if loan.isdigit():
            self.view.update_loan(int(loan))
        else:
            logging.error('"%r" is not a number', loan)

    def set_loan(self, new_value):
        logging.debug('Loan: set_loan')
        value_converted_from_percent = int(new_value * 100)
        self.textinput._set_text(str(value_converted_from_percent))
        