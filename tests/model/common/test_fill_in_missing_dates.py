#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

from unittest.mock import patch
from src.model.common.fill_in_missing_dates import find_first_common_market_day
from src.model.common.fill_in_missing_dates import find_last_common_market_day
from src.model.common.fill_in_missing_dates import fix_gaps2
from src.model.common.fill_in_missing_dates import fill_gaps_data
from src.model.common.Linked_list import linked_list_to_list
from src.model.common.Linked_list import list_to_linked_list


from src.model.market_class import Market

def test_find_first_common_market_day():
    
    # Return first shared market day
    first_list_of_days = [1, 2, 3]
    second_list_of_days = [1, 3, 3]
    list_of_both = [first_list_of_days, second_list_of_days]
    earliest_day_allowed = 0
    correct_answere = 1
    assert find_first_common_market_day(list_of_both, earliest_day_allowed) == correct_answere


    # Return first shared market day
    first_list_of_days = [1, 2, 3]
    second_list_of_days = [2, 3, 4]
    list_of_both = [first_list_of_days, second_list_of_days]
    earliest_day_allowed = 0
    correct_answere = 2
    assert find_first_common_market_day(list_of_both, earliest_day_allowed) == correct_answere

    # Return over writing value "set by user"
    first_list_of_days = [1, 2, 3]
    second_list_of_days = [2, 3, 4]
    list_of_both = [first_list_of_days, second_list_of_days]
    earliest_day_allowed = 3
    assert find_first_common_market_day(list_of_both, earliest_day_allowed) == earliest_day_allowed


def test_find_last_common_market_day():

   # Return last shared market day
    first_list_of_days = [1, 2, 3]
    second_list_of_days = [1, 2, 3]
    list_of_both = [first_list_of_days, second_list_of_days]
    latest_day_allowed = 5
    correct_answere = 3
    assert find_last_common_market_day(list_of_both, latest_day_allowed) == correct_answere

    # Return last shared market day
    first_list_of_days = [1, 2, 3]
    second_list_of_days = [2, 3, 4]
    list_of_both = [first_list_of_days, second_list_of_days]
    latest_day_allowed = 5
    correct_answere = 3
    assert find_last_common_market_day(list_of_both, latest_day_allowed) == correct_answere

    # Return over writing value "set by user"
    first_list_of_days = [1, 2, 3]
    second_list_of_days = [2, 3, 4]
    list_of_both = [first_list_of_days, second_list_of_days]
    latest_day_allowed = 2
    assert find_last_common_market_day(list_of_both, latest_day_allowed) == latest_day_allowed


def test_fix_gaps2():
    first_list_of_days = [1, 3, 4]
    second_list_of_days = [1, 2, 4]
    list_of_both = [first_list_of_days, second_list_of_days]
    latest_first = 1  # TODO fix naming to more understandable
    earliest_last = 4
    answer = linked_list_to_list(fix_gaps2(list_of_both, latest_first, earliest_last))
    correct_answer = [1,2,3,4]
    assert answer == correct_answer

    first_list_of_days = [1, 3, 5, 7]
    second_list_of_days = [2, 4, 5, 8]
    list_of_both = [first_list_of_days, second_list_of_days]
    latest_first = 2  # TODO fix naming to more understandable
    earliest_last = 7
    answer = linked_list_to_list(fix_gaps2(list_of_both, latest_first, earliest_last))
    correct_answer = [2,3,4,5,7]
    assert answer == correct_answer

@patch('src.model.common.fill_in_missing_dates.find_first_common_market_day')
@patch('src.model.common.fill_in_missing_dates.find_last_common_market_day')
@patch('src.model.common.fill_in_missing_dates.fix_gaps2')
def test_fill_gaps_data(mock_fix_gaps2, mock_find_last_common_market_day, mock_find_first_common_market_day):

    timespan_overlapping_A       = [11,12,14]
    timespan_overlapping_B       = [12,13,14]

    mock_find_first_common_market_day.return_value = 12
    mock_find_last_common_market_day.return_value = 14    
    mock_fix_gaps2.return_value = list_to_linked_list([12,13,14])

    value1 = [1,2,3] #Arbitrary values not important

    markets = {"A": Market("A", value1, timespan_overlapping_A),
                        "B": Market("B", value1, timespan_overlapping_B)}

    chosen_time_interval_start_date = 0 # Lower than all
    chosen_time_interval_end_date = 100 # Higher than all

    answer = fill_gaps_data(markets, chosen_time_interval_start_date, chosen_time_interval_end_date)
    correct_answer_time = [12,13,14]
    correct_values_A = [2,2,3]
    correct_values_B = [1,2,3]

    assert answer["A"].time_span == correct_answer_time
    assert answer["B"].time_span == correct_answer_time
    assert answer["A"].get_values() == correct_values_A
    assert answer["B"].get_values() == correct_values_B

    # Make sure mock is used
    assert mock_find_first_common_market_day.call_count > 0
    assert mock_find_last_common_market_day.call_count > 0
    assert mock_fix_gaps2.call_count > 0
