
import tkinter as tk

#Make this a class
def __init__(self):
    frame = tk.Frame(self, padx=5, pady=5)
    frame.pack(side=tk.LEFT)
    #scrollbar
    game_scroll = tk.Scrollbar(frame)
    game_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    columns = ('index', 'country', 'leverage')

    self.market_table = tk.ttk.Treeview(frame,yscrollcommand=game_scroll.set, xscrollcommand =game_scroll.set, columns=columns, show='headings')
    self.market_table.heading('index', text='Index')
    self.market_table.heading('country', text='Country')
    self.market_table.heading('leverage', text='Leverage')
    self.market_table.pack()
    self.market_table.bind('<<TreeviewSelect>>',self.update_table_item_focused)


    # Define the row colors with a tag
    self.market_table.tag_configure("selected_row", background="green")
    self.market_table.tag_configure("not_selected_row", background="white")

def set_market_table(self, markets):
    print("TRACE: table_of_instruments: set_market_table")

    all_item_values = get_all_item_values(self)

    for market in markets:
        #only add if not all ready there
        if market not in all_item_values:
            self.market_table.insert(parent='', index=tk.END, values=(market, 'not known',1))

def get_table_item_focused(self):
    print("TRACE: table_of_instruments: get_table_item_focused")
    curItem = self.market_table.focus()

    return self.market_table.item(curItem)['values']

def update_item_color(self):
    print("TRACE: table_of_instruments: update_item_color")

    curItem = self.market_table.focus()
    current_item_tag = self.market_table.item(curItem)["tags"]

    if current_item_tag != ['selected_row']:
        self.market_table.item(curItem, tag="selected_row")
    else:
        self.market_table.item(curItem, tag="not_selected_row")


def get_all_item_values(self):
    print("TRACE: table_of_instruments: get_all_item_values")

    all_item_values = []

    for item in self.market_table.get_children():
        item_value = self.market_table.item(item)['values']
        all_item_values.append(item_value[0]) # TODO update when adding bull > 1

    return all_item_values

