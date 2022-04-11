
def determine_longest_common_timespan(instruments_selected, data_index_dict):
    min_time = []
    max_time = []

    for index in instruments_selected:
        min_time.append(min(data_index_dict[index[0]]['time'])) #Get all first days (select highest)
        max_time.append(max(data_index_dict[index[0]]['time'])) #Get all last days (select lowest)

    start_time = max(min_time)
    end_time   = min(max_time)

    return [start_time, end_time]
