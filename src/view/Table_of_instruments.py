#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.metrics import dp

from kivymd.uix.datatables import MDDataTable


column_title_leverage_1 = "Leverage 1"
green = [0.0, 0.5019607843137255, 0.0, 1.0]
default_color = [0.05, 0.05, 0.05, 0.05]
default_selected_color = [0.15, 0.15, 0.15, 0.15]

class Table_of_instuments():


    def __init__(self, view, frame):
        self.view = view
        self.table = MDDataTable(
                rows_num=100,
                column_data=[
                    ("Contry", dp(30)),
                    ("Index", dp(20)),
                    (column_title_leverage_1, dp(20)),
                    ("2", dp(10)),
                    ("3", dp(10)),
                    ("4", dp(10)),
                ],
                row_data=[],
                sorted_on="Contry",
                sorted_order="ASC",
                background_color_cell = default_color,
                background_color_selected_cell = default_selected_color,
                elevation=0
            )
        self.table.bind(on_row_press=self.select_cell)
        frame.add_widget(self.table)
    

    def select_cell(self, instance_table, cell):

        if cell.text == '':
            self.update_color_on_press(cell)

            leverage = self.get_leverage_from_cell(instance_table, cell)
            market = self.get_market_from_cell(instance_table, cell)  

            self.view.update_instrument_selected([market, leverage])


    def get_leverage_from_cell(self, instance_table, cell):
        nbr_of_colums = len(instance_table.column_data)

        selected_col = cell.index%nbr_of_colums
        coloumn_title = instance_table.column_data[selected_col][0]

        if coloumn_title == column_title_leverage_1:
            return 1
        elif len(coloumn_title) == 1:
            return int(coloumn_title)
        else:
            logging.error("Table_of_instruments, get_leverage_from_cell: Error in column title of selected cell")
            


    def get_market_from_cell(self, instance_table, cell):

        row_num = int(cell.index/len(instance_table.column_data))
        row_data = instance_table.row_data[row_num]
        return row_data[1]

    def update_color_on_press(self, cell):

        current_color = cell.background_color_selected_cell

        if current_color == green:
            cell.background_color_selected_cell = default_selected_color
            cell.background_color_cell = default_color
        elif cell.text == '' :
            cell.background_color_selected_cell = 'green'
            cell.background_color_cell = 'green'
 


    def set_table(self, names, countries):
        logging.debug("table_of_instruments: set_table")

        #all_item_texts = self.get_all_item_texts()
        all_item_texts=[]

        added_new_item = False

        for market_name, country in zip(names, countries):
            #only add if market not in table
            if market_name not in all_item_texts:

                added_new_item = True

                all_item_texts.append((country, market_name, '', '', '', ''))
        
        if added_new_item:
            self.table.row_data=all_item_texts

                