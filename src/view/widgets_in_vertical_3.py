#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout


from src.view.Table_of_instruments import Table_of_instuments
from src.view.Table_of_statistics import Table_of_statistics


def setup_vertical_frame_3(view):

    frame = BoxLayout(orientation='vertical', padding=5, size_hint=(0.7, 1))
    
    view.table_of_instruments = Table_of_instuments(view, frame)

    view.table_of_statistics = Table_of_statistics(view, frame)
    
    view.add_widget(frame)

