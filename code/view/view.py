
import tkinter as tk
import logging


from code.view.histogram import Histogram
from code.view.line_graph_full_time import Line_Graph_Full_Time
from code.view.table_of_instruments import Table_Of_Instuments
from code.view.widgets_in_vertical_1 import setup_vertical_frame_1
from code.view.table_of_statistics import Table_Of_Statistics
from code.view.setup_time_limiters import setup_time_limiters


class View(tk.Frame):
    """This is the view of the application. It is the interface between
       the user and the model.

       The View contains widgets and plots, and communicates any interactions
       with the view to the controller
    """
    def __init__(self, parent):
        logging.debug("View: __init__")

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

        setup_time_limiters(self, self.vertical_frame_2)

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
        logging.debug("View: set_controller")
        self.controller = controller

    def update_fee_status(self):
        logging.debug("View: update_fee_status")
        self.controller.update_fee_status(self.checkbutton_fee_state.get())
        tk.messagebox.showinfo('Error', 'Not fully implemented')
    
    def update_years_histogram_interval(self):
        logging.debug("View: update_years_histogram_interval")
        value = int(self.spin_years.get())
        self.controller.update_years_histogram_interval(value)

    def update_harvest_point(self):
        logging.debug("View: update_harvest_point")
        value = int(self.spin_harvest_point.get())
        self.controller.update_harvest_point(value)

    def update_refill_point(self):
        logging.debug("View: update_refill_point")
        value = int(self.spin_refill_point.get())
        self.controller.update_refill_point(value)

    def update_rebalance_point(self):
        logging.debug("View: update_rebalance_point")
        value = int(self.spin_rebalance_point.get())
        self.controller.update_rebalance_point(value)



    def update_loan(self):
        logging.debug("View: update_loan")
        value = int(self.spin_loan.get())
        self.controller.update_loan(value/100)
        # TODO not fully implemented

    def update_amount_leverage(self, value):
        logging.debug("View: update_amount_leverage")
        self.controller.set_update_amount_leverage(value)

    def draw_histogram(self, data):
        logging.debug("View: draw_histogram")
        self.histogram.draw(data)

    def draw_line_graph(self, values, time_span):
        logging.debug("View: draw_line_graph")
        self.line_graph_full_time.draw(values, time_span)

    def set_table_of_instruments(self, names, countries):
        logging.debug("View: set_market_table")
        self.table_of_instruments.set_table(names, countries)
        
    def update_instrument_selected(self, table_focus_item):
        logging.debug("View: table_item_focused")
        self.controller.update_instrument_selected(table_focus_item)

    def update_strategy_selected(self, menu_focus_item):
        self.controller.update_strategy_selected(menu_focus_item)

    def update_time_limits(self, from_time, to_time):
        logging.debug("View: update_time_limits, needs implementing")
        self.controller.set_time_limits(from_time, to_time)

    def update_table_of_statistics(self, key_values):
        self.table_of_statistics.set_table(key_values)
