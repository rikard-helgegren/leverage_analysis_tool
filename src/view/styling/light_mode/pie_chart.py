#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.


from src.view.styling.light_mode.color_palet import *

def get_text_style_no_data():
    style = {
        "horizontalalignment" : 'center',
        "verticalalignment" : 'center',
        "fontsize" : 30,
        "fontweight" : 'bold',
        "color" : pie_chart_faded_black_text
    }
    return style

def get_text_style_data():
    style = {
        "horizontalalignment" : 'center',
        "verticalalignment" : 'center',
        "fontsize" : 20,
        "fontweight" : 'bold'
    }
    return style

def get_title_style():
    style = {
        'fontsize': 15,
        'fontweight': 'bold',
        'color': 'k'
    }
    return style

