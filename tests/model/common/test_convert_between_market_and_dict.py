#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

from tests.model.helpers.Market_Builder import Market_Builder
from src.model.Market import Market
from src.model.common.convert_between_market_and_dict import market_dict_to_market_class
from src.model.common.convert_between_market_and_dict import market_class_to_dict_market
from src.model.common.convert_between_market_and_dict import dict_of_market_dicts_to_dict_of_market_classes
from src.model.common.convert_between_market_and_dict import dict_of_market_classes_to_dict_of_market_dicts

def test_market_dict_to_market_class():
    
    market_name = "A"
    timespan = [20200101,20200102,20200103]
    values  = [1,2,3]
    daily_change = [1, 0.5]

    market_dict ={'index_value' : values,
                  'time' : timespan,
                  'daily_change': daily_change}

    market_class = market_dict_to_market_class(market_name, market_dict)

    assert isinstance(market_class, Market)
    assert market_class.get_name() == market_name
    assert market_class.get_values() == values
    assert market_class.get_time_span() == timespan
    assert market_class.get_daily_change() == daily_change


def test_market_class_to_dict_market():


    market_class = Market_Builder().build()

    [key, market_dict] = market_class_to_dict_market(market_class)
    
    assert key == "A"
    assert market_dict['index_value'] == market_class.get_values()
    assert market_dict['time'] == market_class.get_time_span()
    assert market_dict['daily_change'] == market_class.get_daily_change()


def test_dict_of_market_dicts_to_dict_of_market_classes():


    market_class1 = Market_Builder().build()
    market_class2 = Market_Builder() \
            .name('B') \
            .time_span([20100101,20100102,20100103]) \
            .values([4,8,16]) \
            .build()

    
    dict_of_market_dicts ={market_class1.name: 
                                {'index_value' : market_class1.values,
                                 'time' : market_class1.time_span,
                                 'daily_change': market_class1.daily_change},
                           market_class2.name: 
                                {'index_value' : market_class2.values,
                                 'time' : market_class2.time_span,
                                 'daily_change': market_class2.daily_change}}
    
    dict_of_market_classes = dict_of_market_dicts_to_dict_of_market_classes(dict_of_market_dicts)
                            #convert_dict_items_from_dict_to_market_classes
    # Test first market
    assert isinstance(dict_of_market_classes[market_class1.name], Market)
    assert dict_of_market_classes[market_class1.name].get_name() == market_class1.name
    assert dict_of_market_classes[market_class1.name].get_values() == market_class1.values
    assert dict_of_market_classes[market_class1.name].get_time_span() == market_class1.time_span
    assert dict_of_market_classes[market_class1.name].get_daily_change() == market_class1.daily_change

    # Test second market
    assert isinstance(dict_of_market_classes[market_class2.name], Market)
    assert dict_of_market_classes[market_class2.name].get_name() == market_class2.name
    assert dict_of_market_classes[market_class2.name].get_values() == market_class2.values
    assert dict_of_market_classes[market_class2.name].get_time_span() == market_class2.time_span
    assert dict_of_market_classes[market_class2.name].get_daily_change() == market_class2.daily_change

def test_dict_of_market_classes_to_dict_of_market_dicts():

    market_class1 = Market_Builder().build()
    market_class2 = Market_Builder() \
            .name('B') \
            .time_span([20100101,20100102,20100103]) \
            .values([4,8,16]) \
            .build()

    dict_of_classes = {market_class1.name: market_class1,
                       market_class2.name: market_class2}

    dict_of_market_dicts = dict_of_market_classes_to_dict_of_market_dicts(dict_of_classes)
    
    dict_key_list = list(dict_of_market_dicts.keys())

    assert dict_key_list == ["A", "B"]

    assert dict_key_list[0] == market_class1.name
    assert dict_of_market_dicts[market_class1.name]['index_value'] == market_class1.get_values()
    assert dict_of_market_dicts[market_class1.name]['time'] == market_class1.get_time_span()
    assert dict_of_market_dicts[market_class1.name]['daily_change'] == market_class1.get_daily_change()

    assert dict_key_list[1] == market_class2.name
    assert dict_of_market_dicts[market_class2.name]['index_value'] == market_class2.get_values()
    assert dict_of_market_dicts[market_class2.name]['time'] == market_class2.get_time_span()
    assert dict_of_market_dicts[market_class2.name]['daily_change'] == market_class2.get_daily_change()
