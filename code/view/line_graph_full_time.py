
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class Line_Graph_Full_Time:
    def __init__(self, super_frame):
        print("TRACE: View: Line_Graph_Full_Time: __init__")

        self.frame = tk.Frame(super_frame, padx=5, pady=5)
        self.frame.pack()
        # specify the window as master
        self.fig = plt.figure(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        # navigation toolbar
        self.toolbarFrame = tk.Frame(master=self.frame)
        self.toolbarFrame.pack()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)
        self.toolbar.pack(side=tk.BOTTOM)

    def draw(self, values, time_span):
        print("TRACE: View: Line_Graph_Full_Time: draw")
        plt.figure(self.fig.number)

        #if clear_before_drawing: #TODO implement with this input
        self.fig.clear(True)

        if values != []:
            self.set_time_on_x_axis(plt, time_span)
            plt.plot(values)


        self.canvas.draw()

    def set_time_on_x_axis(self, plt, time_span):
        print("TRACE: View: Line_Graph_Full_Time: set_time_on_x_axis")
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


