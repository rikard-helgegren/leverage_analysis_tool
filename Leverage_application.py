#!/usr/bin/env python3

###### MODEL ######
#import code.model.model as model

from tkinter import *
from code.model.Model import Model
from code.view.View import View
from code.controller.Controller import Controller

class Leverage_application(Tk):
    def __init__(self):
        super().__init__()

        self.title('Leverage Experiment Tool')

        # create a model
        model = Model()
        model.model_initiate()

        # create a view and place it on the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = Controller(model, view)

        # set the controller to view
        view.set_controller(controller)
    

    

############################

if __name__ == '__main__':
    app = Leverage_application()
    app.mainloop()