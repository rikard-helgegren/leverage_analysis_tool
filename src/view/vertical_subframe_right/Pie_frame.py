#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.
import logging
import numpy as np

from kivy.uix.boxlayout import BoxLayout

from matplotlib import pyplot as plt

from src.view.styling.light_mode.color_palet import *
from src.view.Matplot_figure import MatplotFigure
from src.view.styling.light_mode.pie_chart import get_text_style_no_data
from src.view.styling.light_mode.pie_chart import get_text_style_data
from src.view.styling.light_mode.pie_chart import get_text_style_double_data
from src.view.styling.light_mode.pie_chart import get_title_style

_WITH_SIZE = 0.2
_THIN_WITH_SIZE=0.05

class Pie_frame():
    def __init__(self, frame, title=""):
        logging.debug("View: Pie_frame: __init__")
        self.title = title
        self.default_color = None
        self.reference_color = None
        self.max_value = 20
        self.display_ending = ''

        self.fig, self.axs = plt.subplots(
            sharey=True,
            tight_layout=True, 
            facecolor=light_gray,
            edgecolor=light_gray
        )
        
        self.matplot = MatplotFigure()
        self.matplot.figure = self.fig
        frame.add_widget(self.matplot)

        self.canvas = self.matplot.figcanvas

        #TODO: REMOVE AFTER CLEAN UP
        self.draw([])


    def draw(self, data):
        logging.debug("View: Pie_frame: draw")
        plt.figure(self.fig.number)

        if isinstance(data, str):
            data = float(data.replace('%',''))
            if data != 0:
                data = data/100 + 1

        #if clear_before_drawing: #TODO implement with this input button
        self.axs.clear()

        if data != []:
            self.prepare_chart_with_data(data)
        else:
            self.prepare_chart_no_data()        

        self.canvas.draw()

    def prepare_chart_with_data(self, data):
        logging.debug("View: Pie_frame: prepare_chart_with_data")
        self.axs.set_title(self.title, pad=0, y=0.95, fontdict=get_title_style())

        if len(data) == 1:
            value = max(0, (data[0] - 1) * 100)  #Cant draw a negative amount in pie chart
            value = int(value + 0.5)
            self.draw_solo_piechart(value)
            self.write_solo_number(value)

        elif len(data) == 2:
            values = [max(0, (value - 1) * 100) for value in data]  #Cant draw a negative amount in pie chart
            values = [int(value + 0.5) for value in values]
            self.draw_double_outer_piechart(values[0])
            self.draw_double_inner_piechart(values[1])
            self.write_double_number(values)
            
        else:
            logging.error("View: Pie_frame: Cant draw pie charts for this data: ", data)

        plt.tight_layout()

    def draw_solo_piechart(self, value):
        logging.debug("View: Pie_frame: draw_solo_piechart")
        outer_colors = [light_gray, self.default_color, light_gray]
        radius= 1
        width=_WITH_SIZE*2
        self.draw_general_piechart(value, outer_colors, radius, width)

    def draw_double_outer_piechart(self, value):
        logging.debug("View: Pie_frame: draw_double_outer_piechart")
        outer_colors = [light_gray, self.default_color, light_gray]
        radius= 1
        width=_WITH_SIZE
        self.draw_general_piechart(value, outer_colors, radius, width)
        
    
    def draw_double_inner_piechart(self, value):
        logging.debug("View: Pie_frame: draw_double_inner_piechart")
        outer_colors = [light_gray, self.reference_color, light_gray]
        radius= 1-_WITH_SIZE
        width=_WITH_SIZE
        self.draw_general_piechart(value, outer_colors, radius, width)
    
    def draw_general_piechart(self, value, color, radius, width):
        logging.debug("View: Pie_frame: draw_general_piechart")
        vissable_value = value #Cant draw a negative amount in pie chart
        invissable_1 = max(0, self.max_value - vissable_value)
        invissable_2 = invissable_1 + vissable_value
        
        data1 = [invissable_1, vissable_value, invissable_2]
        
        self.axs.pie(data1,
                radius=radius,
                colors=(color),
                wedgeprops=dict(width=width, edgecolor='w'))

    def prepare_chart_no_data(self):
        logging.debug("View: Pie_frame: prepare_chart_no_data")
        self.axs.set_title(self.title, pad=0, y=0.95, fontdict=get_title_style())
        self.axs.pie([1],
            radius=1,
            colors=([pie_chart_faded_black_text]),
            wedgeprops=dict(width=_THIN_WITH_SIZE, edgecolor='w')
        )
        self.axs.pie([1],
            radius=1-_THIN_WITH_SIZE, 
            colors=([light_gray]),
            wedgeprops=dict(width=_WITH_SIZE*2, edgecolor='w')
        )
        self.axs.text(0.5, 0.5, '0'+self.display_ending,
                transform=self.axs.transAxes,
                **get_text_style_no_data())
        
    def write_solo_number(self, value):
        logging.debug("View: Pie_frame: write_solo_number")
        self.display_text = str(value) + self.display_ending

        self.axs.set_title(self.title, pad=0, y=0.95, fontdict=get_title_style())
        self.axs.text(0.5, 0.5, self.display_text,
                color=self.default_color,
                transform=self.axs.transAxes,
                **get_text_style_data())
        
    def write_double_number(self, values ):
        logging.debug("View: Pie_frame: write_double_number")
        self.axs.set_title(self.title, pad=0, y=0.95, fontdict=get_title_style())
        
        self.display_text1 = str(values[0]) + self.display_ending

        self.axs.text(0.5, 0.65, self.display_text1,
                color=self.default_color,
                transform=self.axs.transAxes,
                **get_text_style_double_data())
        
        self.display_text2 = str(values[1]) + self.display_ending
        self.axs.text(0.5, 0.54, self.display_text2,
                color=self.reference_color,
                transform=self.axs.transAxes,
                **get_text_style_double_data())

    def set_default_color(self, color):
        logging.debug("View: Pie_frame: set_default_color")
        self.default_color = color

    def set_reference_color(self, color):
        logging.debug("View: Pie_frame: set_reference_color")
        self.reference_color = color

    def set_max_value(self, max_value):
        logging.debug("View: Pie_frame: set_max_value")
        self.max_value = max_value
    
    def set_display_ending(self, display_ending):
        logging.debug("View: Pie_frame: set_display_ending")
        self.display_ending = display_ending
