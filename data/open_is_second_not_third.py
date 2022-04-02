import os
from os import listdir
from os.path import isfile, join
import datetime 

import fileinput
import sys
import re



def change_first_row_open_format():

    clean_files = []
    data_file_path = "raw_data/old_test"

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
        if line_one_splited[1] != "Open":
            print("This file does not have this problem")
            continue

        #Check that data has Date, High, and Low
        if line_one_splited[0] == "Date":
            if line_one_splited[2:4] == ['High', 'Low']:
                print("Setting a first line for this file")
                replacement = "Date,-,Open,High,Low,Vol,Procentage" + "\n"
        
        #Add a extra column to shift "Open" to column 2
        for line in lines_of_file[1:]:
            try:
                p = re.compile("([0-9]+)(.*)")
                match_one = p.match(line).group(1)
                match_two = p.match(line).group(2)
                
                replacement = replacement + match_one + ', -' + match_two + "\n"
            except:
                counter_of_missmatch += 1
                if counter_of_missmatch < 4:
                    print("No match")
                replacement = replacement + line

        file.close()

        #Write to new file
        fout = open("raw_data/old_test/"+file_itter, "w")
        fout.write(replacement)
        fout.close()
        

#Run code
change_first_row_open_format()