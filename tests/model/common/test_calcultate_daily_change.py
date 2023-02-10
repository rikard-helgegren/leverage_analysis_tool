#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

from src.model.Market import Market
from src.model.common.calcultate_daily_change import calcultate_daily_change

def test_calcultate_daily_change():

    timespan = [20200101,20200102,20200103]

    value_constant1 = [1,1,1]
    value_constant2 = [-1,-1,-1]
    value_constant3 = [0,0,0]
    value_increase  = [1,2,3]
    value_decrease  = [3,2,1]

    markets_dict = {"A": Market("A", value_constant1, timespan),
                    "B": Market("B", value_constant2, timespan),
                    "C": Market("C", value_constant3, timespan),
                    "D": Market("D", value_increase, timespan),
                    "E": Market("E", value_decrease, timespan)}
    
    calcultate_daily_change(markets_dict)

    assert markets_dict["A"].get_daily_change() == [0, 0]
    assert markets_dict["B"].get_daily_change() == []  # Non valid values
    assert markets_dict["C"].get_daily_change() == []  # Non valid values
    assert markets_dict["D"].get_daily_change() == [1, 0.5]
    assert markets_dict["E"].get_daily_change() == [-1/3, -0.5]


    """ TODO catch typperrors and wierd stuff
    value_None = [1,None,1]
    value_char = ['1',1,1]
    value_empty = []

    markets_dict = {"A": Market("A", value_None, timespan),
                    "B": Market("B", value_char, timespan),
                    "C": Market("C", value_empty, [])}
    
    calcultate_daily_change(markets_dict)

    assert markets_dict["A"].get_daily_change() == [0, 0]
    assert markets_dict["B"].get_daily_change() == []  
    assert markets_dict["C"].get_daily_change() == []
    """
