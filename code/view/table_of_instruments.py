
from tkinter import *

def __init__(self):
    frame = Frame(self, padx=5, pady=5)
    frame.pack(side=LEFT)
    #scrollbar
    game_scroll = Scrollbar(frame)
    game_scroll.pack(side=RIGHT, fill=Y)

    columns = ('index', 'country', 'leverage')

    self.market_table = ttk.Treeview(frame,yscrollcommand=game_scroll.set, xscrollcommand =game_scroll.set, columns=columns, show='headings')
    self.market_table.heading('index', text='Index')
    self.market_table.heading('country', text='Country')
    self.market_table.heading('leverage', text='Leverage')
    self.market_table.pack()
    self.market_table.bind('<<TreeviewSelect>>',self.update_table_item_focused)

def set_market_table(self, markets):
    print("TRACE: table_of_instruments: set_market_table")

    all_item_values = get_all_item_values(self)

    for market in markets:
        #only add if not all ready there
        if market not in all_item_values:
            self.market_table.insert(parent='', index=END, values=(market, 'not known',1))

def get_table_item_focused(self):
    print("TRACE: table_of_instruments: get_table_item_focused")
    curItem = self.market_table.focus()
    return self.market_table.item(curItem)['values']

def get_all_item_values(self):
    print("TRACE: table_of_instruments: get_all_item_values")

    all_item_values = []

    for item in self.market_table.get_children():
        item_value = self.market_table.item(item)['values']
        all_item_values.append(item_value[0]) # TODO update when adding bull > 1

    return all_item_values

