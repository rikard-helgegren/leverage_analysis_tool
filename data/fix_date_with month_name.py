import os
from os import listdir
from os.path import isfile, join
import datetime 

import fileinput
import sys
import re






def change_date_format():

    clean_files = []
    data_file_path = "raw_data/old_test"

    try:
        all_data_files = [f for f in listdir(data_file_path) if isfile(join(data_file_path, f))]
    except:
        print("ERROR: Path to data files is wrong.")

    # Check each file
    for file_itter in all_data_files:

        counter = 0

        print("TMP: file_itter", file_itter)

        # Read file and lines
        try:
            file = open(data_file_path+"/"+file_itter, 'r') #TODO do it with with
        except:
            print("ERROR: Could not open file: ", data_file_path+"/"+file_itter)

        lines_of_file = file.readlines()

        replacement = ""

        for line in lines_of_file:
            try:
                p = re.compile("(\w+) (\d+) (\d+)(.*)")
                match_one = p.match(line).group(1)
                match_two = p.match(line).group(2)
                match_three = p.match(line).group(3)
                match_four = p.match(line).group(4)
                
                match_one = convert_text_month_to_number(match_one)
                replacement = replacement + match_three + match_one + match_two + match_four + "\n"
            except:
                counter += 1
                if counter < 4:
                    print("No match")
                replacement = replacement + line

        file.close()

        fout = open(data_file_path+"/"+file_itter, "w")
        fout.write(replacement)
        fout.close()


def convert_text_month_to_number(match_one):

    switch={
        "Jan":'01',
        "Feb":'02',
        "Mar":'03',
        "ar" :'03',
        "Apr":'04',
        "May":'05',
        "ay":'05',
        "Jun":'06',
        "Jul":'07',
        "Aug":'08',
        "Sep":'09',
        "Oct":'10',
        "Nov":'11',
        "Dec":'12'
       }

    return switch[match_one]

change_date_format()
