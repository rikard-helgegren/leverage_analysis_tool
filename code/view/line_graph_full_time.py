
##### Line Graph #####

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

def __init__(self):
    
    self.frame3 = tk.Frame(self, padx=5, pady=5)
    self.frame3.pack(side=tk.LEFT)
    # specify the window as master
    self.line_graph_fig = plt.figure(figsize=(4, 5))
    self.line_graph_canvas = FigureCanvasTkAgg(self.line_graph_fig, master=self.frame3)
    self.line_graph_canvas.draw()
    self.line_graph_canvas.get_tk_widget().pack()

    # navigation toolbar
    self.line_graph_toolbarFrame = tk.Frame(master=self.frame3)
    self.line_graph_toolbarFrame.pack()
    self.line_graph_toolbar = NavigationToolbar2Tk(self.line_graph_canvas, self.line_graph_toolbarFrame)
    self.line_graph_toolbar.pack(side=tk.BOTTOM)

def draw_line_graph(self, values, time_span):
    print("TRACE: Line_graph_full_time: draw_line_graph")
    plt.figure(self.line_graph_fig.number)

    #if clear_before_drawing: #TODO implement with this input
    self.line_graph_fig.clear(True)

    if values != []:
        set_time_on_x_axis(plt, time_span)
        plt.plot(values)


    self.line_graph_canvas.draw()

def set_time_on_x_axis(plt, time_span):

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


