#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

from src.model.common.determine_longest_common_timespan import determine_longest_common_timespan
from src.model.market_class import Market


def test_determine_longest_common_timespan():

    timespan_overlapping_A       = [20200101,20200102,20200103]
    timespan_overlapping_B       = [20200102,20200103,20200104]
    timespan_earlier_than_others = [20100102,20100103,20100104]
    timespan_later_than_others   = [20220102,20220103,20220104]

    value1 = [1,2,3] #Arbitrary values not important

    markets = {"A": Market("A", value1, timespan_overlapping_A),
               "B": Market("B", value1, timespan_overlapping_B),
               "C": Market("C", value1, timespan_earlier_than_others),
               "D": Market("D", value1, timespan_later_than_others)}

    # Same instrument, full overlap
    instrument_selected = [["A", 1], ["A", 2]]
    assert determine_longest_common_timespan(instrument_selected, markets) == [timespan_overlapping_A[0], timespan_overlapping_A[-1]]
    
    # A starts earlier B ends later, some overlapp
    instrument_selected = [["A", 1], ["B", 1]]
    assert determine_longest_common_timespan(instrument_selected, markets) == [timespan_overlapping_B[0], timespan_overlapping_A[-1]]

    # Not overlapping
    instrument_selected = [["A", 1], ["C", 1]]
    assert determine_longest_common_timespan(instrument_selected, markets) == [0, 0]

    # Not overlapping
    instrument_selected = [["A", 1], ["D", 1]]
    assert determine_longest_common_timespan(instrument_selected, markets) == [0, 0]
