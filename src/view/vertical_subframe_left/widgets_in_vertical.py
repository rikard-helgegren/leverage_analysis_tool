#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from src.view.vertical_subframe_left.Strategy_menue import Strategy_menue
from src.view.vertical_subframe_left.Leverage_slider import Leverage_slider
from src.view.vertical_subframe_left.Investment_intervall import Investment_intervall
from src.view.vertical_subframe_left.Loan import Loan
from src.view.utils import make_text_black

def setup_vertical_frame(view):
    vertical_frame = BoxLayout(orientation='vertical', padding=5, size_hint=(.6, 1))
    insert_space_top(vertical_frame)
    view.leverage_slider = Leverage_slider(view, vertical_frame)
    insert_check_box(view, vertical_frame)
    insert_time_and_loan(view, vertical_frame)
    view.strategy_meny = Strategy_menue(view, vertical_frame)
    insert_space_bott(vertical_frame)

    view.add_widget(vertical_frame)


def insert_space_top(frame):
    frame.add_widget(Widget(size_hint=(1, .5)))


def insert_space_bott(frame):
    frame.add_widget(Widget(size_hint=(1, .8)))
    

def insert_check_box(view, frame):
    def on_checkbox_active(check_box, state):
        view.update_fee_status(state)


    sub_frame = GridLayout(size_hint=(1, .4), cols=4)

    sub_frame.add_widget(Widget()) # empty space left

    checkbox = CheckBox(size_hint=(1, 1),active=True)
    checkbox.bind(active=on_checkbox_active)
    sub_frame.add_widget(checkbox)
    
    label = Label(text=make_text_black('Include fees'),
    markup = True)
    sub_frame.add_widget(label)

    sub_frame.add_widget(Widget()) # empty space right

    frame.add_widget(sub_frame)


def insert_time_and_loan(view, frame):

    sub_frame = BoxLayout(size_hint=(0.5, .2), pos_hint={'center_x': .5, 'center_y': .5})
    
    view.investment_intervall = Investment_intervall(view, sub_frame)

    sub_frame.add_widget(Widget())

    view.loan = Loan(view, sub_frame)
    
    frame.add_widget(sub_frame)
