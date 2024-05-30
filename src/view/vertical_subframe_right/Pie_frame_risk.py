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
        self.display_text = ""
        outer_colors = [light_gray, self.default_color, light_gray]
        text_color = outer_colors[1]
        self.axs.set_title(self.title, pad=0, y=0.95, fontdict=get_title_style())

        if len(data) == 1:
            value = max(0, data[0] )  #Cant draw a negative amount in pie chart
            self.draw_solo_piechart(value)
            self.write_solo_number(value)

        elif len(data) == 2:
            values = [max(0, value) for value in data]  #Cant draw a negative amount in pie chart
            self.draw_double_outer_piechart(values[0])
            self.draw_double_inner_piechart(values[1])
            self.write_double_number(values)
            
        else:
            logging.error("View: Pie_frame: Cant draw pie charts for this data: ", data)

        self.axs.set_title(self.title, pad=0, y=0.95, fontdict=get_title_style())

        plt.tight_layout()

    def draw_general_piechart(self, value, color, radius, width):
        vissable_value = max(0, (value)) #Cant draw a negative amount in pie chart
        invissable_1 = max(0, self.max_value - vissable_value)
        invissable_2 = invissable_1 + vissable_value
        
        data1 = [invissable_1, vissable_value, invissable_2]
        
        self.display_text = str(vissable_value) + self.display_ending
        
        self.axs.pie(data1,
                radius=radius,
                colors=(color),
                wedgeprops=dict(width=width, edgecolor='w'))

