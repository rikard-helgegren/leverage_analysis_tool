
def fill_in_missing_dates(data_index_dict):
    print("TRACE: Model: fill_in_missing_dates")
    return data_index_dict

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

        if first_day < absolute_first_day:
            very_first_day = first_day
        if last_day > absolute_last_day:
            very_last_day

    #set of all days


    #for days from first date
    #if one have date, add to all others that have earlier ...
    #first date if not later then last date. Add value of prev day
    for day in range(very_first_day, very_last_day): #ineffective

        for index in all_indexes:
            print("hi")




