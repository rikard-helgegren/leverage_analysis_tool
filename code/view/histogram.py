
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)

class Histogram:
    def __init__(self, gui_frame):
        print("TRACE: View: Histogram: __init__")
        frame = tk.Frame(gui_frame, padx=5, pady=5)
        frame.pack(side=tk.LEFT)
        # specify the window as master
        self.fig = plt.figure(figsize=(4, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        # navigation toolbar
        toolbarFrame = tk.Frame(master=frame)
        toolbarFrame.pack()
        toolbar = NavigationToolbar2Tk(self.canvas, toolbarFrame)
        toolbar.pack(side=tk.BOTTOM)

    def draw(self, data):
        print("TRACE: View: Histogram: draw")
        plt.figure(self.fig.number)

        #if clear_before_drawing: #TODO implement with this input button
        self.fig.clear(True)

        if data != []:
            plt.hist(data)

        self.canvas.draw()
