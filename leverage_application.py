#!/usr/bin/env python3

###### MODEL ######

import tkinter as tk
from code.model.model import Model
from code.view.view import View
from code.controller.controller import Controller

print(tk.__file__)

class Leverage_Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Leverage Experiment Tool')

        # create a model
        model = Model()
        model.model_initiate()

        # create a view and place it on the root window
        view = View(self)
        #view.grid(row=0, column=0, padx=10, pady=10)
        view.pack()

        # create a controller
        controller = Controller(model, view)

        # set the controller to view
        view.set_controller(controller)

        # make the view updated
        controller.update_view()
    

    

############################

if __name__ == '__main__':
    app = Leverage_Application()
    app.mainloop()
