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

        self.stats_dict = {}
        self.stats_dict_refrence = {}

    def update_refrence(self):
        logging.info("View: Table_of_statistics: update_refrence")

        if self.stats_dict == 0 or self.stats_dict ==  self.stats_dict_refrence: #Not a good check with risk 0 when no values pressent, HACKS
            self.stats_dict_refrence = {}
            
            if self.use_refence == False:
                self.change_table = False
            else:
                self.change_table = True

            self.use_refence = False
        else:
            self.stats_dict_refrence =  self.stats_dict

            if self.use_refence == True:
                self.change_table = False
            else:
                self.change_table = True

            self.use_refence = True
        
        self._set_table()

    def set_table(self, stats_dict):
        logging.debug("View: Table_of_statistics: set_table")

        self.stats_dict = stats_dict

        self._set_table()

    def _set_table(self):
        """Add all the statistics to the table"""
        row_data=[]

        if self.change_table:
            self.frame.remove_widget(self.table)

            if self.use_refence == False:
                self.table = Color_data_table(
                    rows_num=100,
                    column_data=[
                        ("Metrics", dp(40)),
                        ("Value", dp(30))
                    ],
                    row_data=[],
                    sorted_order="ASC",
                    **get_styling()
                )
            else:
                self.table = Color_data_table(
                    rows_num=100,
                    column_data=[
                        ("Metrics", dp(30)),
                        ("Value", dp(20)),
                        ("Refrence\nvalue", dp(20))
                    ],
                    row_data=[],
                    sorted_order="ASC",
                    **get_styling()
                 )


        if  self.stats_dict_refrence != {}:
            for i, key in enumerate(self.stats_dict):
                row_data.append((key,self.stats_dict[key],self.stats_dict_refrence[key]))
        else: 
            for i, key in enumerate(self.stats_dict):
                row_data.append((key,self.stats_dict[key]))

        self.table.row_data = row_data

        if self.change_table:  
            self.frame.add_widget(self.table)
            self.change_table = False
