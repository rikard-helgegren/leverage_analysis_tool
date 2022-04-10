
class Market:

    def __init__(self, name, values=[], time_span=[]):

        self.name = name
        self.values = values
        self.time_span = time_span

        self.short_name = ""
        self.daily_change = []

    ################## Getters for variables ##############

    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name

    def get_short_name(self):
        return self.short_name
    def set_short_name(self, short_name):
        self.short_name = short_name

    def get_values(self):
        return self.values
    def set_values(self, values):
        self.values = values

    def get_time_span(self):
        return self.time_span
    def set_time_span(self, time_span):
        self.time_span = time_span

    def get_daily_change(self):
        return self.daily_change
    def set_daily_change(self, daily_change):
        self.daily_change = daily_change


    ################## Other methods ##############

    def get_first_day(self):
        return self.time_span[0]

    def get_last_day(self):
        return self.time_span[-1]



