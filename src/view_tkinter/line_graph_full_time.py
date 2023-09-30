#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from src.Json_reader import Json_reader

class Line_Graph_Full_Time:
    def __init__(self, super_frame, tk_frame):
        logging.debug("View: Line_Graph_Full_Time: __init__")
        json_data = Json_reader.read_config()

        self.super_frame = super_frame
        self.tk_frame = tk_frame

        self.frame = tk.Frame(super_frame, padx=5, pady=5)
        self.frame.pack()

        # specify the window as master
        self.fig = plt.figure(figsize=(json_data["PLOT_WIDTH"],json_data["PLOT_HEIGHT"]))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        # navigation toolbar
        self.toolbarFrame = tk.Frame(master=self.frame)
        self.toolbarFrame.pack()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)
        self.toolbar.pack(side=tk.BOTTOM)
        

    def draw(self, values, time_span):
        logging.debug("View: Line_Graph_Full_Time: draw")
        plt.figure(self.fig.number)

        #if clear_before_drawing: #TODO implement with this input
        self.fig.clear(True)

        if values != []:
            self.set_time_on_x_axis(plt, time_span)
            plt.plot(values)
            plt.tight_layout()

        self.canvas.draw()

    def set_time_on_x_axis(self, plt, time_span):
        logging.debug("View: Line_Graph_Full_Time: set_time_on_x_axis")
        pos = []
        labels = []

        current_year = ""
        for i, time in enumerate(time_span):
            #get first 4 digits, i.e. the year
            if str(time)[:4] != current_year:
                current_year = str(time)[:4]
                pos.append(i)
                labels.append(str(time)[:4])

        plt.xticks(pos, labels, rotation='vertical')
