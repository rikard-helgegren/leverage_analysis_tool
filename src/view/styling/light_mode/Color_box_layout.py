#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

from src.view.styling.light_mode.color_palet import *

class Color_box_layout(BoxLayout):
    def __init__(self, **kwargs):
        super(Color_box_layout, self).__init__(**kwargs)
        self.background_color = default_color
        with self.canvas:
            Color(*self.background_color)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    # over writing
    def on_size(self, instance, value):
        self.rect.size = value

    #over writing
    def on_pos(self, instance, value):
        self.rect.pos = value