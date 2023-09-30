#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

from kivy.metrics import dp

from kivymd.uix.datatables import MDDataTable

class Table_of_statistics():
    def __init__(self, view, frame):
        self.table = MDDataTable(
            rows_num=100,
            column_data=[
                ("Metrics", dp(20)),
                ("Value", dp(30)),
            ],
            row_data=[
                (
                    "Mean",
                    "1",
                ),
                (
                    "Median",
                    "1",
                ),
                (
                    "Risk",
                    "1",
                ),
                (
                    "Dounut",
                    "1",
                ),
                (
                    "Mean",
                    "1",
                ),
                (
                    "Median",
                    "1",
                ),
                (
                    "Risk",
                    "1",
                ),
                (
                    "Dounut",
                    "1",
                ),
                (
                    "Mean",
                    "1",
                ),
                (
                    "Median",
                    "1",
                ),
                (
                    "Risk",
                    "1",
                ),
                (
                    "Dounut",
                    "1",
                ),
            ],
            sorted_on="Contry",
            sorted_order="ASC",
            elevation=0
        )
        frame.add_widget(self.table)