
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
    self.market_table.bind('<<TreeviewSelect>>',self.table_item_selected)

def set_market_table(self, markets):
    print("TRACE: table_of_instruments: set_market_table")

    for market in markets:
        self.market_table.insert(parent='', index=END, values=(market, ))

def table_item_selected(self):
    curItem = self.market_table.focus()
    print ("selected item in table",self.market_table.item(curItem))