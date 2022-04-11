
import numpy as np

from code.model.determine_longest_common_timespan import determine_longest_common_timespan


def calculate_common_time_interval(self):

    data_index_dict      = self.get_data_index_dict()
    instruments_selected = self.get_instruments_selected()

    #Check if empty
    if instruments_selected == []:
        print("NOTIFY: Model: calculate_outcomes: instruments_selected is empty")
        return []

    if data_index_dict  == []:
        print("NOTIFY: Model: calculate_outcomes: no loaded data files")
        return []

    #Get common start and end time
    [start_time, end_time] = determine_longest_common_timespan(instruments_selected, data_index_dict)

    #Get select data of a random instrument
    inedx_data = data_index_dict[instruments_selected[0][0]]

    #Get index of start time for this instrument
    start_pos = inedx_data['time'].index(start_time)
    end_pos   = inedx_data['time'].index(end_time)

    #Extract intervall
    time_intervall = inedx_data['time'][start_pos:end_pos]


    return time_intervall
