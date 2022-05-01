
import numpy as np

from code.model.determine_longest_common_timespan import determine_longest_common_timespan


def calculate_common_time_interval(self):

    markets_selected              = self.get_markets_selected()

    instruments_selected = self.get_instruments_selected()

    # Check if empty
    if instruments_selected == []:
        print("NOTIFY: Model: calculate_outcomes: instruments_selected is empty")
        return []

    if markets_selected  == []:
        print("NOTIFY: Model: calculate_outcomes: no loaded data files")
        return []

    # Get common start and end time
    [start_time, end_time] = determine_longest_common_timespan(instruments_selected, markets_selected)

    # Compare calculated start and end time with manually set start and end time
    [start_time, end_time] = compare_times_to_input(self, start_time, end_time) #TODO uggly with self

    # Get select data of a random instrument
    market = markets_selected[instruments_selected[0][0]]

    # Extract interval
    time_span = market.get_time_span()

    start_pos = time_span.index(start_time)
    end_pos   = time_span.index(end_time)

    time_interval = time_span[start_pos:end_pos]


    return time_interval

def compare_times_to_input(self, calculated_start_time, calculated_end_time):
    #TODO refactor uggly

    start_date = calculated_start_time
    end_date = calculated_end_time

    if not self.get_chosen_time_interval_status():
        return [start_date, end_date]

    # Get timespan
    markets_selected = self.get_markets_selected()
    instruments_selected = self.get_instruments_selected()
    market = markets_selected[instruments_selected[0][0]]
    time_span = market.get_time_span()


    manual_start_date = self.get_chosen_start_date_time_limit()
    manual_end_date = self.get_chosen_end_date_time_limit()

    # If start day is manually set
    if manual_start_date != 0:
        for i in range(100):
            try:
                if time_span.index(manual_start_date + i):
                    start_date = manual_start_date + i
                    break
            except ValueError:
                continue

    if manual_end_date != 0:
        for i in range(100):
            try:
                if time_span.index(manual_end_date + i):
                    end_date = manual_end_date + i
                    break
            except ValueError:
                continue

    return [start_date, end_date]