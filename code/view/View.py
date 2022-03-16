from tkinter import *


class View(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # set the controller
        self.controller = None

        # create widgets
        # labels
        self.label = Label(self, text='Years')
        self.label.grid(row=1, column=0)

        self.label_blank = Label(self, text=' ')
        self.label_blank.grid(row=3, column=0)

        # entries
        self.string_var = StringVar()
        self.string_entry = Entry(self, textvariable=self.string_var, width=10)
        self.string_entry.grid(row=2, column=0, sticky=NSEW)

        # checkbuttons
        self.checkbutton_fee_state = IntVar()
        self.checkbutton = Checkbutton(self, text="Include Fees", variable=self.checkbutton_fee_state, command=self.update_fee_status)
        self.checkbutton.grid(row=4, column=0)



    def set_controller(self, controller):
        self.controller = controller

    def update_fee_status(self):
        print("View, fee_status:", self.checkbutton_fee_state.get())
        self.controller.update_fee_status(self.checkbutton_fee_state.get())