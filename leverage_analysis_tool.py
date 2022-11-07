#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.
#

import tkinter as tk
from src.model.model import Model
from src.view.view import View
from src.controller.controller import Controller
import logging
import sys

def set_debug_level():
    if len(sys.argv) >= 2:
        debug_level = sys.argv[1] 

        if (debug_level == "-debug" or
            debug_level == "-Debug" or
            debug_level == "-DEBUG"):

            logging.getLogger().setLevel('DEBUG')
        
        elif(debug_level == "-info" or
            debug_level == "-Info" or
            debug_level == "-INFO"):

            logging.getLogger().setLevel('INFO')


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
    set_debug_level()
    app = Leverage_Application()
    app.mainloop()
