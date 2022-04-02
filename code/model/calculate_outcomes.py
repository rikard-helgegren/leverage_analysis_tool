#!/usr/bin/env python3


def calculate_outcomes(self):


    data_index_dict      = self.get_data_index_dict()
    instruments_selected = self.get_instruments_selected()

    if instruments_selected == []:
        print("NOTIFY: Model: calculate_outcomes: instruments_selected is empty")
        return

    if data_index_dict  == []:
        print("NOTIFY: Model: calculate_outcomes: instruments_selected is empty")
        return


    selected_key = instruments_selected[0][0]
    print("TMP selected_key: ", selected_key)

    combined_outcomes_time_intervall = []
    combined_outcomes_full_time = data_index_dict[selected_key]["index_value"]

    self.set_combined_outcomes_time_intervall(combined_outcomes_time_intervall)
    self.set_combined_outcomes_full_time(combined_outcomes_full_time)


def determine_longest_common_timespan():
    start_time = 20180101
    end_time = 20200101

    return [start_time, end_time]