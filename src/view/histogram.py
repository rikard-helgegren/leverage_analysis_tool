#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import logging

class Histogram:
    def __init__(self, super_frame):
        logging.debug("View: Histogram: __init__")
        frame = tk.Frame(super_frame, padx=5, pady=5)
        frame.pack()

        # specify the window as master
        self.fig = plt.figure(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        # navigation toolbar
        toolbarFrame = tk.Frame(master=frame)
        toolbarFrame.pack()
        toolbar = NavigationToolbar2Tk(self.canvas, toolbarFrame)
        toolbar.pack(side=tk.BOTTOM)

    def draw(self, data):
        logging.debug("View: Histogram: draw")
        plt.figure(self.fig.number)

        #if clear_before_drawing: #TODO implement with this input button
        self.fig.clear(True)

        if data != []:
            plt.style.use('seaborn')
            plt.hist(data, bins =80, alpha=0.5, color='blue')

        self.canvas.draw()
