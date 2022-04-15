

import tkinter as tk


from code.view.histogram import Histogram
from code.view.line_graph_full_time import Line_Graph_Full_Time
from code.view.table_of_instruments import Table_Of_Instuments
from code.view.widgets_in_vertical_1 import setup_vertical_frame_1
from code.view.table_of_statistics import Table_Of_Statistics


class View(tk.Frame):
    """This is the view of the application. It is the interface between
       the user and the model.

       The View contains widgets and plots, and communicates any interactions
       with the view to the controller
    """
    def __init__(self, parent):
        print("TRACE: View: __init__")

        super().__init__(parent)

        # placeholder for controller
        self.controller = None

        #############
        # Vertical 1
        #############

        self.vertical_frame_1 = tk.Frame(self, padx=5, pady=5)
        self.vertical_frame_1.pack(side=tk.LEFT)

        setup_vertical_frame_1(self, self.vertical_frame_1)

        #############
        # Vertical 2
        #############

        self.vertical_frame_2 = tk.Frame(self, padx=5, pady=5)
        self.vertical_frame_2.pack(side=tk.LEFT)

        self.histogram = Histogram(self.vertical_frame_2)
        """ The histogram displays a distribution of outcomes from all continuous
            time intervals of the selected length.
        """

        self.line_graph_full_time = Line_Graph_Full_Time(self.vertical_frame_2)
        """ This line graph displays the performance of the created portfolio
            for the full time span available
        """

        #############
        # Vertical 3
        #############

        self.vertical_frame_3 = tk.Frame(self, padx=5, pady=5)
        self.vertical_frame_3.pack(side=tk.LEFT)

        self.table_of_instruments = Table_Of_Instuments(self.vertical_frame_3, self)
        """ The table of instruments is a table from which the user can select
            instruments with or without leverage to use in their portfolio
        """

        self.table_of_statistics = Table_Of_Statistics(self.vertical_frame_3)


        #############
        # Vertical 4
        #############


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
    
    def update_years_investigating(self):
        print("TRACE: View: updatupdate_years_investigatinge_limit")
        value = int(self.spin_years.get())
        self.controller.update_years_investigating(value)

    def update_loan(self, value):
        print("TRACE: View: update_loan")
        tk.messagebox.showinfo('Error', 'Not fully implemented')

    def update_amount_leverage(self, value):
        print("TRACE: View: update_amount_leverage")
        self.controller.set_update_amount_leverage(value)
        #TODO

    def update_rebalance_status(self):
        print("TRACE: View: update_rebalance_status", self.checkbutton_rebalance_state.get())
        tk.messagebox.showinfo('Error', 'Not fully implemented')
        self.checkbutton_rebalance_state.get()
        # TODO

    def draw_histogram(self, data):
        print("TRACE: View: draw_histogram")
        self.histogram.draw(data)

    def draw_line_graph(self, values, time_span):
        print("TRACE: View: draw_line_graph")
        self.line_graph_full_time.draw(values, time_span)

    def set_table_of_instruments(self, names, countries):
        print("TRACE: View: set_market_table")
        self.table_of_instruments.set_table(names, countries)
        
    def update_instrument_selected(self, table_focus_item):
        print("TRACE: View: table_item_focused")
        self.controller.update_instrument_selected(table_focus_item)
