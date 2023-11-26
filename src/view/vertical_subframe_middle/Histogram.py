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
from src.view.Matplot_figure import MatplotFigure

import matplotlib.pyplot as plt
import seaborn as sns

from src.view.styling.set_empty_ticks import set_empty_ticks

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

        light_gray_value = .98
        light_gray = [light_gray_value, light_gray_value, light_gray_value]
        self.fig, self.axs = plt.subplots(
            1,
            1,
            sharey=True,
            tight_layout=True, 
            facecolor=light_gray,
            edgecolor=light_gray)
        set_empty_ticks(self.axs)   
        self.matplot = MatplotFigure()
        self.matplot.figure = self.fig
        frame.add_widget(self.matplot)

        self.canvas = self.matplot.figcanvas

    
    def draw(self, data):
        logging.debug("View: Histogram: draw")
        plt.figure(self.fig.number)

        #if clear_before_drawing: #TODO implement with this input button
        self.axs.clear()

        if data != []:
            [begining_trailing_values, end_before_trailing_values] = self.point_of_trailing_values(data)
            self.axs.set_xlim(xmin=begining_trailing_values, xmax=end_before_trailing_values)   
            hist_plot = sns.histplot(data, element = "step" ,kde=True, bins=200, discrete=False, ax=self.axs)
            y_ticks = self.axs.get_yticks()
            self.axs.set_yticks(y_ticks, ['']*len(y_ticks))
            self.axs.set_ylabel('')
            hist_plot

            plt.tight_layout()
        
        else:
            set_empty_ticks(self.axs)


        self.canvas.draw()

    def point_of_trailing_values(self, data):
        sorted_data = sorted(data)

        begining_trailing_values = sorted_data[0]

        size = len(data)
        last_procentile = int(size/40)
        end_trailing_values = sorted_data[-last_procentile]

        return [begining_trailing_values, end_trailing_values]