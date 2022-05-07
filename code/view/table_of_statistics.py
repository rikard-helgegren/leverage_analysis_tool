
import tkinter as tk
from tkinter import ttk


class Table_Of_Statistics:
    """A table of statistical values describing the portfolios properties"""
    def __init__(self, super_frame):
        print("TRACE: View: Statistics_self.table: __init__")

        self.frame = tk.Frame(super_frame, padx=5, pady=5)
        self.frame.pack()

        # Make it look lik rows can not be selected
        style = tk.ttk.Style()
        style.map("Custom.Treeview",
                  background=[("selected", "white")],
                  foreground=[("selected", "black")])


        scroll = tk.Scrollbar(self.frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.table = tk.ttk.Treeview(self.frame,
                                     yscrollcommand=scroll.set,
                                     style="Custom.Treeview")

        self.table.pack()


        # Define our column
        self.table['columns'] = ('measure', 'value')

        # format our column
        self.table.column("#0", width=0,  stretch=tk.NO)
        self.table.column("measure", width=200)
        self.table.column("value", width=80)

        # Create Headings
        self.table.heading("#0", text="", anchor=tk.CENTER)
        self.table.heading("measure", text="Measure", anchor=tk.CENTER)
        self.table.heading("value", text="Value", anchor=tk.CENTER)

        # Prepare for alternating row colors
        self.table.tag_configure('odd_row', background='#E8E8E8')
        self.table.tag_configure('even_row', background='#D0D0D0')


    def set_table(self, stats_dict):
        """ Add all the statistics to the table"""
        print("TRACE: View: Statistics_self.table: set_self.table")

        self.clear_table()

        for i, key in enumerate(stats_dict):

            # Determine which color should be used on the row
            if i % 2 == 0:
                tag = 'even_row'
            else:
                tag = 'odd_row'

            self.table.insert(parent='', index='end', text='', values=(key, stats_dict[key]), tags=(tag,))

    def clear_table(self):
        # Clear the treeview list items
        for item in self.table.get_children():
            self.table.delete(item)



