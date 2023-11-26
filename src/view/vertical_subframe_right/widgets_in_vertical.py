#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging
from kivy.uix.boxlayout import BoxLayout

from src.view.vertical_subframe_right.Table_of_statistics import Table_of_statistics
from src.view.vertical_subframe_right.Pie_frame import Pie_frame
from src.view.styling.light_mode.color_palet import *

def setup_vertical_frame(view):

    frame = BoxLayout(orientation='vertical', size_hint=(0.5, 1))

    sub_frame_super =BoxLayout(orientation='vertical', size_hint=(1, 1))
    
    sub_frame =BoxLayout(orientation='horizontal', size_hint=(1, 1))
    view.pie_frame1 = Pie_frame(sub_frame, "Mean")
    view.pie_frame1.set_default_color(pie_chart_mean_first_color)
    view.pie_frame1.set_refrence_color(pie_chart_mean_first_color)
    view.pie_frame1.set_display_ending('%')

    view.pie_frame2 = Pie_frame(sub_frame, "Median")
    view.pie_frame2.set_default_color(pie_chart_median_first_color)
    view.pie_frame2.set_refrence_color(pie_chart_median_first_color)
    view.pie_frame2.set_display_ending('%')

    sub_frame_super.add_widget(sub_frame)


    view.pie_frame3 = Pie_frame(sub_frame_super, "Risk Index")
    view.pie_frame3.set_default_color(pie_chart_risk_first_color)
    view.pie_frame3.set_refrence_color(pie_chart_risk_first_color)
    view.pie_frame3.set_max_value(100)

    frame.add_widget(sub_frame_super)

    sub_frame2 =BoxLayout(size_hint=(1, 1))
    view.table_of_statistics = Table_of_statistics(view, sub_frame2)

    frame.add_widget(sub_frame2)
    
    view.add_widget(frame)
