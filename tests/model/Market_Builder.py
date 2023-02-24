#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.


from src.model.Market import Market
from src.model.common.calcultate_daily_change import calculate_daily_change_from_value


class Market_Builder:
    """ Represents a stock market

        params Values

        E.g. Market("Name", [1,2,3], [20200103,20200102,20200101])

    """
    def __init__(self):

        self.market = Market('A')

        self.market.name = 'A'
        self.market.values = [1,2,3]
        self.market.time_span = [20200101,20200102,20200103]

        self.market.country = "a"
        self.market.daily_change = calculate_daily_change_from_value(self.market.values)

    def name(self, name):
        self.market.name = name
        return self

    def country(self, country):
        self.market.country = country
        return self

    def values(self, values):
        self.market.values = values
        self.market.daily_change = calculate_daily_change_from_value(self.market.values)
        return self

    def time_span(self, time_span):
        self.market.time_span = time_span

        return self

    def daily_change(self, daily_change):
        self.market.daily_change = daily_change
        return self

    def build(self):
        return self.market
