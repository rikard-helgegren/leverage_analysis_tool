#!/usr/bin/env python3
import numpy as np


def calculate_outcomes(self):
    print("TRACE: Model: calculate_outcomes")
    data_index_dict      = self.get_data_index_dict()
    instruments_selected = self.get_instruments_selected()
    proportion_funds     = self.get_proportion_funds()
    proportion_leverage  = self.get_proportion_leverage()

    #Check if empty
    if instruments_selected == []:
        print("NOTIFY: Model: calculate_outcomes: instruments_selected is empty")
        return

    if data_index_dict  == []:
        print("NOTIFY: Model: calculate_outcomes: instruments_selected is empty")
        return

    #Get common start and end time
    [start_time, end_time] = determine_longest_common_timespan(instruments_selected, data_index_dict)

    #Calculate the outcome
    combined_outcomes_full_time = calculate_combined_outcomes_full_time(start_time,
                                                                        end_time,
                                                                        instruments_selected,
                                                                        data_index_dict,
                                                                        proportion_funds,
                                                                        proportion_leverage)

    combined_outcomes_time_intervall = []#TODO remove, temporary
    
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


def calculate_combined_outcomes_full_time(start_time,
                                          end_time,
                                          instruments_selected,
                                          data_index_dict,
                                          proportion_funds,
                                          proportion_leverage):

    combined_outcome = []
    outcomes_of_normal_investments = []
    outcomes_of_leverage_investments = []

    number_of_leveraged_selected = 0
    number_of_non_leveraged_selected = 0



    for instrument in instruments_selected:

        leverage = instrument[2]

        #Get data with instrument name
        inedx_data = data_index_dict[instrument[0]]

        #Get index of start time for this instrument
        start_pos = inedx_data['time'].index(start_time)
        end_pos   = inedx_data['time'].index(end_time)


        relevant_daily_change = inedx_data['daily_change'][start_pos:end_pos]


        if leverage == 1:
            number_of_non_leveraged_selected += 1
            performance = simulate_normal_performance(relevant_daily_change)
            outcomes_of_normal_investments.append(performance)
        elif leverage > 1:
            number_of_leveraged_selected += 1
            performance = simulate_leverage_strategy(relevant_daily_change, leverage)
            outcomes_of_leverage_investments.append(performance)
        else:
            print("ERROR: Non valid leverage used")

    #Unifed list of normal instruments
    unified_normal = []
    if number_of_non_leveraged_selected == 1:
        unified_normal = outcomes_of_normal_investments[0]

    elif  number_of_non_leveraged_selected > 1:
        unified_normal = outcomes_of_normal_investments[0]

        for i in range(1, number_of_non_leveraged_selected):
            unified_normal = [a + b for a, b in zip(unified_normal, outcomes_of_normal_investments[i])]
        unified_normal = np.divide(unified_normal, number_of_non_leveraged_selected)

    #Unifed list of leveraged instruments
    unified_leveraged = []
    if number_of_leveraged_selected == 1:
        unified_leveraged = outcomes_of_leveraged_investments[0]

    elif  number_of_leveraged_selected > 1:
        unified_leveraged = outcomes_of_leveraged_investments[0]

        for i in range(1, number_of_leveraged_selected):
            unified_leveraged = [a + b for a, b in zip(unified_leveraged, outcomes_of_leveraged_investments[i])]
        unified_leveraged = np.divide(unified_leveraged, number_of_leveraged_selected)

    #add both lists, take cere if empty TODO
    if number_of_leveraged_selected == 0:
        return unified_normal
    elif number_of_non_leveraged_selected == 0:
        return unified_leveraged
    else:
        unified_combined = [a + b for a, b in zip(np.multiply(proportion_funds,unified_normal), np.multiply(proportion_leverage, unified_leveraged))] 
        return unified_combined


def simulate_normal_performance(relevant_daily_change):

    START_STOCK_VALUE_START = 1000
    stock_value = [START_STOCK_VALUE_START]

    for change in relevant_daily_change:
        new_value = stock_value[-1]*(1+change)
        stock_value.append(new_value)

    return stock_value


def simulate_leverage_strategy(relevant_daily_change, leverage):
    print("TMP: NOT YET FULLY IMPLEMENTED")

    START_STOCK_VALUE_START = 1000
    stock_value = [START_STOCK_VALUE_START]

    for change in relevant_daily_change:
        new_value = stock_value[-1]*(1+change*leverage)
        stock_value.append(new_value)

    return stock_value