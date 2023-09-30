#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

from kivy.logger import Logger
from kivy.logger import logging
import sys

from src.model.Model import Model
from src.view.View import View
from src.controller.Controller import Controller


def set_debug_level():
    if len(sys.argv) >= 2:
        debug_level = sys.argv[1] 

        if (debug_level == "-debug"):
            logging.getLogger().setLevel('DEBUG')
        
        elif(debug_level == "-info"):
            logging.getLogger().setLevel('INFO')


#class LeverageApp(App):
    """ GUI for analyzing investments with leveraged certificates.
        The code follows the MVC (Model View Controller) architecture
    
    def __init__(self):
        super().__init__()

        self.title('Leverage Analysis Tool')

        model = Model()
        model.model_import_data()

        # place view on the root window
        view = View()
        #view.pack()

       

        controller = Controller(model, view)
"""
 
        # make the view updated
        #controller.update_view()
    
# Create an instance and run the application
#if __name__ == '__main__':
#    set_debug_level()
#    Leverage_Application().run()

from kivymd.app import MDApp as MDAPP
from kivy.uix.widget import Widget


class LeverageApp(MDAPP):
    def build(self):

        model = Model()
        model.model_import_data()

        view = View()

        controller = Controller(model, view)

        # set the controller to view
        view.set_controller(controller)

        return view
    

if __name__ == '__main__':
    set_debug_level()
    LeverageApp().run()
