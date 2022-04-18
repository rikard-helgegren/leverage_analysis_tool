#!/usr/bin/env python3

###### MODEL ######

import tkinter as tk
from code.model.model import Model
from code.view.view import View
from code.controller.controller import Controller

class Leverage_Application(tk.Tk):
    """ GUI for analyzing investments with leveraged cirtificates.
        The code follows the MVC (Model View Controller) achitecture

    """
    def __init__(self):
        super().__init__()

        self.title('Leverage Experiment Tool')

        # create a model
        model = Model()
        model.model_import_data()

        # create a view and place it on the root window
        view = View(self)
        view.pack()

        # create a controller
        controller = Controller(model, view)

        # set the controller to view
        view.set_controller(controller)

        # make the view updated
        controller.update_view()
    

############################

# Create an inctance and run the application
if __name__ == '__main__':
    app = Leverage_Application()
    app.mainloop()
