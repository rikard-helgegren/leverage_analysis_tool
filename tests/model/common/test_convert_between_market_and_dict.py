#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.


from src.model.market_class import Market
from src.model.common.convert_between_market_and_dict import market_dict_to_market_class
from src.model.common.convert_between_market_and_dict import market_class_to_dict_market
from src.model.common.convert_between_market_and_dict import dict_of_market_dicts_to_dict_of_market_classes
from src.model.common.convert_between_market_and_dict import dict_of_market_classes_to_dict_of_market_dicts


from src.model.market_class import Market

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

    market_name = "A"
    timespan = [20200101,20200102,20200103]
    values  = [1,2,3]
    daily_change = [1, 0.5]
    
    market_class = Market(market_name, values, timespan)
    market_class.set_daily_change(daily_change)

    [key, market_dict] = market_class_to_dict_market(market_class)
    
    assert key == "A"
    assert market_dict['index_value'] == market_class.get_values()
    assert market_dict['time'] == market_class.get_time_span()
    assert market_dict['daily_change'] == market_class.get_daily_change()


def test_dict_of_market_dicts_to_dict_of_market_classes():

    market_name1 = "A"
    market_name2 = "B"
    timespan1 = [20200101,20200102,20200103]
    timespan2 = [20100101,20100102,20100103]
    values1  = [1,2,3]
    values2  = [4,8,16]
    daily_change1 = [1, 0.5]
    daily_change2 = [1, 1]
    
    dict_of_market_dicts ={market_name1: {'index_value' : values1,
                                 'time' : timespan1,
                                 'daily_change': daily_change1},
                  market_name2: {'index_value' : values2,
                                 'time' : timespan2,
                                 'daily_change': daily_change2}}

    dict_of_market_classes = dict_of_market_dicts_to_dict_of_market_classes(dict_of_market_dicts)

    # Test first market
    assert isinstance(dict_of_market_classes[market_name1], Market)
    assert dict_of_market_classes[market_name1].get_name() == market_name1
    assert dict_of_market_classes[market_name1].get_values() == values1
    assert dict_of_market_classes[market_name1].get_time_span() == timespan1
    assert dict_of_market_classes[market_name1].get_daily_change() == daily_change1

    # Test second market
    assert isinstance(dict_of_market_classes[market_name2], Market)
    assert dict_of_market_classes[market_name2].get_name() == market_name2
    assert dict_of_market_classes[market_name2].get_values() == values2
    assert dict_of_market_classes[market_name2].get_time_span() == timespan2
    assert dict_of_market_classes[market_name2].get_daily_change() == daily_change2

def test_dict_of_market_classes_to_dict_of_market_dicts():

    market_name1 = "A"
    market_name2 = "B"
    timespan1 = [20200101,20200102,20200103]
    timespan2 = [20100101,20100102,20100103]
    values1  = [1,2,3]
    values2  = [4,8,16]
    daily_change1 = [1, 0.5]
    daily_change2 = [1, 1]
    
    market_class1 = Market(market_name1, values1, timespan1)
    market_class1.set_daily_change(daily_change1)
    market_class2 = Market(market_name2, values2, timespan2)
    market_class2.set_daily_change(daily_change2)

    dict_of_classes = {market_name1: market_class1,
                       market_name2: market_class2}

    dict_of_market_dicts = dict_of_market_classes_to_dict_of_market_dicts(dict_of_classes)
    
    dict_key_list = list(dict_of_market_dicts.keys())

    assert dict_key_list == ["A", "B"]

    assert dict_key_list[0] == market_name1
    assert dict_of_market_dicts[market_name1]['index_value'] == market_class1.get_values()
    assert dict_of_market_dicts[market_name1]['time'] == market_class1.get_time_span()
    assert dict_of_market_dicts[market_name1]['daily_change'] == market_class1.get_daily_change()

    assert dict_key_list[1] == market_name2
    assert dict_of_market_dicts[market_name2]['index_value'] == market_class2.get_values()
    assert dict_of_market_dicts[market_name2]['time'] == market_class2.get_time_span()
    assert dict_of_market_dicts[market_name2]['daily_change'] == market_class2.get_daily_change()
