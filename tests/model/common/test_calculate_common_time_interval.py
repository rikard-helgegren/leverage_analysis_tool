#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.


from unittest.mock import patch
from src.model.Market import Market
from src.model.Model import Model
from src.model.common.calculate_common_time_interval import calculate_common_time_interval
from src.model.common.calculate_common_time_interval import compare_available_times_to_view_selected

def test_calculate_common_time_interval():
    model = Model()

    timespan_overlapping_A       = [20200101,20200102,20200103]
    timespan_overlapping_B       = [20200102,20200103,20200104]
    timespan_earlier_than_others = [20100102,20100103,20100104]
    timespan_later_than_others   = [20220102,20220103,20220104]

    value1 = [1,2,3] #Arbitrary values not important

    markets = {"A": Market("A", value1, timespan_overlapping_A),
               "B": Market("B", value1, timespan_overlapping_B),
               "C": Market("C", value1, timespan_earlier_than_others),
               "D": Market("D", value1, timespan_later_than_others)}
    
    model.set_markets(markets)
    model.set_markets_selected(markets)

    # Same instrument, full overlap
    instrument_selected = [["A", 1], ["A", 2]]
    model.set_instruments_selected(instrument_selected)
    assert calculate_common_time_interval(model) == [20200101,20200102,20200103]

    # A starts earlier B ends later, some overlapp
    instrument_selected = [["A", 1], ["B", 1]]
    model.set_instruments_selected(instrument_selected)
    assert calculate_common_time_interval(model) == [20200102,20200103]

    # Not overlapping
    instrument_selected = [["A", 1], ["C", 1]]
    model.set_instruments_selected(instrument_selected)
    assert calculate_common_time_interval(model) == []

    # Not overlapping
    instrument_selected = [["A", 1], ["D", 1]]
    model.set_instruments_selected(instrument_selected)
    assert calculate_common_time_interval(model) == []

    ## Manual override of time intevalls
    model.set_chosen_time_interval_status(True)

    model.set_chosen_start_date_time_limit(20200101)
    model.set_chosen_end_date_time_limit(20200103)
    instrument_selected = [["A", 1], ["A", 2]]
    model.set_instruments_selected(instrument_selected)
    assert calculate_common_time_interval(model) == [20200101,20200102,20200103]
    
    model.set_chosen_start_date_time_limit(20200102)
    model.set_chosen_end_date_time_limit(20200102)
    instrument_selected = [["A", 1], ["A", 2]]
    model.set_instruments_selected(instrument_selected)
    assert calculate_common_time_interval(model) == [20200102]


def test_compare_available_times_to_view_selected():

    model = Model()

    timespan_overlapping_A       = [20200101,20200102,20200103]
    timespan_overlapping_B       = [20200102,20200103,20200104]
    timespan_earlier_than_others = [20100102,20100103,20100104]
    timespan_later_than_others   = [20220102,20220103,20220104]

    value1 = [1,2,3] #Arbitrary values not important

    markets = {"A": Market("A", value1, timespan_overlapping_A),
               "B": Market("B", value1, timespan_overlapping_B),
               "C": Market("C", value1, timespan_earlier_than_others),
               "D": Market("D", value1, timespan_later_than_others)}


    model.set_markets(markets)
    model.set_markets_selected(markets)

    # Same instrument, full overlap
    instrument_selected = [["A", 1], ["A", 2]]
    model.set_instruments_selected(instrument_selected)
    calculated_start_time = 20200101
    calculated_end_time = 20200103
    timespan = timespan_overlapping_A
    assert compare_available_times_to_view_selected(model, calculated_start_time, calculated_end_time, timespan) == [20200101, 20200103]

    # A starts earlier B ends later, some overlapp
    instrument_selected = [["A", 1], ["B", 1]]
    model.set_instruments_selected(instrument_selected)
    model.set_instruments_selected(instrument_selected)
    calculated_start_time = 20200102
    calculated_end_time = 20200103
    timespan = [20200101,20200102,20200103,20200104]
    assert compare_available_times_to_view_selected(model, calculated_start_time, calculated_end_time, timespan) == [20200102,20200103]


    ## Manual override of time intevalls
    model.set_chosen_time_interval_status(True)

    model.set_chosen_start_date_time_limit(20200101)
    model.set_chosen_end_date_time_limit(20200103)    
    instrument_selected = [["A", 1], ["A", 2]]
    model.set_instruments_selected(instrument_selected)
    calculated_start_time = 20200101
    calculated_end_time = 20200103
    timespan = timespan_overlapping_A
    assert compare_available_times_to_view_selected(model, calculated_start_time, calculated_end_time, timespan) == [20200101,20200103]
    
    model.set_chosen_start_date_time_limit(20200102)
    model.set_chosen_end_date_time_limit(20200102)
    instrument_selected = [["A", 1], ["A", 2]]
    model.set_instruments_selected(instrument_selected)
    calculated_start_time = 20200101
    calculated_end_time = 20200103
    timespan = timespan_overlapping_A
    assert compare_available_times_to_view_selected(model, calculated_start_time, calculated_end_time, timespan) == [20200102, 20200102]

    #time dates to early
    model.set_chosen_start_date_time_limit(19990101)
    model.set_chosen_end_date_time_limit(19990103)    
    instrument_selected = [["A", 1], ["A", 2]]
    model.set_instruments_selected(instrument_selected)
    calculated_start_time = 20200101
    calculated_end_time = 20200103
    timespan = timespan_overlapping_A
    assert compare_available_times_to_view_selected(model, calculated_start_time, calculated_end_time, timespan) == [20200101,20200103]
    