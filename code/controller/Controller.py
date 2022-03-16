class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view


    def update_fee_status(self, checkbutton_fee_state):

        #Update model
        print("Controller fee_status:", checkbutton_fee_state)
        self.model.set_include_fee_status(checkbutton_fee_state)
        self.update_model()

        #Update View
        self.update_view()


    def update_model(self):
        print("controller: update_model")
        #TODO

    def update_view(self):
        print("controller: update_view")
        #TODO