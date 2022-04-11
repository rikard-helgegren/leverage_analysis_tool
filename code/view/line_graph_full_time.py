
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

def draw_line_graph(self, data, time_intervall):
    print("TRACE: Line_graph_full_time: draw_line_graph")
    plt.figure(self.line_graph_fig.number)

    #if clear_before_drawing: #TODO implement with this input
    self.line_graph_fig.clear(True)

    if data != []:
        set_time_on_x_axis(plt, time_intervall)
        plt.plot(data)


    self.line_graph_canvas.draw()

def set_time_on_x_axis(plt, time_intervall):

    pos = []
    labels = []

    current_year = ""
    for value, time in enumerate(time_intervall):
        #get first 4 digits, i.e. the year
        if str(time)[:4] != current_year:
            current_year = str(time)[:4]
            pos.append(value)
            labels.append(str(time)[:4])

    plt.xticks(pos, labels, rotation='vertical')


