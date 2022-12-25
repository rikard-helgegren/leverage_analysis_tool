#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

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

        # For Histogram purposes
        self.has_appended = False
        self.has_done_action = False


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

    def set_has_appended(self, has_appended):
        self.has_appended = has_appended
    def get_has_appended(self):
        return self.has_appended
    
    def set_has_done_action(self, value):
        self.has_done_action = value
    def get_has_done_action(self):
        return self.has_done_action

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
