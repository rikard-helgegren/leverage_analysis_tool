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

        counter = 0

        print("TMP: file_itter", file_itter)

        # Read file and lines
        try:
            file = open(data_file_path+"/"+file_itter, 'r')
        except:
            print("ERROR: Could not open file: ", data_file_path+"/"+file_itter)

        lines_of_file = file.readlines()

        replacement = ""
        line_one_splited_two = lines_of_file[2].split(',')
        line_one_splited_three = lines_of_file[3].split(',')

        #Check that time line is backwards (only two inctances) 
        if line_one_splited_two[0] > line_one_splited_three[0]:
            print("This file does not have this problem")
            continue


        print("Making a fix")

        # Reverse all rows except first
        for line in lines_of_file[1:]:
            replacement = line + replacement + "\n"

        #Add first row
        replacement = lines_of_file[0] + replacement + "\n"
        file.close()

        #Write to new file
        fout = open("raw_data/old_test/"+file_itter, "w")
        fout.write(replacement)
        fout.close()
        

#Run code
change_first_row_open_format()