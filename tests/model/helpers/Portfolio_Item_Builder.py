#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.


from src.model.Portfolio_item import Portfolio_Item
from src.model.common.calcultate_daily_change import calculate_daily_change_from_value


class Portfolio_Item_Builder:
    """ Represents an item in the investment portfolio

        params Values

    """
    def __init__(self):

        self.portfolio_item = Portfolio_Item("A", 1)

        self.portfolio_item.name = "A"
        self.portfolio_item.leverage = 1

        self.portfolio_item.values = [1.0] # gets populated when running
        self.portfolio_item.country = "a"
        self.portfolio_item.daily_change = [1, 0.5]
        self.portfolio_item.reference_value = 1.0
        self.portfolio_item.current_value = 1.0

        # For Histogram purposes
        self.portfolio_item.has_appended = False
        self.portfolio_item.has_done_action = False

    def name(self, name):
        self.portfolio_item.name = name
        return self

    def country(self, country):
        self.portfolio_item.country = country
        return self
    
    def values(self, values):
        self.portfolio_item.values = values
        self.portfolio_item.current_value = values[0]
        #self.portfolio_item.daily_change = calculate_daily_change_from_value(self.portfolio_item.values)
        return self
   
    def leverage(self, leverage):
        self.portfolio_item.leverage = leverage
        return self
   
    def current_value(self, current_value):
        self.portfolio_item.current_value = current_value
        return self
  
    def reference_value(self, reference_value):
        self.portfolio_item.reference_value = reference_value
        return self
   
    def daily_change(self, daily_change):
        self.portfolio_item.daily_change = daily_change
        return self
    
    def has_appended(self, has_appended):
        self.portfolio_item.has_appended = has_appended
        return self
    
    def has_done_action(self, value):
        self.portfolio_item.has_done_action = value
        return self 

    def build(self):
        return self.portfolio_item
    