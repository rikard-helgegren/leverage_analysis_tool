from tkinter import *
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from tkinter import messagebox

class View(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        print("TRACE: View: __init__")

        # set the controller
        self.controller = None

        # create widgets
        # labels
        self.label = Label(self, text='Years')
        self.label.grid(row=1, column=0)

        self.label_blank = Label(self, text=' ')
        self.label_blank.grid(row=3, column=0)

        # entries
        self.string_var = StringVar()
        self.string_entry = Entry(self, textvariable=self.string_var, width=10)
        self.string_entry.grid(row=2, column=0, sticky=NSEW)

        # checkbuttons
        self.checkbutton_fee_state = IntVar()
        self.checkbutton = Checkbutton(self, text="Include Fees", variable=self.checkbutton_fee_state, command=self.update_fee_status)
        self.checkbutton.grid(row=4, column=0)

        #Spinbox
        self.spin = Spinbox(self, from_=0, to=100, width=5,command=self.update_limit)
        self.spin.grid(row=5,column=0)

        #Scale
        self.scale = Scale(self, from_=0, to=100, orient='horizontal', command=self.update_amount)
        self.scale.grid(row=6,column=0)

        self.draw_histogram([])
        self.draw_line_graph([])

    def set_controller(self, controller):
        print("TRACE: View: set_controller")
        self.controller = controller

    def update_fee_status(self):
        print("TRACE: View: update_fee_status")
        print("View, fee_status:", self.checkbutton_fee_state.get())
        self.controller.update_fee_status(self.checkbutton_fee_state.get())
        messagebox.showinfo('Error', 'Not fully implemented')
    
    def update_limit(self):
        print("TRACE: View: update_limit")
        messagebox.showinfo('Error', 'Not fully implemented')
        #TODO

    def update_amount(self, value):
        print("TRACE: View: update_amount")
        messagebox.showinfo('Error', 'Not fully implemented')
        #TODO


    def draw_histogram(self, data):
        print("TRACE: View: draw_histogram")
        #Figure
        fig = plt.figure(figsize=(4, 5))
        
        if data != []:
            plt.hist(data)

        # specify the window as master
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=7, column=0, ipadx=40, ipady=20)

        # navigation toolbar
        toolbarFrame = Frame(master=self)
        toolbarFrame.grid(row=8,column=0)
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)


    def draw_line_graph(self, data):
        print("TRACE: View: draw_line_graph")
        #Figure
        fig = plt.figure(figsize=(4, 5))
        
        if data != []:
            plt.plot(data)

        # specify the window as master
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=7, column=1, ipadx=40, ipady=20)

        # navigation toolbar
        toolbarFrame = Frame(master=self)
        toolbarFrame.grid(row=8,column=1)
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)