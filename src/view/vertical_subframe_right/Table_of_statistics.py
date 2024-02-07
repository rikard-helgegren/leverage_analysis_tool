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

from src.view.styling.light_mode.table import get_styling
from src.view.styling.light_mode.Color_data_table import Color_data_table

class Table_of_statistics():
    def __init__(self, view, frame):
        self.frame = frame
        self.use_refence = False
        self.change_table = False

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

        self.stats_dict_list = [] #list of dicts

    def set_table(self, stats_dict_list):
        logging.debug("View: Table_of_statistics: set_table")

        self.stats_dict_list = stats_dict_list

        self._set_table()

    def _set_table(self):
        """Add all the statistics to the table"""
        row_data=[]
        self.frame.remove_widget(self.table)

        match len(self.stats_dict_list):
            case 1:
                self.table = Color_data_table(
                    rows_num=100,
                    column_data=[
                        ("Metrics", dp(40)),
                        ("Portfolio 1", dp(30))
                    ],
                    row_data=[],
                    sorted_order="ASC",
                    **get_styling()
                )

                for i, key in enumerate(self.stats_dict_list[0]):
                    row_data.append((key,self.stats_dict_list[0][key]))
            case 2:
                self.table = Color_data_table(
                    rows_num=100,
                    column_data=[
                        ("Metrics", dp(30)),
                        ("Portfolio 1", dp(20)),
                        ("Portfolio 2", dp(20))
                    ],
                    row_data=[],
                    sorted_order="ASC",
                    **get_styling()
                 )
                
                for i, key in enumerate(self.stats_dict_list[0]):
                    row_data.append((key, self.stats_dict_list[0][key], self.stats_dict_list[1][key]))
            case _:
                logging.warn("Table_of_statistics: Cant generate statistics for '%r' portfolios", len(self.stats_dict_list))

        self.table.row_data = row_data
        self.frame.add_widget(self.table)
