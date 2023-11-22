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

column_title_leverage_1 = "Leverage 1"

class Table_of_instuments():
    def __init__(self, view, frame):
        self.view = view
        self.selected_cels = [] #Cell index is in list if selected.
        self.table = Color_data_table(
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
                **get_styling()
            )
        self.table.bind(on_row_press=self.select_cell)
        frame.add_widget(self.table)
    
    def get_row_and_column_from_cell(self, cell):
        cell_nr = cell.index
        nbr_table_columns = len(self.table.column_data)
        column = cell_nr%nbr_table_columns
        row = int(cell_nr/nbr_table_columns)

        return [row, column]


    def select_cell(self, instance_table, cell):
        row, column = self.get_row_and_column_from_cell(cell)
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
            logging.error("""Table_of_instruments, get_leverage_from_cell:
                           Error in column title of selected cell""") 


    def get_market_from_cell(self, instance_table, cell):

        row_num = int(cell.index/len(instance_table.column_data))
        row_data = instance_table.row_data[row_num]
        return row_data[1]

    def update_color_on_press(self, cell):
        row_nbr, column_nbr = self.get_row_and_column_from_cell(cell)
        #current_color = cell.background_color_selected_cell

        if cell.index in self.selected_cels:
            self.selected_cels.remove(cell.index)
            prev_row = list(self.table.row_data[row_nbr])
            prev_row[column_nbr] = ''
            self.table.row_data[row_nbr] = tuple(prev_row)
        else :
            self.selected_cels.append(cell.index)
            prev_row = list(self.table.row_data[row_nbr])
            prev_row[column_nbr] = ("checkbox-marked-circle",[39 / 256, 174 / 256, 96 / 256, 1],"")
            self.table.row_data[row_nbr] = tuple(prev_row)
            

    def set_table(self, names, countries):
        logging.debug("table_of_instruments: set_table")

        all_item_texts=[]
        added_new_item = False

        for market_name, country in zip(names, countries):
            #only add if market not in table
            if market_name not in all_item_texts:
                added_new_item = True
                all_item_texts.append((country, market_name, '', '', '', ''))
        
        if added_new_item:
            self.table.row_data=all_item_texts
  