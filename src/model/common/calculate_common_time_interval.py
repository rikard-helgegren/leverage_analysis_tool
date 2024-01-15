#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging

from src.model.common.is_data_empty import is_data_empty
from src.model.common.determine_longest_common_timespan import determine_longest_common_timespan


def calculate_common_time_interval(model):
    """Returns the time interval for the displayed data"""
    logging.debug("Model: calculate_common_time_interval")

    markets_selected = model.get_markets_selected()
    instruments_selected = model.get_instruments_selected()

    if is_data_empty(instruments_selected, markets_selected):
        return []

    # Get select data of a random instrument
    market = markets_selected[instruments_selected[0][0]]

    time_span = market.get_time_span()
    
    [start_time, end_time] = determine_longest_common_timespan(instruments_selected, markets_selected)
    
    if start_time == end_time:
        return []

    # Compare calculated start and end time with manually set start and end time
    [start_time, end_time] = compare_available_times_to_view_selected(model, start_time, end_time, time_span)

    start_pos = time_span.index(start_time)
    end_pos   = time_span.index(end_time)

    time_interval = time_span[start_pos:end_pos+1]  # +1 to include end_pos as well

    return time_interval

def compare_available_times_to_view_selected(model, calculated_start_time, calculated_end_time, time_span):
    """ Check if the manually set time limits are valid, otherwise use calculated start and end time"""
    logging.debug("Model: compare_available_times_to_view_selected")

    # Set default
    start_date = calculated_start_time
    end_date = calculated_end_time

    if not model.get_chosen_time_interval_status():
        return [start_date, end_date]

    manual_start_date = model.get_chosen_start_date_time_limit()
    manual_end_date = model.get_chosen_end_date_time_limit()

    # If start day is manually set
    if manual_start_date != 0:
        # find first upcoming day
        for i in range(100):
            try:
                # Match manual_start_date with an existing day in data
                if (manual_start_date + i) in time_span:  # TODO currently i=0 never enters and is tested before 
                    start_date = manual_start_date + i
                    break
            except ValueError:
                continue

    # If end day is manually set
    if manual_end_date != 0:
        # find first previous day
        for i in range(100):
            try:
                # Match manual_end_date with an existing day in data
                if (manual_end_date - i) in time_span:
                    end_date = manual_end_date - i
                    break
            except ValueError:
                continue

    return [start_date, end_date]
