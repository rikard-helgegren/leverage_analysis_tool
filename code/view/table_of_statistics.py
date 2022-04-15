
import tkinter as tk
from tkinter import ttk


class Table_Of_Statistics:
    print("TRACE: View: Statistics_self.table: __init__")
    def __init__(self, super_frame):

        self.frame = tk.Frame(super_frame, padx=5, pady=5)
        self.frame.pack()

        # Make it look lik rows cant be selected
        style = tk.ttk.Style()
        style.map("Custom.Treeview", background=[("selected", "white")],
                                     foreground=[("selected", "black")])


        scroll = tk.Scrollbar(self.frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.table = tk.ttk.Treeview(self.frame,
                                  yscrollcommand=scroll.set,
                                  style="Custom.Treeview")

        self.table.pack()


        #define our column

        self.table['columns'] = ('measure', 'value')

        # format our column
        self.table.column("#0", width=0,  stretch=tk.NO)
        self.table.column("measure",anchor=tk.CENTER, width=80)
        self.table.column("value",anchor=tk.CENTER,width=80)

        #Create Headings
        self.table.heading("#0",text="",anchor=tk.CENTER)
        self.table.heading("measure",text="Measure",anchor=tk.CENTER)
        self.table.heading("value",text="Value",anchor=tk.CENTER)

        #add data
        self.table.insert(parent='',index='end',iid=0,text='',
        values=('Mean','123'))
        self.table.insert(parent='',index='end',iid=1,text='',
        values=('Median','321'))
        self.table.insert(parent='',index='end',iid=2,text='',
        values=('Volatitlity','111'))

    def set_table(self, stats):
        print("TRACE: View: Statistics_self.table: set_self.table")
        #TODO





