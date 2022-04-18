

import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


import code.view.histogram
import code.view.line_graph_full_time
import code.view.table_of_instruments

from code.view.histogram import Histogram
from code.view.line_graph_full_time import Line_Graph_Full_Time
from code.view.table_of_instruments import Table_Of_Instuments

class View(tk.Frame):
    """This is the view of the application. It is the interface beetween
       the user and the model.

       The View contains widgets and plots, and comunicates any interactions
       with the view to the controller
    """
    def __init__(self, parent):
        print("TRACE: View: __init__")

        super().__init__(parent)

        # placeholder for controller
        self.controller = None


        ######################
        # create widgets
        ######################

        self.frame1 = tk.Frame(self, padx=5, pady=5)
        self.frame1.pack(side=tk.LEFT)
        self.checkbutton_fee_state = tk.IntVar()
        self.checkbutton = tk.Checkbutton(self.frame1, text="Include Fees", variable=self.checkbutton_fee_state, command=self.update_fee_status)
        self.checkbutton.pack()

        self.label = tk.Label(self.frame1, text='Years')
        self.label.pack()

        #Spinbox
        self.spin = tk.Spinbox(self.frame1, from_=0, to=100, width=5,command=self.update_limit)
        self.spin.pack()

        #Slide
        self.scale = tk.Scale(self.frame1, from_=0, to=100, orient='horizontal', command=self.update_amount)
        self.scale.pack()

        self.histogram = Histogram(self)
        """ The histogram displaies a distribution of outcomes from all continious
            time intervals of the selected length.
        """

        self.line_graph_full_time = Line_Graph_Full_Time(self)
        """ This line garaph displaies the performance of the created portfolio
            for the full time span available
        """

        self.table_of_instruments = Table_Of_Instuments(self)
        """ The table of instruments is a table from which the user can select
            instruments with or without leverage to use in their portfolio
        """


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
        tk.messagebox.showinfo('Error', 'Not fully implemented')
    
    def update_limit(self):
        print("TRACE: View: update_limit")
        tk.messagebox.showinfo('Error', 'Not fully implemented')
        #TODO

    def update_amount(self, value):
        print("TRACE: View: update_amount")
        tk.messagebox.showinfo('Error', 'Not fully implemented')
        #TODO

    def draw_histogram(self, data):
        print("TRACE: View: draw_histogram")
        self.histogram.draw(data)

    def draw_line_graph(self, values, time_span):
        print("TRACE: View: draw_line_graph")
        self.line_graph_full_time.draw(values, time_span)

    def set_table_of_instruments(self, names, countries):
        print("TRACE: View: set_market_table")
        self.table_of_instruments.set_table(names, countries)
        
    def update_table_item_focused(self, _ ):
        #TODO move parts of code to the table class and rename method
        print("TRACE: View: table_item_focused")

        did_unfolding = self.table_of_instruments.only_did_unfolding()

        if did_unfolding:
            #An item was only unfolded do nothing
            return
        else:
            #An item was selected update view
            self.table_of_instruments.update_item_color()
            table_focus_item = self.table_of_instruments.get_table_item_focused()
            self.controller.update_instrument_selected(table_focus_item)
