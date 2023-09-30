#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from src.view.Histogram import Histogram
from src.view.Line_graph import Line_graph
from src.view.Matplot_figure import MatplotFigure

def setup_vertical_frame_2(view):


    frame = BoxLayout(orientation='vertical', padding=5)


    view.histogram = Histogram(view, frame)

    view.line_graph = Line_graph(view, frame)

    insert_time_boxing(frame)
    

    view.add_widget(frame)



def insert_time_boxing(frame):


    box_in_box = BoxLayout(size_hint=(1, .15))
    box_in_box.add_widget(Widget(size_hint=(.8, 1)))

    box_in_box2 = BoxLayout(orientation='vertical', size_hint=(1, 1))
    label = Label(text='[color=000000]Start Date[/color]',
    markup = True, size_hint=(1, .8))
    box_in_box2.add_widget(label)
    textinput = TextInput(text='2000-01-01', multiline=False, size_hint =(1, 1))
    textinput.bind(on_text_validate=on_enter)
    box_in_box2.add_widget(textinput)
    box_in_box.add_widget(box_in_box2)

    box_in_box.add_widget(Widget(size_hint=(.7, 1)))


    box_in_box3 = BoxLayout(orientation='vertical', size_hint=(1, 1))
    label = Label(text='[color=000000]End Date[/color]',
    markup = True, size_hint=(1, .8))
    box_in_box3.add_widget(label)
    textinput2 = TextInput(text='2020-01-01', multiline=False, size_hint =(1, 1))
    textinput2.bind(on_text_validate=on_enter)
    box_in_box3.add_widget(textinput2)
    box_in_box.add_widget(box_in_box3)
    
    frame.add_widget(box_in_box)

    box_in_box.add_widget(Widget(size_hint=(.8, 1)))


def on_enter(one):
    print("text")
