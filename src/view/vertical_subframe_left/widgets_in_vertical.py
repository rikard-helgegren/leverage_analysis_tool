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

from src.view.vertical_subframe_left.Loan import Loan
from src.view.vertical_subframe_left.Strategy_menue import Strategy_menue
from src.view.vertical_subframe_left.Leverage_slider import Leverage_slider
from src.view.vertical_subframe_left.Investment_intervall import Investment_intervall
from src.view.vertical_subframe_left.Table_of_instruments import Table_of_instruments
from src.view.styling.light_mode.label import get_style
import src.view.constants as constants

def setup_vertical_frame(view):
    vertical_frame = BoxLayout(orientation='vertical', padding=5, size_hint=(.7, 1))

    vertical_sub_frame_top = BoxLayout(orientation='vertical', size_hint=(1, .3))
    view.leverage_slider = Leverage_slider(view, vertical_sub_frame_top)
    insert_check_box_and_loan(view, vertical_sub_frame_top)
    view.strategy_menue = Strategy_menue(view, vertical_sub_frame_top)
    vertical_frame.add_widget(vertical_sub_frame_top)

    vertical_sub_frame_bot = BoxLayout(orientation='vertical', size_hint=(1, .6))
    view.table_of_instruments = Table_of_instruments(view, vertical_sub_frame_bot)
    vertical_frame.add_widget(vertical_sub_frame_bot)

    view.add_widget(vertical_frame)


def insert_check_box_and_loan(view, frame):
    def on_checkbox_active(check_box, state):
        view.update_fee_status(state)

    frame.add_widget(Widget(size_hint=(1, .1))) # empty space on top


    sub_frame = BoxLayout(size_hint=(1, .15), orientation='horizontal')

    sub_frame.add_widget(Widget(size_hint=(.5, 1))) # empty space left

    label = Label(text='Include fees',
            **get_style())
    sub_frame.add_widget(label)

    view.use_fees = CheckBox(size_hint=(.2, 1),active=True)
    view.use_fees.bind(active=on_checkbox_active)
    sub_frame.add_widget(view.use_fees)
    
    sub_frame.add_widget(Widget(size_hint=(.6, 1))) # empty space middle

    view.loan = Loan(view, sub_frame)

    sub_frame.add_widget(Widget(size_hint=(.6, 1))) # empty space right

    frame.add_widget(sub_frame)
