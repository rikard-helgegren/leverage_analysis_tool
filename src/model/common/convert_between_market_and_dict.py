#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging

from src.model.Market import Market

def market_dict_to_market_class(market_name ,market_dict):
    """ Convert a dictionary represenattion of a market class to a market object"""
    logging.debug("Model: market_dict_to_market_class")

    market_class = Market(market_name, market_dict['index_value'], market_dict['time'])
    market_class.set_daily_change(market_dict['daily_change'])

    return market_class


def market_class_to_dict_market(market_class):
    """ Convert a  market object to a dictionary represenattion of a market class"""
    logging.debug("Model: market_class_to_dict_market")

    key = market_class.get_name()
    market_dict = {}

    market_dict['index_value'] = market_class.get_values()
    market_dict['time'] = market_class.get_time_span()
    market_dict['daily_change'] = market_class.get_daily_change()

    return [key, market_dict]


def dict_of_market_dicts_to_dict_of_market_classes(dict_of_market_dicts):
    logging.debug("Model: dict_of_market_dicts_to_dict_of_market_classes")
    dict_of_market_classes = {}

    for key in dict_of_market_dicts.keys():
        dict_of_market_classes[key] = market_dict_to_market_class(key, dict_of_market_dicts[key])

    return dict_of_market_classes

def dict_of_market_classes_to_dict_of_market_dicts(dict_of_classes):
    logging.debug("Model: dict_of_market_classes_to_dict_of_market_dicts")
    dict_of_market_dicts = {}

    for key in dict_of_classes.keys():
        dict_of_market_dicts[key] = market_class_to_dict_market(dict_of_classes[key])[1]

    return dict_of_market_dicts
