#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable

from src.view.styling.light_mode.table import get_styling
from src.view.styling.light_mode.Color_data_table import Color_data_table

class Table_of_statistics():
    def __init__(self, view, frame):
        self.table = Color_data_table(
            rows_num=100,
            column_data=[
                ("Metrics", dp(40)),
                ("Value", dp(30)),
            ],
            row_data=[],
            sorted_order="ASC",
            **get_styling()
        )
        frame.add_widget(self.table)

    def set_table(self, stats_dict):
        """Add all the statistics to the table"""
        logging.debug("View: Table_of_statistics: set_table")
        row_data=[]

        for i, key in enumerate(stats_dict):
            row_data.append((key,stats_dict[key]))

        self.table.row_data = row_data
