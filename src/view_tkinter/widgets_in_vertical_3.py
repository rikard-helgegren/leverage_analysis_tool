#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import tkinter as tk


from src.view.table_of_statistics import Table_Of_Statistics
from src.view.table_of_instruments import Table_Of_Instuments


def setup_vertical_frame_3(view):

        view.vertical_frame_3 = tk.Frame(view, padx=5, pady=5)
        view.vertical_frame_3.pack(side=tk.LEFT)

        view.table_of_instruments = Table_Of_Instuments(view.vertical_frame_3, view)
        """ The table of instruments is a table from which the user can select
            instruments with or without leverage to use in their portfolio
        """

        view.table_of_statistics = Table_Of_Statistics(view.vertical_frame_3)
