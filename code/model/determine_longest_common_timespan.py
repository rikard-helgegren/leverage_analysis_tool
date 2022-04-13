
def determine_longest_common_timespan(instruments_selected, market_dict):
    min_time = []
    max_time = []

    for instrument in instruments_selected:
        min_time.append(market_dict[instrument[0]].get_first_day()) #Get all first days (select highest)
        max_time.append(market_dict[instrument[0]].get_last_day()) #Get all last days (select lowest)

    start_time = max(min_time)
    end_time   = min(max_time)

    return [start_time, end_time]
