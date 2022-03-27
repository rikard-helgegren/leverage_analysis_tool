class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view


    def update_fee_status(self, checkbutton_fee_state):

        #Update model
        print("TRACE: controller: fee_status:", checkbutton_fee_state)
        self.model.set_include_fee_status(checkbutton_fee_state)
        self.update_model()

        #Update View
        self.update_view()


    def update_model(self):
        print("TRACE: controller: update_model")
        #TODO
        self.model.update_model()

    def update_view(self):
        print("TRACE: controller: update_view")
        #TODO

        ### Update histogram ###
        #data = model.get_all_outcomes()
        data = [1,2,2,3]
        self.draw_histogram(data)
        self.draw_line_graph(data)

        self.set_market_table()



    def draw_histogram(self, data):
        print("TRACE: controller: draw_histogram")
        self.view.draw_histogram(data)

    def draw_line_graph(self, data):
        print("TRACE: controller: draw_line_graph")
        self.view.draw_line_graph(data)

    def set_market_table(self):
        print("TRACE: controller: set_market_table")

        markets = self.model.get_data_index_dict().keys()
        print("markets: ",markets)
        self.view.set_market_table(markets)