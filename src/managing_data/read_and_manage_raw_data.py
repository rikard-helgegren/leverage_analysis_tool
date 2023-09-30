#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import csv
from src.model.Market import Market
#import logging
from kivy.logger import logging


def read_and_manage_raw_data(data_file_path, markets_file_name_list):
    
    country_data_and_sattistics = {}

    for market_file_name in markets_file_name_list:

        time, value = read_data(data_file_path, market_file_name)

        #save data in dict of market objects
        [name, country] = market_file_name.split()

        market = Market(name, value, time)
        market.set_country(country[:-4]) # remove ".csv" before setting contry
        country_data_and_sattistics[name] = market

    return country_data_and_sattistics

def read_data(data_file_path, market_file_name):

    time  = []
    value = []

    with open(data_file_path+"/"+market_file_name) as csvfile:
        _ = next(csvfile)  # exclude first row of describing text 
        reader = csv.reader(csvfile,)
        for row in reader:
            time.append(int(row[0]))
            value.append(float(row[2]))
    
    #Reverse, since data is backwards
    time  = time[::-1]
    value = value[::-1]

    return [time, value]
    
