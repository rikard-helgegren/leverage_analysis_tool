#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

from os import listdir
from os.path import isfile, join
from src.Config import Config
import datetime 
import sys
import logging


def check_if_data_files_are_clean(data_file_path):

    clean_files = []

    all_data_files = read_data_files(data_file_path)
    
    # Check each file
    for file_itter in all_data_files:

        # Open file
        try:
            file = open(data_file_path+"/"+file_itter, 'r')
        except:
            logging.error(" Could not open file: ", data_file_path+"/"+file_itter)
            continue

        lines_of_file = file.readlines()
        
        if check_minimum_two_years_of_data(lines_of_file):
            logging.info("SUCCESS: ", file_itter, " File passed size")
        else:
            logging.info("FAIL:    ", file_itter, " File failed size")
            continue

        if check_format_first_line(lines_of_file[0]):
            logging.info("SUCCESS: ", file_itter, " File passed first row format")
        else:
            logging.info("FAIL:    ", file_itter, " File failed first row format")
            continue
        
        if check_value_on_rows(lines_of_file[1:]):
            logging.info("SUCCESS: ", file_itter, " File passed value format")
        else:
            logging.info("FAIL:    ", file_itter, " File failed value format")
            continue

        if check_time_decreases_for_each_row(lines_of_file[1:]):
            logging.info("SUCCESS: ", file_itter, " File passed time decreasing with row number")
        else:
            logging.info("FAIL:    ", file_itter, " File failed time decreasing with row number")
            continue

        if check_daily_change_on_rows(lines_of_file[1:]):
            logging.info("SUCCESS: ", file_itter, " File passed daily change")
        else:
            logging.info("FAIL:    ", file_itter, " File failed daily change")
            continue

        # After passing all tests
        logging.info("SUCCESS: ", file_itter, " Passed all tests")
        clean_files.append(file_itter)

        file.close()

    return clean_files

def read_data_files(data_file_path):
    try:
        return [f for f in listdir(data_file_path) if isfile(join(data_file_path, f))]
    except:
        logging.error("Path to data files is wrong.")
        sys.exit(1)

def check_format_first_line(line):
    words_in_line = line.strip().split(',')

    if words_in_line[0] != "Date":
        return False

    if words_in_line[2] != "Open":
        return False

    return True

def check_minimum_two_years_of_data(lines_of_file):
    config = Config()
    size_of_year = config.DEFAUT_YEARS_HISTOGRAM_INTERVAL
    return len(lines_of_file) > size_of_year*2

def check_value_on_rows(lines):
    return_value = True

    current_time = datetime.datetime.now()
    today = current_time.year*10000+current_time.month*100+current_time.day
    date_before_valid_date = 18000000

    for line in lines:
        words_in_line = line.split(',')

        try:
            date_value = int(words_in_line[0])
            if date_value < date_before_valid_date or date_value > today:
                return_value = False
        except :
            logging.error("  Date format in data file is in wrong format.")
            return False

        try:
            float(words_in_line[2])
        except :
            logging.error("  Market opening value in data file is in wrong format.")
            return False

    return return_value

def check_time_decreases_for_each_row(lines):

    previous_date = 100000000 #date value larger most resent data point

    for line in lines:
        words_in_line = line.split(',')
    
        date_value = int(words_in_line[0])
        if date_value > previous_date:
            logging.error("Time FAILED date_value > previous_date", date_value ,">", previous_date)
            return False
        previous_date = date_value
    return True

def check_daily_change_on_rows(lines):

    market_values = []

    for line in lines:
        words_in_line = line.split(',')
        market_values.append(float(words_in_line[2]))

    for i, value in enumerate(market_values[1:]):
        change = (int(value)-market_values[i])/market_values[i]
        
        if change<= 1 and change >= -0.6:
            # all is well, do nothing
            continue
        else:
            logging.error(" Unprobable daily change:" ,\
                round(change*100,0), "%. Check line ", i-1 )
            return False
    return True
