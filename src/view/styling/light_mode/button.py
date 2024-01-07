#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

from src.view.styling.light_mode.color_palet import *

def get_style():
    style = {
        "theme_text_color" : "Custom",
        "text_color" : gray_4,
        "line_color" : gray_4,
        "theme_icon_color" : "Custom",
        "icon_color" : gray_4,
        "line_width" : 2,
        "font_size" :20
    }
    return style