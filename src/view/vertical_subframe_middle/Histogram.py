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
import seaborn as sns

from kivy.metrics import dp

from src.view.Matplot_figure import MatplotFigure
from src.view.styling.set_empty_ticks import set_empty_ticks
from src.view.styling.light_mode.color_palet import *


#optimized draw on Agg backend
mpl.rcParams['path.simplify'] = True
mpl.rcParams['path.simplify_threshold'] = 1.0
mpl.rcParams['agg.path.chunksize'] = 1000

#define some matplotlib figure parameters
mpl.rcParams['axes.spines.top'] = False
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.linewidth'] = 1.0
mpl.style.use('seaborn-v0_8')

font_size_axis_title=dp(13)
font_size_axis_tick=dp(12)        


class Histogram:
    def __init__(self, view, frame):
        super().__init__()

        self.fig, self.axs = plt.subplots(
            nrows=1,
            ncols=1,
            sharey=True,
            tight_layout=True, 
            facecolor=light_gray,
            edgecolor=light_gray
        )
        set_empty_ticks(self.axs)   
        self.matplot = MatplotFigure()
        self.matplot.figure = self.fig
        frame.add_widget(self.matplot)

        self.canvas = self.matplot.figcanvas

        self.data_list = []
    
    def draw(self, data_list): #TODO make list input of hist data.
        logging.debug("View: Histogram: draw")

        self.data_list = data_list

        self._draw()

    def _draw(self):
        plt.figure(self.fig.number)

        clear_canvas = True
        
        color_graph = portfolio_data_color

        #if clear_before_drawing: #TODO implement with this input button
        self.axs.clear()

        left_edge = 1
        right_edge = 1.01

        for data in self.data_list:
            if data != []:
                left_edge = min(left_edge, min(data))
                right_edge = max(right_edge, max(data))

        for index in range(len(self.data_list)):
            if self.data_list[index] != []:
                [begining_trailing_values, end_before_trailing_values] = self.point_of_trailing_values(self.data_list[index])
                if (begining_trailing_values != end_before_trailing_values): # Avoid cosmetical error
                    self.axs.set_xlim(xmin=begining_trailing_values, xmax=end_before_trailing_values)   
                hist_plot = sns.histplot(
                    self.data_list[index],
                    element = "step",
                    kde=True,
                    bins=200,
                    binrange=(left_edge, right_edge),
                    discrete=False,
                    ax=self.axs,
                    color = color_graph[index]
                )
                y_ticks = self.axs.get_yticks()
                self.axs.set_yticks(y_ticks, ['']*len(y_ticks))
                self.axs.set_ylabel('')
                hist_plot

            plt.tight_layout()

            clear_canvas = False
        
        if clear_canvas:
            set_empty_ticks(self.axs)

        self.stylize_ticks()
        self.canvas.draw_idle()

    def point_of_trailing_values(self, data):
        sorted_data = sorted(data)

        begining_trailing_values = sorted_data[0]

        size = len(data)
        last_procentile = int(size/40)
        end_trailing_values = sorted_data[-last_procentile]

        return [begining_trailing_values, end_trailing_values]

    def stylize_ticks(self):
        for lbl in self.axs.get_xticklabels():
            try:
                if abs(float(lbl.get_text()) - 1.0) < 1e-4:
                    lbl.set_fontweight('bold')
                else:
                    lbl.set_fontweight('normal')

                if float(lbl.get_text()) < 0.95:
                    lbl.set_color('red')
                if float(lbl.get_text()) > 1.05:
                    lbl.set_color('green')

            except Exception:
                # Non-numeric tick label, ignore
                pass