

class Controller:
    """ This is the controller of the application. Which has access to
        both the view and the model in order to keep the model updated
        and sending the right information to the view.
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.set_table_of_instruments()


    def update_fee_status(self, checkbutton_fee_state):

        #Update model
        print("TRACE: Controller: fee_status:", checkbutton_fee_state)
        self.model.set_include_fee_status(checkbutton_fee_state)
        self.update_model()

        #Update View
        self.update_view()


    def update_model(self):
        print("TRACE: Controller: update_model")
        #TODO not complete (update_model)?
        self.model.update_model()

    def update_view(self):
        print("TRACE: Controller: update_view")
        #TODO not complete (update_view)

        ### Update histogram ###
        self.draw_histogram([1,2,2,3])#TODO fix histogram

        ### Update line graph ###
        time_intervall = self.model.get_common_time_intervall()
        portfolio_results_full_time = self.model.get_portfolio_results_full_time()
        self.draw_line_graph(portfolio_results_full_time, time_intervall)


    def draw_histogram(self, data):
        print("TRACE: Controller: draw_histogram")
        self.view.draw_histogram(data)

    def draw_line_graph(self, data, time_intervall):
        print("TRACE: Controller: draw_line_graph")
        self.view.draw_line_graph(data, time_intervall)

    def set_table_of_instruments(self):
        """ Set the table with information of instruments available"""
        print("TRACE: Controller: set_table_of_instruments")
        names = []
        countries = []

        for market in self.model.get_markets().values():
            names.append(market.get_name())
            countries.append(market.get_country())

        self.view.set_table_of_instruments(names, countries)

    def update_instrument_selected(self, table_focus_item_data ):
        print("TRACE: Controller: update_table_item_focused")
        #Update model
        self.model.update_instrument_selected(table_focus_item_data)

        self.update_model()
        self.update_view()
