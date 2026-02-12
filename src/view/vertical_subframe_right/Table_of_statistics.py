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
from kivy.core.window import Window

from src.view.styling.light_mode.table import get_styling
from src.view.styling.light_mode.Color_data_table import Color_data_table
from src.view.styling import formatting

class Table_of_statistics():
    style_scaler = 0.04 # Adjust this to scale the table for better fit on different screen sizes
    def __init__(self, view, frame):
        logging.debug("View: Table_of_statistics: __init__")
        Window.bind(on_resize=self._on_window_resize)

        self.frame = frame
        self.stats_dict_list = []
        self._current_column_count = None

        self.table = Color_data_table(
            column_data=[("Metrics", dp(40))],  # placeholder
            row_data=[],
            rows_num=50,
            sorted_order="ASC",
            size_hint=(1, 1),
            **get_styling()
        )
        frame.add_widget(self.table)

        self._current_columns = None
    
    def _on_window_resize(self, window, width, height):
        self._set_table()


    def set_table(self, stats_dict_list):
        logging.debug("View: Table_of_statistics: set_table")
        self.stats_dict_list = stats_dict_list
        self._update_table()

    def _update_table(self):
        n = len(self.stats_dict_list)
        if n == 0:
            return

        # If column structure changed → rebuild table
        if n != self._current_column_count:
            self._rebuild_table(n)

        # Safe & cheap
        self.table.row_data = self._build_rows(n)

    def _rebuild_table(self, n):
        # Remove old table
        if self.table:
            self.frame.remove_widget(self.table)

        self.table = Color_data_table(
            rows_num=50,
            column_data=self._get_columns(n),
            row_data=[],  # rows added after
            sorted_order="ASC",
            **get_styling()
        )

        self.frame.add_widget(self.table)
        self._current_column_count = n


    def _get_columns(self, n):
        total_width = Window.width * 0.95  # leave margin, prevents overflow
        total_width = total_width * self.style_scaler #scale factor, can be adjusted for better fit
        if n == 1:
            return [
                (formatting.small_indent_text + "Metrics", total_width*0.55),
                (formatting.small_indent_text + "Portfolio 1", total_width*0.45),
            ]
        elif n == 2:
            return [
                (formatting.small_indent_text + "Metrics", 0.33*total_width),
                (formatting.small_indent_text + "Portfolio 1", 0.33*total_width),
                (formatting.small_indent_text + "Portfolio 2", 0.33*total_width),
            ]
        else:
            logging.warning("Unsupported portfolio count: %s", n)
            return []

    def _build_rows(self, n):
        logging.debug("View: Table_of_statistics: _build_rows")
        rows = []

        keys = self.stats_dict_list[0].keys()

        if n == 1:
            d0 = self.stats_dict_list[0]
            for key in keys:
                rows.append(("  " +key, d0[key]))

        elif n == 2:
            d0, d1 = self.stats_dict_list

            for key in keys:
                rows.append(("  " +key, d0[key], d1[key]))

        return rows


    def _set_table(self):
        logging.debug("View: Table_of_statistics: _set_table")
        """Add all the statistics to the table"""
        total_width = Window.width * 0.95  # leave margin, prevents overflow
        total_width = total_width * self.style_scaler #scale factor, can be adjusted for better fit

        row_data=[]
        self.frame.remove_widget(self.table)

        match len(self.stats_dict_list):
            case 1:
                self.table = Color_data_table(
                    rows_num=100,
                    column_data=[
                        (formatting.small_indent_text + "Metrics", total_width*0.55),
                        ("Portfolio 1", total_width*0.45)
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
                        (formatting.small_indent_text + "Metrics", total_width*0.33),
                        ("Portfolio 1", total_width*0.33),
                        ("Portfolio 2", total_width*0.33)
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
