import tkinter as tk
from tkinter import ttk

class Menu_Of_Strategies:
    def __init__(self, super_frame, view_object):

        self.view_object = view_object

        # Dropdown menu
        self.frame_dropdown = tk.Frame(super_frame, padx=5, pady=5)
        self.frame_dropdown.pack()

        self.label_dropdown = tk.Label(self.frame_dropdown, text='Strategy')
        self.label_dropdown.pack()

        self.options = ["Hold", "Harvest/Refill", "Rebalance Time", "Do not invest"]

        # datatype of menu text
        self.clicked = tk.StringVar() # TODO "self.clicked" I do not understand this variable name.

        # initial menu text
        self.clicked.set(self.options[0])

        self.drop_menu = tk.OptionMenu(self.frame_dropdown, self.clicked, *self.options, command=self.update_menu_item_focused)
        self.drop_menu.pack()
        self.drop_menu.bind('<<drop_menuSelect>>', self.update_menu_item_focused)

    def get_menu_item_focused(self):
        print("TRACE: Menu_Of_Strategies: get_menu_item_focused")
        item = self.clicked.get()
        return item

    def update_menu_item_focused(self, _):
        print("TRACE: Menu_Of_Strategies: update_menu_item_focused")
        menu_focus_item = self.get_menu_item_focused()
        self.view_object.update_strategy_selected(menu_focus_item)

