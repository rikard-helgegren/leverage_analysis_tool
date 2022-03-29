from tkinter import *
from  tkinter import ttk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from tkinter import messagebox

import code.view.histogram
import code.view.line_graph_full_time
import code.view.table_of_instruments

class View(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        print("TRACE: View: __init__")

        # create controller
        self.controller = None


        ######################
        # create widgets
        ######################

        self.frame1 = Frame(self, padx=5, pady=5)
        self.frame1.pack(side=LEFT)
        self.checkbutton_fee_state = IntVar()
        self.checkbutton = Checkbutton(self.frame1, text="Include Fees", variable=self.checkbutton_fee_state, command=self.update_fee_status)
        self.checkbutton.pack()

        self.label = Label(self.frame1, text='Years')
        self.label.pack()

        #Spinbox
        self.spin = Spinbox(self.frame1, from_=0, to=100, width=5,command=self.update_limit)
        self.spin.pack()

        #Slide
        self.scale = Scale(self.frame1, from_=0, to=100, orient='horizontal', command=self.update_amount)
        self.scale.pack()

        # Histogram
        code.view.histogram.__init__(self)

        # Line Graph
        code.view.line_graph_full_time.__init__(self)
       
        #Table of Stock Markets
        code.view.table_of_instruments.__init__(self)

    ###############
    # Commands
    ###############

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
        code.view.histogram.draw_histogram(self,data)

    def draw_line_graph(self, data):
        print("TRACE: View: draw_line_graph")
        code.view.line_graph_full_time.draw_line_graph(self,data)

    def set_market_table(self, markets):
        print("TRACE: View: set_market_table")
        code.view.table_of_instruments.set_market_table(self, markets)
        
    def table_item_selected(self, _ ):
        code.view.table_of_instruments.table_item_selected(self)
        