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

def setup_vertical_frame(view):

    frame = BoxLayout(orientation='vertical', size_hint=(0.5, 1))

    sub_frame_super =BoxLayout(orientation='vertical', size_hint=(1, 1))
    sub_frame =BoxLayout(orientation='horizontal', size_hint=(1, 1))

    view.pie_frame1 = Pie_frame(view, sub_frame, "Mean")
    view.pie_frame1.set_default_color([.4,1,.4])
    view.pie_frame2 = Pie_frame(view, sub_frame, "Median")

    sub_frame_super.add_widget(sub_frame)
    view.pie_frame3 = Pie_frame(view, sub_frame_super, "Risk")
    view.pie_frame3.set_default_color([1,.4,.4])
    view.pie_frame3.set_max_value(100)



    frame.add_widget(sub_frame_super)
    
    view.table_of_statistics = Table_of_statistics(view, frame)
    
    view.add_widget(frame)
