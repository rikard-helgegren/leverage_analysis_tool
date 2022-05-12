#!/usr/bin/env python3
#
#Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
#This software is only allowed for private use. As a private user you are allowed to copy,
#modify, use, and compile the software. You are NOT however allowed to publish, sell, or
#distribute this software, either in source code form or as a compiled binary, for any purpose,
#commercial or non-commercial, and by any means.
#

import tkinter as tk
from code.model.model import Model
from code.view.view import View
from code.controller.controller import Controller

class Leverage_Application(tk.Tk):
    """ GUI for analyzing investments with leveraged certificates.
        The code follows the MVC (Model View Controller) architecture
    """
    def __init__(self):
        super().__init__()

        self.title('Leverage Analysis Tool')

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

# Create an instance and run the application
if __name__ == '__main__':
    app = Leverage_Application()
    app.mainloop()
