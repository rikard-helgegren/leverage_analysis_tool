#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import tkinter as tk
from code.model.model import Model
from code.view.view import View
from code.controller.controller import Controller

class Leverage_Application(tk.Tk):
    """ GUI for analyzing investments with leveraged cirtificates.
        The code follows the MVC (Model View Controller) architecture
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
