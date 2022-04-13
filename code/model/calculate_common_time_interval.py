
import numpy as np

from code.model.determine_longest_common_timespan import determine_longest_common_timespan


def calculate_common_time_interval(self):

    markets              = self.get_markets()

    instruments_selected = self.get_instruments_selected()

    #Check if empty
    if instruments_selected == []:
        print("NOTIFY: Model: calculate_outcomes: instruments_selected is empty")
        return []

    if markets  == []:
        print("NOTIFY: Model: calculate_outcomes: no loaded data files")
        return []

    #Get common start and end time
    [start_time, end_time] = determine_longest_common_timespan(instruments_selected, markets)

    #Get select data of a random instrument
    market = markets[instruments_selected[0][0]]

    #Extract intervall
    time_span = market.get_time_span()

    start_pos = time_span.index(start_time)
    end_pos   = time_span.index(end_time)

    time_intervall = time_span[start_pos:end_pos]


    return time_intervall
