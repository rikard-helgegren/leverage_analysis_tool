#!/usr/bin/env python3
import numpy as np
import csv


def read_and_manage_raw_data(data_file_path, index_file_names_list):
    
    country_data_and_sattistics = {}

    for contry_index in index_file_names_list:
        
        
        time = []
        index_value = []


        #read data, exclude first row of describing text
        results = []
        with open(data_file_path+"/"+contry_index) as csvfile:
            first_row = next(csvfile)
            reader = csv.reader(csvfile,)
            for row in reader: # each row is a list
                time.append(float(row[0]))
                index_value.append(float(row[2]))

        #save data in dict
        country_data_and_sattistics[contry_index] = {'time': np.array(time)}
        country_data_and_sattistics[contry_index]['index_value'] = np.array(index_value)


    return country_data_and_sattistics