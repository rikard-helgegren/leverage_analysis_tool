#!/usr/bin/env python3
#
# Copyright (C) 2024 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout

from src.view.styling.light_mode.table import get_styling
from src.view.vertical_subframe_left.Portfolio_tab import Portfolio_tab
from src.view.styling.light_mode.Color_data_table import Color_data_table
from src.view.styling.light_mode.color_palet import *
from src.Config import Config

column_title_leverage_1 = "Leverage 1"
COLUMNS_BEFORE_LEVERAGES = 2

class Table_of_instruments():
    def __init__(self, view, frame):
        logging.debug("table_of_instruments: __init__")
        self.view = view
        self.selected_cells = [] #Cell index is in list if selected.
        self.config = Config()
        self.current_tabe_key = 0
        self.table_cache = {} # {Key: {Table: table, Selected_cells: selected_cels}}
        self.index_names = []
        self.index_countries = []

        self.table_main_frame = BoxLayout(
                orientation='vertical', 
                size_hint=(1, 1))
        
        self.portfolio_selection_frame = BoxLayout(
                orientation='horizontal',
                size_hint=(1, 0.2))
        
        Portfolio_tab(self, self.portfolio_selection_frame)
        self.table_main_frame.add_widget(self.portfolio_selection_frame)

        self.generate_column_data()
        self.generate_and_set_new_table(self.current_tabe_key)

        frame.add_widget(self.table_main_frame)

    def generate_column_data(self):
        logging.debug("table_of_instruments: generate_column_data")
        self.column_data=[
                ("Contry", dp(30)),
                ("Index", dp(20)),
                (column_title_leverage_1, dp(20))]

        # auto fill column titles
        for i in range(2,self.config.HIGHEST_LEVERAGE_AVAILABLE + 1): 
            self.column_data.append([str(i),dp(10)])

    def generate_and_set_new_table(self, table_key):
        logging.debug("table_of_instruments: generate_and_set_new_table")
        self.table = Color_data_table(
                rows_num=100,
                column_data=self.column_data,
                row_data=[],
                **get_styling()
            )
        self.set_instruments_in_table(self.index_names, self.index_countries)
        self.table.bind(on_row_press=self.select_cell)
        
        self.table_main_frame.add_widget(self.table)

        self.table_cache[table_key] = {"Table": self.table, "Selected_cells": []}

        self.current_tabe_key = table_key

    def change_selected_portfolio(self, new_portfolio_key): 
        """This implementation is sub optimal but due to slow updates of table cell values, is the best implementation
        for changing the table in acordance with a change of selected portfolio. 
        """
        logging.debug("table_of_instruments: change_selected_portfolio")

        self.table_main_frame.remove_widget(self.table_cache[self.current_tabe_key]["Table"])
        self.table_cache[self.current_tabe_key]["Selected_cells"] = self.selected_cells
        
        if new_portfolio_key in self.table_cache.keys():
            self.table = self.table_cache[new_portfolio_key]["Table"]
            self.selected_cells = self.table_cache[new_portfolio_key]["Selected_cells"]
            self.table_main_frame.add_widget(self.table)
            self.current_tabe_key = new_portfolio_key
            
        else:
            self.generate_and_set_new_table(new_portfolio_key)
            self.selected_cells = []
           

    def calc_row_and_column_from_cell_index(self, cell_nbr):
        logging.debug("table_of_instruments: calc_row_and_column_from_cell_index")
        nbr_table_columns = len(self.table.column_data)
        column = cell_nbr % nbr_table_columns
        row = int(cell_nbr / nbr_table_columns)

        return [row, column]

    def select_cell(self, instance_table, cell):
        logging.debug("table_of_instruments: select_cell")
        row, column = self.calc_row_and_column_from_cell_index(cell.index)
        if cell.text == '':
            self.update_color_on_press(cell.index)

            leverage = self.extract_leverage_from_cell(instance_table, cell)
            market = self.extract_market_from_cell(instance_table, cell)  

            self.view.update_instrument_selected([market, leverage])

    def extract_leverage_from_cell(self, instance_table, cell):
        logging.debug("table_of_instruments: extract_leverage_from_cell")
        nbr_of_colums = len(instance_table.column_data)

        selected_col = cell.index%nbr_of_colums
        coloumn_title = instance_table.column_data[selected_col][0]

        if coloumn_title == column_title_leverage_1:
            return 1
        elif coloumn_title.isdigit() == 1:
            return int(coloumn_title)
        else:
            logging.error("""Table_of_instruments, extract_leverage_from_cell:
                           Error in column title of selected cell""") 

    def extract_market_from_cell(self, instance_table, cell):
        logging.debug("table_of_instruments: extract_market_from_cell")
        row_num = int(cell.index/len(instance_table.column_data))
        row_data = instance_table.row_data[row_num]
        return row_data[1]

    def update_color_on_press(self, cell_index):
        logging.debug("table_of_instruments: update_color_on_press")
        row_nbr, column_nbr = self.calc_row_and_column_from_cell_index(cell_index)
        #current_color = cell.background_color_selected_cell

        if cell_index in self.selected_cells:
            self.selected_cells.remove(cell_index)
            prev_row = self.table.row_data[row_nbr]
            prev_row[column_nbr] = ''
            self.table.row_data[row_nbr] = prev_row #TODO: time consuming 0.9 sec for each call, four times
        else :
            self.selected_cells.append(cell_index)
            prev_row = self.table.row_data[row_nbr]
            prev_row[column_nbr] = ("checkbox-marked-circle", instrument_table_check_color,"")
            self.table.row_data[row_nbr] = prev_row  #TODO: time consuming 0.9 sec for each call, four times
   
    def clear_old_and_set_new_selected_instruments(self, selected_instruments, model_nbr):
        logging.debug("Table_of_instruments: clear_old_and_set_new_selected_instruments")
        self.change_selected_portfolio(model_nbr)
  
    def get_row_nbr_for_instrument_index_name(self, index_name):
        logging.debug("Table_of_instruments: get_row_nbr_for_instrument_index_name")
        for row_number, row in enumerate(self.table.row_data):
            index_name_of_row = row[1]

            if index_name_of_row == index_name:
                return row_number
    
    def add_marker_to_variable_selected_cells(self, row_nbr, column_nbr):
        logging.debug("Table_of_instruments: add_marker_to_variable_selected_cells")
        nbr_table_columns = len(self.table.column_data)
        cell_nbr = nbr_table_columns * row_nbr + column_nbr
        self.selected_cells.append(cell_nbr)
         
    def remove_selectons(self):
        logging.debug("Table_of_instruments: remove_selectons")
        for cell_index in self.selected_cells:
            row_nbr, column_nbr = self.calc_row_and_column_from_cell_index(cell_index)

            prev_row = self.table.row_data[row_nbr]
            prev_row[column_nbr] = ''
            self.table.row_data[row_nbr] = prev_row #TODO: time consuming 0.9 sec for each call, four times
        
        self.selected_cells = []

    def set_instruments_in_table(self, names, countries):
        logging.debug("table_of_instruments: set_instruments_in_table")

        self.index_names = names
        self.index_countries = countries

        all_item_texts=[]
        added_new_item = False
        number_of_empty_strings = self.config.HIGHEST_LEVERAGE_AVAILABLE

        for market_name, country in zip(names, countries):
            #only add if market not in table
            if market_name not in all_item_texts:
                added_new_item = True
                all_item_texts.append([country, market_name] + [''] * number_of_empty_strings)
        
        if added_new_item:
            self.table.row_data=all_item_texts
    
    """ DEPRICATED REMOVE 2025
    def set_selected_instruments(self, selected_instruments):
        logging.debug("Table_of_instruments: set_selected_instruments")
        for instrument, leverage in selected_instruments:
            row_nbr_for_instrument = self.get_row_nbr_for_instrument_index_name(instrument) 
            column_number = leverage -1 + COLUMNS_BEFORE_LEVERAGES # -1 due to 0 indexing
            self.set_selected_marker(row_nbr_for_instrument, column_number)
    
          
    def set_selected_marker(self, row_nbr, column_nbr):
        logging.debug("Table_of_instruments: set_selected_marker")
        self.add_marker_to_variable_selected_cells(row_nbr, column_nbr)
        prev_row = self.table.row_data[row_nbr]
        prev_row[column_nbr] = ("checkbox-marked-circle", instrument_table_check_color,"")
        self.table.row_data[row_nbr] = prev_row #TODO: time consuming 0.9 sec for each call, occurs four times
    """