#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging

from src.managing_data.check_if_data_files_are_clean import check_if_data_files_are_clean
from src.managing_data.sort_file_names               import sort_file_names
from src.managing_data.read_and_manage_raw_data      import read_and_manage_raw_data

import src.model.constants_model as constants_model
from src.Config import Config

class Market_data_loader:
    _instance = None
    data_files_path  = constants_model.data_files_path

    def __new__(class_instance):
        logging.debug("Market_data_loader: init")
        if class_instance._instance is None:
            class_instance._instance = super(Market_data_loader, class_instance).__new__(class_instance)
            # Initialize data loading here
            class_instance._instance.data = class_instance._instance.load_data() # Placeholder, replace with actual data loading logic
        return class_instance._instance

    def load_data(self):
        """ Check if data files are clean and store the market data in
            Market class objects
        """
        logging.debug("Market_data_loader: load_data")
        clean_file_names = check_if_data_files_are_clean(self.data_files_path)
        sorted_files = sort_file_names(clean_file_names, Config().SORT_RANKING)
        markets = read_and_manage_raw_data(self.data_files_path, sorted_files)
        return markets

    def get_data(self):
        return self.data
    