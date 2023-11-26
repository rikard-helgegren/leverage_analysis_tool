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

from matplotlib import pyplot as plt
import numpy as np

from src.view.styling.light_mode.color_palet import *


from src.view.Matplot_figure import MatplotFigure
from src.view.styling.light_mode.pie_chart import get_text_style_no_data
from src.view.styling.light_mode.pie_chart import get_text_style_data
from src.view.styling.light_mode.pie_chart import get_title_style

class Pie_frame():
    def __init__(self, frame, title=""):

        self.title = title

        self.default_color = None
        self.refrence_color = None
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

        #REMOVE AFTER CLEAN UP
        self.draw(0)


    def draw(self, data):
        logging.debug("View: Pie_frame: draw")
        plt.figure(self.fig.number)

        if isinstance(data, str):
            data = float(data.replace('%',''))
            if data != 0:
                data = data/100 + 1

        with_size = 0.2

        #if clear_before_drawing: #TODO implement with this input button
        self.axs.clear()

        if data != 0:
            display_text = ""
            if data>=1:
                outer_colors = [light_gray,self.default_color,light_gray]
                val2 = max(0, (data - 1) * 100) #Cant draw a negative amount in pie chart
                val1 = max(0, self.max_value - val2)
                val3 = val1 + val2
                
            else:
                outer_colors = [light_gray,pie_chart_risk_first_color,light_gray]
                val2 = max(0,(1 - data ) * 100) #Cant draw a negative amount in pie chart
                val3 = max(0, self.max_value - val2)
                val1 = val2 + val3 
            
            data1 = [val1,val2,val3]
            text_color = outer_colors[1]
            val2 = int(val2) #round to whole integer
            display_text = display_text + str(val2) + self.display_ending
            
            self.axs.set_title(self.title, pad=0, y=0.95, fontdict=get_title_style())
            self.axs.pie(data1, radius=1, colors=(outer_colors),
                wedgeprops=dict(width=with_size*2, edgecolor='w'))
            self.axs.text(0.5, 0.5, display_text,
                    color= text_color,
                    transform=self.axs.transAxes,
                    **get_text_style_data()
            )

            plt.tight_layout()
        
        else:
            thin=0.05

            self.axs.set_title(self.title, pad=0, y=0.95, fontdict=get_title_style())
            self.axs.pie([1], radius=1, colors=([pie_chart_faded_black_text]),
                wedgeprops=dict(width=thin, edgecolor='w'))
            self.axs.pie([1], radius=1-thin, colors=([light_gray]),
                wedgeprops=dict(width=with_size*2, edgecolor='w'))
            #self.axs.pie([1], radius=1-thin-(with_size*2), colors=(['k']),
            #    wedgeprops=dict(width=thin, edgecolor='w'))
            self.axs.text(0.5, 0.5, '0'+self.display_ending,
                    transform=self.axs.transAxes,
                    **get_text_style_no_data())

        self.canvas.draw()


    def set_default_color(self, color):
        self.default_color = color

    def set_refrence_color(self, color):
        self.refrence_color = color

    def set_max_value(self, max_value):
        self.max_value = max_value
    
    def set_display_ending(self, display_ending):
        self.display_ending = display_ending
