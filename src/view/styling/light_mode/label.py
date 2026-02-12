#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

def get_style():
    style = {
        "color" : [0,0,0,1],
        "markup" : True,
        "font_size" : 18
    }
    return style


def get_style_bold():
    style = {
        "color" : [0,0,0,1],
        "markup" : True,
        "font_size" : 18,
        "bold" : True,
    }
    return style

def get_style_no_font_size():
    style = {
        "color" : [0,0,0,1],
        "markup" : True,
    }
    return style
