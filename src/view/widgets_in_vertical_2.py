#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import tkinter as tk

from src.view.setup_time_limiters import setup_time_limiters
from src.view.histogram import Histogram
from src.view.line_graph_full_time import Line_Graph_Full_Time


def setup_vertical_frame_2(view):
    view.vertical_frame_2 = tk.Frame(view, padx=5, pady=5)
    view.vertical_frame_2.pack(side=tk.LEFT)

    view.histogram = Histogram(view.vertical_frame_2)
    """ The histogram displays a distribution of outcomes from all continuous
        time intervals of the selected length.
    """

    view.line_graph_full_time = Line_Graph_Full_Time(view.vertical_frame_2)
    """ This line graph displays the performance of the created portfolio
        for the full time span available
    """

    setup_time_limiters(view, view.vertical_frame_2)