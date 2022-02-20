#!/usr/bin/env python3

from code.test_code.test_callfile_in_different_folder import say_hi
from code.data_manager.check_if_data_files_are_clean import check_if_data_files_are_clean
import code.model.constants as constant


def main():
    
    data_files =check_if_data_files_are_clean(constant.data_files_path)
    print(data_files)


    return 0




############################
main()