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
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout


def setup_vertical_frame(view):
    vertical_frame = BoxLayout(orientation='vertical', padding=5, size_hint=(.8, 1))
    insert_space_top(vertical_frame)
    insert_slider(vertical_frame)
    insert_check_box(vertical_frame)
    insert_time_and_loan(vertical_frame)
    insert_spinner(vertical_frame)
    insert_space_bott(vertical_frame)

    view.add_widget(vertical_frame)


def insert_space_top(frame):
    frame.add_widget(Widget(size_hint=(1, .5)))


def insert_space_bott(frame):
    frame.add_widget(Widget(size_hint=(1, .8)))


def insert_slider(frame):
    def on_slider_change(instance, value):
        slide_counter.text=make_text_black(str(int(value)))

    sub_frame = GridLayout(size_hint=(1, .4), cols=1, )
    label = Label(text=make_text_black('Percent Leverage'),
    markup = True, size_hint=(1, 1))
    sub_frame.add_widget(label)

    sub_sub_frame = BoxLayout(size_hint=(1, .2) )
    slider = Slider(value=10, size_hint =(1, 1))
    slider.bind(value=on_slider_change)
    sub_sub_frame.add_widget(slider)

    slide_counter = Label(text=make_text_black('10'),
    markup = True, size_hint=(.1, 1))
    sub_sub_frame.add_widget(slide_counter)

    sub_frame.add_widget(sub_sub_frame)
    frame.add_widget(sub_frame)
    

def insert_check_box(frame):
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


def insert_time_and_loan(frame):
    sub_frame = BoxLayout(size_hint=(1, .2))
    
    sub_frame.add_widget(Widget())

    time_frame = BoxLayout(orientation='vertical', size_hint=(1, 1))
    label = Label(text=make_text_black('Time Investing'),
    markup = True, size_hint=(1, 1))
    time_frame.add_widget(label)
    textinput = TextInput(text='1', multiline=False, size_hint =(.8, .7))
    textinput.bind(on_text_validate=textbox_on_enter)
    time_frame.add_widget(textinput)
    sub_frame.add_widget(time_frame)

    sub_frame.add_widget(Widget())

    loan_frame = BoxLayout(orientation='vertical', size_hint=(1, 1))
    label = Label(text=make_text_black('Loan'),
    markup = True)
    loan_frame.add_widget(label)
    textinput = TextInput(text='0', multiline=False, size_hint =(.8, .7))
    textinput.bind(on_text_validate=textbox_on_enter)
    loan_frame.add_widget(textinput)
    sub_frame.add_widget(loan_frame)

    sub_frame.add_widget(Widget())
    
    frame.add_widget(sub_frame)


def insert_spinner(frame):
    frame.add_widget(Widget(size_hint=(1, .2)))

    spinner = Spinner(
        text='Strategies',
        values=('Hold', 'Rebalance', 'Harvest refill', 'Variance', 'Dont invest'),
        size_hint=(0.2, 0.12),
        pos_hint={'center_x': .5, 'center_y': .5}
    )
    
    spinner.bind(text=show_selected_value)
    frame.add_widget(spinner)


def make_text_black(text):
    return '[color=000000]'+ text +'[/color]'


def textbox_on_enter(one):
    print("text")


def on_checkbox_active(one, two):
    print("on_checkbox_active")


def show_selected_value(spinner, text):
    print('The spinner', spinner, 'has text', text)
    