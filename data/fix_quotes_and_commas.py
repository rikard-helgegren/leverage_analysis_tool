import os
from os import listdir
from os.path import isfile, join
import datetime 

import fileinput
import sys
import re




#!/usr/bin/env python3
import numpy as np
import csv



#x = ",".join(myList)
global reader

def fix_quotes_and_commas():

    clean_files = []
    data_file_path = "raw_data/old_test"

    # Read file and lines
    try:
        all_data_files = [f for f in listdir(data_file_path) if isfile(join(data_file_path, f))]
    except:
        print("ERROR: Path to data files is wrong.")

    # Check each file
    for file_itter in all_data_files:
        print("TMP: file_itter", file_itter)

        replacement = ""


        # Read file and lines
        try:
            csvfile = open(data_file_path+"/"+file_itter)
            first_row = next(csvfile)
            reader = csv.reader(csvfile,)
        except:
            print("ERROR: Could not open file: ", data_file_path+"/"+file_itter)

        replacement = first_row
        count_nice_lines = 0
        
        for row in reader: # each row is a list
            one_line = ""

            #replace commas in string. Should only exsist between items in list
            if ',' in row[1]:
                count_nice_lines = 0
                for string in row:
                    one_line = one_line + string.replace(",",".") + ','

            else:
                # This is not a common problem for this file
                if count_nice_lines > 4:
                    print("Abort clean up")
                    break
                count_nice_lines = count_nice_lines + 1 
                one_line = ",".join(row)

            replacement = replacement + one_line + "\n"

        #Make sure not to write to file furter down
        if count_nice_lines > 4:
            print("Abort dubble time")
            continue

        #Write to new file
        fout = open("raw_data/old_test/"+file_itter, "w")
        fout.write(replacement)
        fout.close()   
        
        
#Run code
fix_quotes_and_commas()