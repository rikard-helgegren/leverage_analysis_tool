
class Portfolio_Item:
    """ Represents an item in the investment portfolio

        params Values

    """
    def __init__(self, name, leverage):

        self.name = name
        self.leverage = leverage

        self.values = []
        self.country = ""
        self.daily_change = []
        self.reference_value = 0
        self.current_value = 0

        ## For Histogram purposes
        self.current_interval = 0
        self.lowest_value = []  # one value for each index
        self.lowest_value_index = []  # one index each time strategy needs to be implemented
        self.highest_value = []  # one value for each index
        self.highest_value_index = []  # one index each time strategy needs to be implemented
        self.start_values_of_intervals_low = []
        self.start_values_of_intervals_high = []
        self.has_appended = False
        self.has_done_action = False

    ################## Getters for variables ##############

    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name

    def get_country(self):
        return self.country
    def set_country(self, country):
        self.country = country

    def get_values(self):
        return self.values
    def set_values(self, values):
        self.values = values

    def get_leverage(self):
        return self.leverage
    def set_leverage(self, leverage):
        self.leverage = leverage

    def get_current_value(self):
        return self.current_value
    def set_current_value(self, current_value):
        self.current_value = current_value

    def get_reference_value(self):
        return self.reference_value
    def set_reference_value(self, reference_value):
        self.reference_value = reference_value

    def get_daily_change(self):
        return self.daily_change
    def set_daily_change(self, daily_change):
        self.daily_change = daily_change

    # lowest_value #
    def set_lowest_value(self, lowest_value):
        self.lowest_value = lowest_value
    def get_lowest_value(self):
        return self.lowest_value
    def reset_lowest_value(self):
        self.lowest_value = []
    def replace_lowest_value(self, value, index):
        self.lowest_value[index] = value

    # highest_value #
    def set_highest_value(self, highest_value):
        self.highest_value = highest_value
    def get_highest_value(self):
        return self.highest_value
    def reset_highest_value(self):
        self.highest_value = []
    def replace_highest_value(self, value, index):
        self.highest_value[index] = value

    # lowest_value_index #
    def set_lowest_value_index(self, lowest_value_index):
        self.lowest_value_index = lowest_value_index
    def get_lowest_value_index(self):
        return self.lowest_value_index
    def reset_lowest_value_index(self):
        self.lowest_value_index = []
    def replace_lowest_value_index(self, value, index):
        self.lowest_value_index[index] = value

    # highest_value_index #
    def set_highest_value_index(self, highest_value_index):
        self.highest_value_index = highest_value_index
    def get_highest_value_index(self):
        return self.highest_value_index
    def reset_highest_value_index(self):
        self.highest_value_index = []
    def replace_highest_value_index(self, value, index):
        self.highest_value_index[index] = value

    # start values of intervals that end in low #
    def set_start_values_of_intervals_low(self, values):
        self.start_values_of_intervals_low = values
    def get_start_values_of_intervals_low(self):
        return self.start_values_of_intervals_low
    def reset_start_values_of_intervals_low(self):
        self.start_values_of_intervals_low = []
    def replace_start_values_of_intervals_low(self, value, index):
        self.start_values_of_intervals_low[index] = value


    # start values of intervals that end in high #
    def set_start_values_of_intervals_high(self, values):
        self.start_values_of_intervals_high = values
    def get_start_values_of_intervals_high(self):
        return self.start_values_of_intervals_high
    def reset_start_values_of_intervals_high(self):
        self.start_values_of_intervals_high = []
    def replace_start_values_of_intervals_high(self, value, index):
        self.start_values_of_intervals_high[index] = value


    def set_has_appended(self, has_appended):
        self.has_appended = has_appended
    def get_has_appended(self):
        return self.has_appended
    
    def set_has_done_action(self, value):
        self.has_done_action = value
    def get_has_done_action(self):
        return self.has_done_action

    def get_current_interval(self):
        return self.current_interval
    def set_current_interval(self, current_interval):
        self.current_interval = current_interval

    ################## Other methods ##############

    def get_first_day(self):
        return self.time_span[0]

    def get_last_day(self):
        return self.time_span[-1]

    def to_string(self):
        return "name: " + self.name + ...
        "\nleverage: "+ self.leverage + ...
        "\nvalues len: "+ len(self.values) + ...
        "\ncountry: " + self.country + ...
        "\ndaily_change len: " + len(self.daily_change) + ...
        "\nreference_value: " +self.reference_value + ...
        "\ncurrent_value: " + self.current_value
