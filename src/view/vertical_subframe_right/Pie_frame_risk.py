#!/usr/bin/env python3
#
# Copyright (C) 2024 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.
import logging
import numpy as np

from kivy.uix.boxlayout import BoxLayout

from matplotlib import pyplot as plt

from src.view.vertical_subframe_right.Pie_frame import Pie_frame

from src.view.styling.light_mode.color_palet import *
from src.view.Matplot_figure import MatplotFigure
from src.view.styling.light_mode.pie_chart import get_text_style_no_data
from src.view.styling.light_mode.pie_chart import get_text_style_data
from src.view.styling.light_mode.pie_chart import get_title_style


_WITH_SIZE = 0.2
_THIN_WITH_SIZE=0.05


class Pie_frame_risk(Pie_frame):
    
    def prepare_chart_with_data(self, data):
        display_text = ""
        #if data>=1:
        outer_colors = [light_gray, self.default_color, light_gray]
        vissable_value = max(0, data) #Cant draw a negative amount in pie chart
        invissable_1 = max(0, self.max_value - vissable_value)
        invissable_2 = invissable_1 + vissable_value
        
        data1 = [invissable_1, vissable_value, invissable_2]
        text_color = outer_colors[1]
        vissable_value = round(vissable_value,1)
        display_text = display_text + str(vissable_value) + self.display_ending
        
        self.axs.set_title(self.title, pad=0, y=0.95, fontdict=get_title_style())
        self.axs.pie(data1, radius=1, colors=(outer_colors),
            wedgeprops=dict(width=_WITH_SIZE*2, edgecolor='w'))
        self.axs.text(0.5, 0.5, display_text,
                color= text_color,
                transform=self.axs.transAxes,
                **get_text_style_data()
        )

        plt.tight_layout()
