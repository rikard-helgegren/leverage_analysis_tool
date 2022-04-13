
def fill_in_missing_dates(markets_dict):
    print("TRACE: Model: fill_in_missing_dates")

    # dict init first date and last date
    very_first_day = 30001224 # some day in future
    very_last_day  = 0        #some day before market data
    for market in markets_dict.values():
        market_first_day = market.get_first_day()
        market_last_day  = market.get_last_day()

        # Itterate to find the very first and last day of all the markets
        if market_first_day < very_first_day:
            very_first_day = market_first_day
        if market_last_day > very_last_day:
            very_last_day = market_last_day


    #set of all days
    all_dates = {very_first_day}
    for market in markets_dict.values():
        for date in market.get_time_span():
            all_dates.add(date)

    # sort set
    all_dates =sorted(all_dates)


    #for days from first date
    #if one have date, add to all others that have earlier ...
    #first date if not later then last date. Add value of prev day
    for market in markets_dict.values():


        first_day = market.get_first_day()
        last_day = market.get_last_day()
        previous_day = first_day # starting refrence
        time_span = market.get_time_span()
        market_values = market.get_values()

        for current_day in all_dates:
        
            if current_day > first_day and current_day < last_day:
                if current_day in time_span:
                    previous_day = current_day
                else:

                    #get values needed
                    pos = time_span.index(previous_day)
                    most_resent_index_value = market_values[pos]
                    
                    #Insert value of prev day in missing day
                    time_span.insert(pos+1, current_day) # would be mouch faster with linked list
                    market_values.insert(pos+1, most_resent_index_value) # would be mouch faster with linked list
                    
                    #Update last checked day
                    previous_day = current_day

    return markets_dict


