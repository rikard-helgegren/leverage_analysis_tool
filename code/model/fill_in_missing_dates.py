
def fill_in_missing_dates(data_index_dict):
    print("TRACE: Model: fill_in_missing_dates")
    
    # get keys
    all_indexes = data_index_dict.keys()

    # dict init first date and last date
    very_first_day = 30001224
    very_last_day = 0
    index_dict = {}
    for index in all_indexes:
        first_day = min(data_index_dict[index]['time'])
        last_day = max(data_index_dict[index]['time'])

        index_dict[index] = {'first_day':first_day, 'last_day':last_day, 'last_checked_day':first_day} 

        if first_day < very_first_day:
            very_first_day = first_day
        if last_day > very_last_day:
            very_last_day = last_day

    #set of all days
    all_dates = {very_first_day}
    for index in all_indexes:
        for date in data_index_dict[index]['time']:
            all_dates.add(date)


    #for days from first date
    #if one have date, add to all others that have earlier ...
    #first date if not later then last date. Add value of prev day
    for index in all_indexes:
        for day in all_dates:
        
            if day > index_dict[index]['first_day'] and day < index_dict[index]['last_day']:
                if day in data_index_dict[index]['time']:
                    index_dict[index]['last_checked_day'] = day
                else:

                    #get values needed
                    last_checked_day = index_dict[index]['last_checked_day']
                    pos = data_index_dict[index]['time'].index(last_checked_day)
                    most_resent_index_value = data_index_dict[index]['index_value'][pos]
                    
                    #Insert value of prev day in missing day
                    data_index_dict[index]['time'].insert(pos+1, day) # would be mouch faster with linked list
                    data_index_dict[index]['index_value'].insert(pos+1, most_resent_index_value) # would be mouch faster with linked list
                    
                    #Update last checked day
                    index_dict[index]['last_checked_day'] = day

    return data_index_dict


