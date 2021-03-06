

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

        self.draw_histogram(self.model.get_results_for_intervals())  # TODO fix histogram visuals

        ### Update line graph ###
        time_interval = self.model.get_common_time_interval()
        portfolio_results_full_time = self.model.get_portfolio_results_full_time()
        self.draw_line_graph(portfolio_results_full_time, time_interval)

        self.update_chosen_time_intervals()

        self.update_table_of_statistics(self.model.key_values.get_all_values())


    def draw_histogram(self, data):
        print("TRACE: Controller: draw_histogram")
        self.view.draw_histogram(data)

    def draw_line_graph(self, data, time_interval):
        print("TRACE: Controller: draw_line_graph")
        self.view.draw_line_graph(data, time_interval)

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
        print("TRACE: Controller: update_instrument_selected")

        self.model.update_instrument_selected(table_focus_item_data)

        self.update_model()
        self.update_view()

    def set_update_amount_leverage(self, value_percent):
        print("TRACE: Controller: set_update_amount_leverage")
        value = int(value_percent)/100
        self.model.set_proportion_leverage(value)
        self.model.set_proportion_funds(1-value)

        self.update_model()
        self.update_view()

    def update_years_investigating(self, years):
        print("TRACE: Controller: update_years_investigating")
        self.model.set_years_investigating(years)

        self.update_model()
        self.update_view()

    def set_time_limits(self, from_time, to_time):
        print("TRACE: Controller: set_time_limits")

        self.model.set_chosen_start_date_time_limit(from_time)
        self.model.set_chosen_end_date_time_limit(to_time)

        # If time limit is not set, do not use it
        if from_time == 0 and to_time == 0:
            self.model.set_chosen_time_interval_status(False)
        else:
            self.model.set_chosen_time_interval_status(True)

        self.update_model() #TODO can fine tune this
        self.update_view() #TODO can fine tune this

    def update_chosen_time_intervals(self):
        """ Update the manually selected time intervals in the view"""
        start = self.model.get_chosen_start_date_time_limit()
        end = self.model.get_chosen_end_date_time_limit()

        # If start day is 0 then no date is set
        if start != 0:
            start = str(start)

            start = list(start)
            start.insert(6, '-')
            start.insert(4, '-')
            start = ''.join(start)

            self.view.text_box_left.set_text(start)

        # If start day is 0 then no date is set
        if end != 0:
            end = str(end)

            end = list(end)
            end.insert(6, '-')
            end.insert(4, '-')
            end = ''.join(end)

            self.view.text_box_right.set_text(end)

    def update_table_of_statistics(self, key_values):
        self.view.update_table_of_statistics(key_values)
