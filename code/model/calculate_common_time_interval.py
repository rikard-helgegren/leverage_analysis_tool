
import logging
import numpy as np

from code.model.determine_longest_common_timespan import determine_longest_common_timespan


def calculate_common_time_interval(model):

    markets_selected              = model.get_markets_selected()

    instruments_selected = model.get_instruments_selected()

    # Check if empty
    if instruments_selected == []:
        logging.debug("NOTIFY: Model: calculate_outcomes: instruments_selected is empty")
        return []

    if markets_selected  == []:
        logging.debug("NOTIFY: Model: calculate_outcomes: no loaded data files")
        return []

    # Get select data of a random instrument
    market = markets_selected[instruments_selected[0][0]]

    # Extract interval
    time_span = market.get_time_span()

    # Get common start and end time
    [start_time, end_time] = determine_longest_common_timespan(instruments_selected, markets_selected)

    # Compare calculated start and end time with manually set start and end time
    [start_time, end_time] = compare_calculated_times_to_input(model, start_time, end_time, time_span)

    start_pos = time_span.index(start_time)
    end_pos   = time_span.index(end_time)

    time_interval = time_span[start_pos:end_pos]

    return time_interval

def compare_calculated_times_to_input(model, calculated_start_time, calculated_end_time, time_span):
    """ Check if the manually set time limits are valid, otherwise use calculated start and end time"""

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
                if time_span.index(manual_start_date + i):
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
                if time_span.index(manual_end_date - i):
                    end_date = manual_end_date - i
                    break
            except ValueError:
                continue

    return [start_date, end_date]
