
##### Line Graph #####

from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)

def __init__(self):
    
    self.frame3 = Frame(self, padx=5, pady=5)
    self.frame3.pack(side=LEFT)
    # specify the window as master
    self.line_graph_fig = plt.figure(figsize=(4, 5))
    self.line_graph_canvas = FigureCanvasTkAgg(self.line_graph_fig, master=self.frame3)
    self.line_graph_canvas.draw()
    self.line_graph_canvas.get_tk_widget().pack()

    # navigation toolbar
    self.line_graph_toolbarFrame = Frame(master=self.frame3)
    self.line_graph_toolbarFrame.pack()
    self.line_graph_toolbar = NavigationToolbar2Tk(self.line_graph_canvas, self.line_graph_toolbarFrame)
    self.line_graph_toolbar.pack(side=BOTTOM)

def draw_line_graph(self, data):
    print("TRACE: Line_graph_full_time: draw_line_graph")
    plt.figure(self.line_graph_fig.number)

    if data != []:
        plt.plot(data)

    self.line_graph_canvas.draw()