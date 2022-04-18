import os
from os import listdir
from os.path import isfile, join
import datetime

import fileinput
import sys
import re



def change_first_row_open_format():

    clean_files = []
    data_file_path = "raw_data/new_test"

    #Open all data files in folder
    try:
        all_data_files = [f for f in listdir(data_file_path) if isfile(join(data_file_path, f))]
    except:
        print("ERROR: Path to data files is wrong.")

    # Check each file
    for file_itter in all_data_files:
        print("TMP: file_itter", file_itter)


        counter_of_missmatch = 0

        # Read file and lines
        try:
            file = open(data_file_path+"/"+file_itter, 'r')
        except:
            print("ERROR: Could not open file: ", data_file_path+"/"+file_itter)

        lines_of_file = file.readlines()

        replacement = ""
        line_one_splited = lines_of_file[0].split(',')


        # Check that "Open" is in the correct wrong place
        if line_one_splited[5] != "open" and line_one_splited[5] != "Open":
            print("This file does not have this problem")
            continue

        #REMOVE: date,close,raw_close,high,low,open,volume

        #Check that data has Date, High, and Low
        if line_one_splited[0] == "Date" or line_one_splited[0] == "date":
            if line_one_splited[1:5] == ['close','raw_close','high','low']:
                print("Setting a first line for this file")
                replacement = "Date,Close,Open,High,Low,Vol,Procentage" + "\n"

        #Shift "Open" (column 6) to column 2
        for line in lines_of_file[1:]:
            try:
                p = re.compile("(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*)")
                match_one = p.match(line).group(1)
                match_two = p.match(line).group(2)
                match_three = p.match(line).group(3)
                match_four = p.match(line).group(4)
                match_five = p.match(line).group(5)
                match_six = p.match(line).group(6)

                replacement = replacement + match_one +","+ match_two +","+ match_six +","+ match_three+","+ match_four+","+ match_five+ "\n"
                print("TMP, match_five",match_five)
            except:
                counter_of_missmatch += 1
                if counter_of_missmatch < 4:
                    print("No match")
                replacement = replacement + line

        file.close()

        #Write to new file
        fout = open(data_file_path+"/"+file_itter, "w")
        fout.write(replacement)
        fout.close()


#Run code
change_first_row_open_format()
