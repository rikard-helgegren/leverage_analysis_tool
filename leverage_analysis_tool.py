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
from kivymd.app import MDApp as MDAPP
import sys

from src.model.Model import Model
from src.view.View import View
from src.controller.Controller import Controller


def set_debug_level():

    if len(sys.argv) > 1:
        argument_from_terminal = sys.argv[1]
        label_text = f"Argument from terminal: {argument_from_terminal}"
    else:
        label_text = "No argument provided from the terminal"

    print(label_text)


    print("sys.argv",sys.argv)
    if len(sys.argv) >= 2:
        debug_level = sys.argv[1] 

        if (debug_level == "debug"):
            logging.getLogger().setLevel('DEBUG')
        
        elif(debug_level == "info"):
            logging.getLogger().setLevel('INFO')
        
        elif(debug_level == "trace"):
            logging.getLogger().setLevel('TRACE')


class LeverageApp(MDAPP):
    def build(self):
        self.title ='Leverage Analysis Tool'

        model = Model()
        model.model_import_data()

        view = View()

        controller = Controller(model, view)

        # set the controller to view
        view.set_controller(controller)

        #self.theme_cls.theme_style = "Dark"

        return view
    

if __name__ == '__main__':
    set_debug_level()
    LeverageApp().run()
