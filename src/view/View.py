#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import tkinter as tk
import logging

from src.view.widgets_in_vertical_1 import setup_vertical_frame_1
from src.view.widgets_in_vertical_2 import setup_vertical_frame_2
from src.view.widgets_in_vertical_3 import setup_vertical_frame_3

class View(tk.Frame):
    """This is the view of the application. It is the interface between
       the user and the model.

       The View contains widgets and plots, and communicates any interactions
       with the view to the controller
    """
    def __init__(self, tk_frame):
        logging.debug("View: __init__")

        tk_frame.geometry("800x600")

        super().__init__(tk_frame)

        # placeholder for controller
        self.controller = None

        setup_vertical_frame_1(self)
        setup_vertical_frame_2(self, tk_frame)
        setup_vertical_frame_3(self)


    def set_controller(self, controller):
        logging.debug("View: set_controller")
        self.controller = controller

    def update_fee_status(self):
        logging.debug("View: update_fee_status")
        self.controller.update_fee_status(self.checkbutton_fee_state.get())
    
    def update_years_histogram_interval(self):
        logging.debug("View: update_years_histogram_interval")
        value = int(self.spin_years.get())
        self.controller.update_years_histogram_interval(value)

    def update_loan(self):
        logging.debug("View: update_loan")
        value = int(self.spin_loan.get())
        self.controller.update_loan(value / 100)
        # TODO not fully implemented (hist)

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

    def update_variance_calc_sample_size(self):
        logging.debug("View: update_variance_calc_sample_size")
        value = int(self.spin_variance_calc_sample_size.get())
        self.controller.update_variance_calc_sample_size(value)

    def update_volatility_strategie_sample_size(self):
        logging.debug("View: update_volatility_strategie_sample_size")
        value = int(self.spin_volatility_strategie_sample_size.get())
        self.controller.update_volatility_strategie_sample_size(value)

    def update_volatility_strategie_level(self):
        logging.debug("View: update_volatility_strategie_level")
        value = float(self.spin_volatility_strategie_level.get().replace(",", "."))
        self.controller.update_volatility_strategie_level(value)
   

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
        logging.debug("View: update_time_limits")
        self.controller.set_time_limits(from_time, to_time)

    def update_table_of_statistics(self, key_values):
        self.table_of_statistics.set_table(key_values)
