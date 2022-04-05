#!/usr/bin/env python3
import numpy as np


def calculate_outcomes(self):
    data_index_dict      = self.get_data_index_dict()
    instruments_selected = self.get_instruments_selected()

    if instruments_selected == []:
        print("NOTIFY: Model: calculate_outcomes: instruments_selected is empty")
        return

    if data_index_dict  == []:
        print("NOTIFY: Model: calculate_outcomes: instruments_selected is empty")
        return

    #Get common start and end time
    [start_time, end_time] = determine_longest_common_timespan(instruments_selected, data_index_dict)

    combined_outcomes_full_time = calculate_combined_outcomes_full_time(start_time, end_time, instruments_selected, data_index_dict)


    selected_key = instruments_selected[0][0]
    print("TMP selected_key: ", selected_key)



    combined_outcomes_time_intervall = []
    combined_outcomes_full_time = data_index_dict[selected_key]["index_value"]

    self.set_combined_outcomes_time_intervall(combined_outcomes_time_intervall)
    self.set_combined_outcomes_full_time(combined_outcomes_full_time)


def determine_longest_common_timespan(instruments_selected, data_index_dict):    
    min_time = []
    max_time = []
    for index in instruments_selected:
        min_time.append(min(data_index_dict[index[0]]['time'])) #Get all first days (select highest)
        max_time.append(max(data_index_dict[index[0]]['time'])) #Get all last days (select lowest)

    start_time = max(min_time)
    end_time   = min(max_time)

    return [start_time, end_time]

def calculate_combined_outcomes_full_time(start_time, end_time, instruments_selected, data_index_dict):
    print("TMP: work in progress")

    combined_outcome = []

    number_of_leveraged_selected = 0
    number_of_non_leveraged_selected = 0

    for instrument in instruments_selected:
        print("TMP: index", instrument)

        #Get data with instrument name
        inedx_data = data_index_dict[instrument[0]]

        #Get index of start time for this instrument
        start_pos = np.where(inedx_data['time'] == start_time)
        end_pos   = np.where(inedx_data['time'] == end_time)

        relevant_daily_change = inedx_data['daily_change'][start_pos:end_pos]


        # Look at instrument leverage
        if instrument[2] == 1:
            number_of_non_leveraged_selected += 1
            performance = simulate_normal_performance(relevant_daily_change)
        elif instrument[2] > 1:
            number_of_leveraged_selected += 1
            performance = simulate_leverage_strategy(relevant_daily_change)
        else:
            print("ERROR: elegal leverage used")



def simulate_normal_performance(relevant_daily_change):
    

def simulate_leverage_strategy(relevant_daily_change):