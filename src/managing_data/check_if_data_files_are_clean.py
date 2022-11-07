import os
from os import listdir
from os.path import isfile, join
import datetime 
import sys
import logging


def check_if_data_files_are_clean(data_file_path):

    clean_files = []

    try:
        all_data_files = [f for f in listdir(data_file_path) if isfile(join(data_file_path, f))]
    except:
        logging.error(" Path to data files is wrong.")
        sys.exit(1)

    # Check each file
    for file_itter in all_data_files:

        try:
            file = open(data_file_path+"/"+file_itter, 'r')
        except:
            logging.error(" Could not open file: ", data_file_path+"/"+file_itter)
        lines_of_file = file.readlines()
        
        # Check data is more than 600 days
        if len(lines_of_file) > 600:
            logging.debug("SUCCESS: ", file_itter, "\t File passed size")
        else:
            logging.debug("FAIL:    ", file_itter, "\t File failed size")
            continue

        # Check format on first row
        if check_first_line(lines_of_file[0]):
            logging.debug("SUCCESS: ", file_itter, "\t File passed first row format")
        else:
            logging.debug("FAIL:    ", file_itter, "\t File failed first row format")
            continue
        
        # Check format on first uppcomming rows
        if check_value_rows(lines_of_file[1:]):
            logging.debug("SUCCESS: ", file_itter, "\t File passed value format")
        else:
            logging.debug("FAIL:    ", file_itter, "\t File failed value format")
            continue

        # Check time decreases for each row
        if check_time_decreases_for_each_row(lines_of_file[1:]):
            logging.debug("SUCCESS: ", file_itter, "\t File passed time decreasing with row number")
        else:
            logging.debug("FAIL:    ", file_itter, "\t File failed time decreasing with row number")
            continue

        # Check daily change for each row
        if check_daily_change(lines_of_file[1:]):
            logging.debug("SUCCESS: ", file_itter, "\t File passed daily change")
        else:
            logging.debug("FAIL:    ", file_itter, "\t File failed daily change")
            continue

        # After passing all tests
        logging.debug("SUCCESS: ", file_itter, "\t Passed all tests")
        clean_files.append(file_itter)

        file.close()

    return clean_files

def check_first_line(line):
    words_in_line = line.split(',')

    if words_in_line[0] != "Date":
        return False

    if words_in_line[2] != "Open":
        return False

    return True

def check_value_rows(lines):
    return_value = True

    current_time = datetime.datetime.now()
    today = current_time.year*10000+current_time.month*100+current_time.day


    for line in lines:
        words_in_line = line.split(',')

        try:

            date_value = int(words_in_line[0])
            if date_value < 18000000 or date_value > today:
                return_value = False
        except :
            logging.error("  Date format in data file is in wrong format.")
            
            return False

        

        try:
            opening_value = float(words_in_line[2])
        except :
            logging.error("  Market opening value in data file is in wrong format.")
            return False


    return True

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

def check_daily_change(lines):

    market_values = []

    for line in lines:
        words_in_line = line.split(',')
        market_values.append(float(words_in_line[2]))

    for i, value in enumerate(market_values[1:]):
        change = (int(value)-market_values[i])/market_values[i]
        
        if change<= 1 and change >= -0.6:
            #all is well, do nothing
            continue
        else:
            logging.error(" Unprobable daily change:" ,\
                round(change*100,0), "%. Check line ", i-1 )
            return False
    return True
