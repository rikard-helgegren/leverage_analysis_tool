#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

from src.view.styling.light_mode.color_palet import *

def get_styling():
    styling = {
        "background_color_cell"          : plot_bg,
        "background_color_selected_cell" : plot_bg_darker,
        "background_color_header"        : plot_bg_little_darker,
        "background_color"               : plot_bg,
        "elevation"                      : 0
    }
    
    return styling
