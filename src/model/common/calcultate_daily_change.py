#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging

def calcultate_daily_change(markets_dict):
    """ Calculating the daily change based on a markets value over time.
        Then sets that parameter in the market object
    """
    logging.debug("Model: calcultate_daily_change")

    for market in markets_dict.values():

        market_values = market.get_values()

        market.set_daily_change(calculate_daily_change_from_value(market_values))

    return markets_dict

def calculate_daily_change_from_value(values):

    daily_change = []

    # Calculate change in index value since last input
    for i, value in enumerate(values[1:]):
        if values[i] <=0:
            logging.error("Stock value can not be negative")
            continue
        change = (value-values[i])/values[i]
        daily_change.append(change)
    
    return daily_change
