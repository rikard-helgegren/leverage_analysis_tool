#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import tkinter as tk
from tkinter import ttk
import logging
import src.model.constants as constants

class Table_Of_Instuments:
    def __init__(self, super_frame, view_object):

        self.view_object = view_object

        frame = tk.Frame(super_frame, padx=5, pady=5)
        frame.pack()

        #scrollbar
        scroll = tk.Scrollbar(frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ('country', 'leverage')

        self.table = tk.ttk.Treeview(frame,
                                     yscrollcommand=scroll.set,
                                     columns=columns,
                                     selectmode="extended")
        self.table.heading('#0', text='Market')
        self.table.heading('country', text='Country')
        self.table.heading('leverage', text='Leverage')
        self.table.pack()
        self.table.bind('<<TreeviewSelect>>', self.update_table_item_focused)


        # Define the row colors with a tag
        self.table.tag_configure("selected_row", background="green")
        self.table.tag_configure("not_selected_row", background="white")

        self.rows_unfolded = []


    def set_table(self, names, countries):
        logging.debug("table_of_instruments: set_table")

        all_item_values = self.get_all_item_values()
        all_item_texts = self.get_all_item_texts()

        added_new_item = False

        for market_name, country in zip(names, countries):
            #only add if market not in table
            if market_name not in all_item_texts:

                added_new_item = True

                self.table.insert(parent='', index=tk.END, iid=market_name, text=market_name, values=(country,1))
                for i in range(2,constants.HIGHEST_LEVERAGE_AVAILABLE + 1): #leverage span
                    self.table.insert(parent=market_name, index=tk.END, text=market_name, values=(country,i))

        if added_new_item:
            self.update_unfolding_status()


    def get_table_item_focused(self):
        logging.debug("table_of_instruments: get_table_item_focused")
        cur_item = self.table.focus()
        item = self.table.item(cur_item)

        return [item['text'], item['values'][1]] #market index and leverage


    def update_item_color(self):
        logging.debug("table_of_instruments: update_item_color")

        cur_item = self.table.focus()
        current_item_tag = self.table.item(cur_item)["tags"]

        if current_item_tag != ['selected_row']:
            self.table.item(cur_item, tag="selected_row")
        else:
            self.table.item(cur_item, tag="not_selected_row")


    def get_all_item_texts(self):
        logging.debug("table_of_instruments: get_all_item_texts")

        all_item_texts = []

        for item in self.table.get_children():
            item_text = self.table.item(item)['text']
            all_item_texts.append(item_text)

        return all_item_texts


    def get_all_item_values(self):
        logging.debug("table_of_instruments: get_all_item_values")

        all_item_values = []

        for item in self.table.get_children():
            item_value = self.table.item(item)['values']
            all_item_values.append(item_value[0]) # TODO update when adding bull > 1

        return all_item_values


    def update_unfolding_status(self):
        logging.debug("View: update_unfolding_status")

        rows_folding_status = []
        for item in self.table.get_children():
            item =  self.table.item(item)['open']

            rows_folding_status.append(item)
        self.rows_unfolded = rows_folding_status


    def only_did_unfolding(self):
        rows_folding_status = []
        for item in self.table.get_children():
            item =  self.table.item(item)['open']

            rows_folding_status.append(item)


        if rows_folding_status == self.rows_unfolded:
            # Folding sattus unchanged, action was no unfolding
            self.rows_unfolded = rows_folding_status
            return False
        else:
            # Folding sattus changed, action was an unfolding
            self.rows_unfolded = rows_folding_status
            return True



    def update_table_item_focused(self, _ ):
        #TODO move parts of code to the table class and rename method
        logging.debug("View: table_item_focused")

        did_unfolding = self.only_did_unfolding()

        if did_unfolding:
            #An item was only unfolded do nothing
            return
        else:
            #An item was selected update view
            self.update_item_color()
            table_focus_item = self.get_table_item_focused()
            self.view_object.update_instrument_selected(table_focus_item)

