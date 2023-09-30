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

#optimized draw on Agg backend
mpl.rcParams['path.simplify'] = True
mpl.rcParams['path.simplify_threshold'] = 1.0
mpl.rcParams['agg.path.chunksize'] = 1000

#define some matplotlib figure parameters
mpl.rcParams['axes.spines.top'] = False
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.linewidth'] = 1.0

font_size_axis_title=dp(13)
font_size_axis_tick=dp(12)        


class Histogram:
    def __init__(self, view, frame):
        super().__init__()

        self.fig, self.axs = plt.subplots(1, 1, sharey=True, tight_layout=True)      
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
            #plt.style.use('seaborn')
            self.axs.hist(data, bins=80)
            plt.tight_layout()

        self.canvas.draw()
