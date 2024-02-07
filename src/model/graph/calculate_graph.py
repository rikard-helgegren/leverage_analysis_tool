#!/usr/bin/env python3
#
# Copyright (C) 2024 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

from src.model.common.is_data_empty import is_data_empty
from src.model.graph.graph_cpp_adapter import graph_ctypes
import logging

def calculate_graph(model):
    """
        The main function for calculating the values of the portfolio shown in the graph.
    """
    logging.debug("Model: calculate_graph")

    markets_selected     = model.get_markets_selected()
    instruments_selected = model.get_instruments_selected()

    if is_data_empty(instruments_selected, markets_selected):
        model.set_portfolio_results_full_time([])
        return

    return_data = graph_ctypes(model)
    model.set_portfolio_results_full_time(return_data)
