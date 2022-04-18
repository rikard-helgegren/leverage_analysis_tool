import os
from os import listdir
from os.path import isfile, join
import datetime

import fileinput
import sys
import re






def change_date_format():

    clean_files = []
    data_file_path = "raw_data/new_test"

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
                p = re.compile("(\d+)\-(\d+)\-(\d+)(.*)")
                match_one = p.match(line).group(1)
                match_two = p.match(line).group(2)
                match_three = p.match(line).group(3)
                match_four = p.match(line).group(4)

                replacement = replacement + match_one + match_two + match_three + match_four + "\n"
            except:
                counter += 1
                if counter < 4:
                    print("No match")
                replacement = replacement + line

        file.close()

        fout = open(data_file_path+"/"+file_itter, "w")
        fout.write(replacement)
        fout.close()


change_date_format()
