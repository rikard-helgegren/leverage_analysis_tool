#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.


class Market:
    """ Represents a stock market

        params Values

    """
    def __init__(self, name, values=[], time_span=[]):

        self.name = name
        self.values = values
        self.time_span = time_span

        self.country = ""
        self.daily_change = []

    
    def get_first_day(self):
        return self.time_span[0]

    def get_last_day(self):
        return self.time_span[-1]

    ################## Getters for variables ##############

    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name

    def get_country(self):
        return self.contry
    def set_country(self, contry):
        self.contry = contry

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
