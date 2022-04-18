

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view


    def update_fee_status(self, checkbutton_fee_state):

        #Update model
        print("TRACE: Controller: fee_status:", checkbutton_fee_state)
        self.model.set_include_fee_status(checkbutton_fee_state)
        self.update_model()

        #Update View
        self.update_view()


    def update_model(self):
        print("TRACE: Controller: update_model")
        #TODO
        self.model.update_model()

    def update_view(self):
        print("TRACE: Controller: update_view")
        #TODO

        ### Update histogram ###
        combined_outcomes_time_intervals = self.model.get_combined_outcomes_time_intervall()
        self.draw_histogram([1,2,2,3])#combined_outcomes_time_intervals)

        ### Update line graph ###
        time_intervall = self.model.get_common_time_intervall()
        combined_outcomes_full_time = self.model.get_combined_outcomes_full_time()
        self.draw_line_graph(combined_outcomes_full_time, time_intervall)


        self.set_market_table()



    def draw_histogram(self, data):
        print("TRACE: controller: draw_histogram")
        self.view.draw_histogram(data)

    def draw_line_graph(self, data, time_intervall):
        print("TRACE: controller: draw_line_graph")
        self.view.draw_line_graph(data, time_intervall)

    def set_market_table(self):
        print("TRACE: controller: set_market_table")
        #markets = self.model.get_markets().keys() # TODO: maybe make a method for this
        names = []
        countries = []

        for market in self.model.get_markets().values():
            names.append(market.get_name())
            countries.append(market.get_country())


        self.view.set_market_table(names, countries)

    def update_instrument_selected(self, table_focus_item_data ):
        print("TRACE: controller: update_table_item_focused")
        #Update model
        self.model.update_instrument_selected(table_focus_item_data)

        self.update_model()
        self.update_view()
