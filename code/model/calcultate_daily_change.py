#!/usr/bin/env python3

def calcultate_daily_change(index_dictionary):

    for index_key in index_dictionary:

        #Extract index values 
        index_values = index_dictionary[index_key]["index_value"]

        daily_change = []

        #Calculate change in index value since last input
        for index, val in enumerate(index_values[1:]):
            change = (val-index_values[index])/index_values[index]            
            daily_change.append(change)
        
        index_dictionary[index_key]["daily_change"] = daily_change

    return index_dictionary