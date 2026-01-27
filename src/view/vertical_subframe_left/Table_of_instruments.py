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
class Table_of_instruments:
    def __init__(self, view, frame):
        logging.debug("Table_of_instruments: __init__")

        self.view = view
        self.config = Config()

        self.selected_cells: set[int] = set()
        self.current_table_key = 0

        # { key: { "Table": table, "Selected_cells": set[int] } }
        self.table_cache: dict[int, dict] = {}

        self.index_names = []
        self.index_countries = []

        self.portfolio_selection_frame = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.2)
        )

        self.table_main_frame = BoxLayout(
            orientation='vertical',
            size_hint=(1, 1)
        )

        Portfolio_tab(self, self.portfolio_selection_frame)
        self.table_main_frame.add_widget(self.portfolio_selection_frame)

        self.generate_column_data()
        # Pre-create two tables and show only the first. This allows
        # fast switching between portfolio 0 and 1 without rebuilding.
        self.generate_and_set_new_table(self.current_table_key, add_to_view=True)
        self.generate_and_set_new_table(1, add_to_view=False)

        frame.add_widget(self.table_main_frame)

    # ------------------------------------------------------------------

    def generate_column_data(self):
        logging.debug("Table_of_instruments: generate_column_data")

        self.column_data = [
            ("Country", dp(30)),
            ("Index", dp(20)),
            (column_title_leverage_1, dp(20)),
        ]

        for i in range(2, self.config.HIGHEST_LEVERAGE_AVAILABLE + 1):
            self.column_data.append((str(i), dp(10)))

    # ------------------------------------------------------------------

    def generate_and_set_new_table(self, table_key, add_to_view=True):
        logging.debug("Table_of_instruments: generate_and_set_new_table")

        new_table = Color_data_table(
            rows_num=100,
            column_data=self.column_data,
            row_data=[],
            **get_styling()
        )

        # populate the new table with current index data
        new_table.row_data = []
        # bind selection handler
        new_table.bind(on_row_press=self.select_cell)

        if add_to_view:
            # make this table the active widget and reference
            self.table = new_table
            self.set_instruments_in_table(self.index_names, self.index_countries)
            self.table_main_frame.add_widget(self.table)
        else:
            # store without changing the visible `self.table`
            # but still initialize its rows so it's ready when swapped in
            new_table.row_data = []

        self.table_cache[table_key] = {
            "Table": new_table,
            "Selected_cells": set()
        }

        # Only update the currently visible table key when this table
        # was actually added to the view.
        if add_to_view:
            self.current_table_key = table_key

    # ------------------------------------------------------------------

    def change_selected_portfolio(self, new_portfolio_key):
        logging.debug("Table_of_instruments: change_selected_portfolio")

        self.table_main_frame.remove_widget(
            self.table_cache[self.current_table_key]["Table"]
        )

        self.table_cache[self.current_table_key]["Selected_cells"] = self.selected_cells

        if new_portfolio_key in self.table_cache:
            cached = self.table_cache[new_portfolio_key]
            self.table = cached["Table"]
            self.selected_cells = cached["Selected_cells"]
            self.table_main_frame.add_widget(self.table)
            self.current_table_key = new_portfolio_key
        else:
            self.generate_and_set_new_table(new_portfolio_key)
            self.selected_cells = set()

    # ------------------------------------------------------------------

    def calc_row_and_column_from_cell_index(self, cell_index):
        nbr_columns = len(self.table.column_data)
        row = cell_index // nbr_columns
        column = cell_index % nbr_columns
        return row, column

    # ------------------------------------------------------------------

    def select_cell(self, instance_table, cell):
        logging.debug("Table_of_instruments: select_cell")

        if cell.text:
            return

        row, column = self.calc_row_and_column_from_cell_index(cell.index)
        self.update_color_on_press(cell.index)

        leverage = self.extract_leverage_from_cell(instance_table, cell)
        market = self.extract_market_from_cell(instance_table, cell)

        self.view.update_instrument_selected((market, leverage))

    # ------------------------------------------------------------------

    def extract_leverage_from_cell(self, instance_table, cell):
        nbr_columns = len(instance_table.column_data)
        selected_col = cell.index % nbr_columns
        column_title = instance_table.column_data[selected_col][0]

        if column_title == column_title_leverage_1:
            return 1
        if column_title.isdigit():
            return int(column_title)

        logging.error(
            "Table_of_instruments: Invalid leverage column title: %s",
            column_title
        )
        return None

    # ------------------------------------------------------------------

    def extract_market_from_cell(self, instance_table, cell):
        row = cell.index // len(instance_table.column_data)
        return instance_table.row_data[row][1]

    # ------------------------------------------------------------------

    def update_color_on_press(self, cell_index):
        logging.debug("Table_of_instruments: update_color_on_press")

        row, column = self.calc_row_and_column_from_cell_index(cell_index)
        row_data = self.table.row_data[row]

        if cell_index in self.selected_cells:
            self.selected_cells.remove(cell_index)
            row_data[column] = ''
        else:
            self.selected_cells.add(cell_index)
            row_data[column] = (
                "checkbox-marked-circle",
                instrument_table_check_color,
                ""
            )

        self.table.row_data[row] = row_data

    # ------------------------------------------------------------------

    def remove_selectons(self):
        logging.debug("Table_of_instruments: remove_selections")

        for cell_index in self.selected_cells:
            row, column = self.calc_row_and_column_from_cell_index(cell_index)
            row_data = self.table.row_data[row]
            row_data[column] = ''
            self.table.row_data[row] = row_data

        self.selected_cells.clear()

    def update_selected_view(self, model_nbr):
        logging.debug("Table_of_instruments: update_selected_view")

        # Switch to requested portfolio/table if needed
        if model_nbr != self.current_table_key:
            self.change_selected_portfolio(model_nbr)


    def set_instruments_in_table(self, names, countries):
        logging.debug("Table_of_instruments: set_instruments_in_table")

        self.index_names = names
        self.index_countries = countries

        rows = []
        seen_markets = set()
        empty_cells = [''] * self.config.HIGHEST_LEVERAGE_AVAILABLE

        for market_name, country in zip(names, countries):
            if market_name not in seen_markets:
                seen_markets.add(market_name)
                rows.append([country, market_name] + empty_cells)

        if not rows:
            return

        nbr_columns = len(self.column_data)

        # For each cached table we must give it an independent copy of the rows
        for key, entry in self.table_cache.items():
            try:
                entry_table = entry.get("Table")
                if entry_table is None:
                    continue

                # Make shallow copies of each row (enough because rows are lists of simple values)
                entry_table.row_data = [r.copy() for r in rows]

                # Re-apply any stored selected cells for this table so visuals match state
                selected = entry.get("Selected_cells", set())
                for cell_index in selected:
                    row_idx = cell_index // nbr_columns
                    col_idx = cell_index % nbr_columns
                    if 0 <= row_idx < len(entry_table.row_data) and 0 <= col_idx < nbr_columns:
                        row_data = list(entry_table.row_data[row_idx])
                        row_data[col_idx] = ("checkbox-marked-circle", instrument_table_check_color, "")
                        entry_table.row_data[row_idx] = row_data
            except Exception:
                pass

        # Also ensure the visible `self.table` is populated (if not already the same object)
        if hasattr(self, 'table') and self.table is not None:
            # if the visible table is in cache, it was already populated above
            in_cache = any(entry.get("Table") is self.table for entry in self.table_cache.values())
            if not in_cache:
                self.table.row_data = [r.copy() for r in rows]
