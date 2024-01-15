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
from src.view.styling.set_empty_ticks import set_empty_ticks
from src.view.styling.light_mode.color_palet import *


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

        self.view = view

        self.fig, self.axs = plt.subplots(
            nrows=1, 
            ncols=1,
            sharey=True,
            tight_layout=True,
            facecolor=light_gray
        )
    
        set_empty_ticks(self.axs)
        self.matplot = MatplotFigure()
        self.matplot.figure = self.fig
        frame.add_widget(self.matplot)

        self.canvas = self.matplot.figcanvas

        # Place holders
        self.values = [] 
        self.time_span = []
        self.buy_sell_log = {}
        self.values_refrence = [] 
        self.time_span_refrence = []
        self.buy_sell_log_refrence = {}

    def update_refrence(self):
        logging.info("View: Line_graph: update_refrence")

        if self.values == [] or self.values ==  self.values_refrence:
            self.values_refrence = []
            self.time_span_refrence = []
            self.buy_sell_log_refrence = {}
        else:
            self.values_refrence =  self.values      
            self.time_span_refrence = self.time_span
            self.buy_sell_log_refrence = self.buy_sell_log
        
        self._draw()

    def draw(self, values, time_span, buy_sell_log):
        logging.debug("View: Line_graph: draw")
        
        self.values = values
        self.time_span = time_span        
        self.buy_sell_log = buy_sell_log

        self._draw()

    def update(self):
        logging.debug("View: Line_graph: update")
        self._draw()

    def _draw(self):
        plt.figure(self.fig.number)
        clear_canvas = True

        #if clear_before_drawing: #TODO implement with this input
        self.axs.clear()

        if self.values != []:
            self.set_time_on_x_axis(self.axs, self.time_span)
            if self.view.show_trades:
                self.set_buy_and_sell_markers(self.axs, self.values, self.buy_sell_log)
            self.line1, = self.axs.plot(
                self.values, 
                color = 'blue',
                alpha=0.5
            )
            plt.tight_layout()
            clear_canvas = False
        
        if self.values_refrence != []:
            self.set_time_on_x_axis(self.axs, self.time_span_refrence)
            if self.view.show_trades:
                self.set_buy_and_sell_markers(self.axs, self.values_refrence, self.buy_sell_log_refrence)
            self.line1, = self.axs.plot(
                self.values_refrence, 
                color = 'green',
                alpha=0.5
            )
            plt.tight_layout()
            clear_canvas = False
        
        if clear_canvas:
            set_empty_ticks(self.axs)
        
        self.canvas.draw()

    def set_buy_and_sell_markers(self, axs, values, buy_sell_log):
        logging.debug("View: Line_graph: set_buy_and_sell_markers")
        circle_size =100

        x_values = []
        y_values = []
        colors = []
        did_buy=False
        did_sell=False

        for value in buy_sell_log:
            if value > len(values): # bug from samples size of data to determine behaviour
                logging.warn("index out off bounds scatter plott" + str(value) + " of " + str(len(values)))
            else:
                
                x_values.append(value)
                y_values.append(values[value])
                events = buy_sell_log[value]
                
                # Reset
                did_buy=False
                did_sell=False

                for event in events:
                    if event['Action'].value == 1:
                        did_buy=True
                    elif event['Action'].value == 2:
                        did_sell=True
                    else:
                        logging.warn("View.Linegraph: set_buy_and_sell_markers, invallid logg action: " + str(event['Activity']))
                
                if did_buy and did_sell:
                    colors.append(graph_buy_and_sell)
                elif did_buy:
                    colors.append(graph_buy_green)
                elif did_sell:
                    colors.append(graph_sell_red)

        axs.scatter(x_values, y_values, s=circle_size, c=colors)

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
