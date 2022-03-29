##### histogram #####
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)

def __init__(self):
    print("TRACE: View: draw_histogram")
    frame = Frame(self, padx=5, pady=5)
    frame.pack(side=LEFT)
    # specify the window as master
    self.histogram_fig = plt.figure(figsize=(4, 5))
    self.histogram_canvas = FigureCanvasTkAgg(self.histogram_fig, master=frame)
    self.histogram_canvas.draw()
    self.histogram_canvas.get_tk_widget().pack()

    # navigation toolbar
    histogram_toolbarFrame = Frame(master=frame)
    histogram_toolbarFrame.pack()
    histogram_toolbar = NavigationToolbar2Tk(self.histogram_canvas, histogram_toolbarFrame)
    histogram_toolbar.pack(side=BOTTOM)

def draw_histogram(self, data):
    print("TRACE: Histogram: draw_histogram")
    plt.figure(self.histogram_fig.number)

    if data != []:
        plt.hist(data)

    self.histogram_canvas.draw()