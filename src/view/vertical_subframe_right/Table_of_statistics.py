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

class Table_of_statistics():
    def __init__(self, view, frame):
        self.table = MDDataTable(
            rows_num=100,
            column_data=[
                ("Metrics", dp(40)),
                ("Value", dp(30)),
            ],
            row_data=[],
            sorted_order="ASC",
            elevation=0
        )
        frame.add_widget(self.table)

    def set_table(self, stats_dict):
        """Add all the statistics to the table"""
        logging.debug("View: Table_of_statistics: set_table")
        row_data=[]

        for i, key in enumerate(stats_dict):
            row_data.append((key,stats_dict[key]))

        self.table.row_data = row_data
