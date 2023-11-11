#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.
import logging
import matplotlib as mpl
import matplotlib.pyplot as plt

from kivy.metrics import dp
from kivy.uix.widget import Widget
from src.view.Matplot_figure import MatplotFigure


#optimized draw on Agg backend
mpl.rcParams['path.simplify'] = True
mpl.rcParams['path.simplify_threshold'] = 1.0
mpl.rcParams['agg.path.chunksize'] = 1000

#define some matplotlib figure parameters
#mpl.rcParams['font.family'] = 'Verdana'
mpl.rcParams['axes.spines.top'] = False
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.linewidth'] = 1.0

font_size_axis_title=dp(13)
font_size_axis_tick=dp(12)        


class Line_graph(Widget):
    """class that generate Matplotlib graph."""
    def __init__(self, view, frame):  
        super().__init__()

        light_gray = .98
        self.fig, self.axs = plt.subplots(1, 1, sharey=True, tight_layout=True, facecolor=[light_gray, light_gray, light_gray])
    
        self.axs.set_xticks([0,2,4,6,8,10], ['','','','','',''])
        self.axs.set_yticks([0,2,4,6,8,10], ['','','','','',''])
        self.matplot = MatplotFigure()
        self.matplot.figure = self.fig
        frame.add_widget(self.matplot)

        self.canvas = self.matplot.figcanvas

    
    def draw(self, values, time_span):
        logging.debug("View: Line_graph: draw")
        plt.figure(self.fig.number)

        #if clear_before_drawing: #TODO implement with this input
        self.axs.clear()

        if values != []:
            self.set_time_on_x_axis(self.axs, time_span)
            self.line1, = self.axs.plot(values)
            plt.tight_layout()
        else:
            self.axs.set_xticks([0,2,4,6,8,10], ['','','','','',''])
            self.axs.set_yticks([0,2,4,6,8,10], ['','','','','',''])
        
        self.canvas.draw()


    def set_time_on_x_axis(self, ax, time_span):
        logging.debug("View: Line_graph: set_time_on_x_axis")
        pos = []
        labels = []

        refrence_year = ""
        for i, time in enumerate(time_span):
            #get first 4 digits, i.e. the year
            year = str(time)[:4]
            if year != refrence_year:
                refrence_year = year
                pos.append(i)
                labels.append(year)

        ax.set_xticks(pos, labels, rotation='vertical')
