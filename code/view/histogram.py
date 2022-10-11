
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
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
            plt.hist(data, bins =80, alpha=0.5,color='blue')

        self.canvas.draw()
