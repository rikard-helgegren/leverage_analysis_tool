#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import os
import json
import sys
import logging

from src.model.common.convert_between_market_and_dict import dict_of_market_dicts_to_dict_of_market_classes, dict_of_market_classes_to_dict_of_market_dicts

def are_files_preproccessed(clean_file_names):
    logging.debug("are_files_preproccessed")

    file_name = get_filname_based_on_markets(clean_file_names)
    path = "data/pre_calculated/" + file_name

    # Does file exsist
    isFile = os.path.isfile(path)

    return isFile


def load_preproccessed_files(clean_file_names):
    logging.debug("load_preproccessed_files")
    
    file_name = get_filname_based_on_markets(clean_file_names)
    path = "data/pre_calculated/" + file_name

    data = {}
    # Read data from json file
    with open(path) as json_file:
        data = json.load(json_file)

    dict_of_markets = dict_of_market_dicts_to_dict_of_market_classes(data)
    return dict_of_markets


def save_preproccessed_files(clean_file_names, market_dict):
    logging.debug("save_preproccessed_files")
    
    file_name = get_filname_based_on_markets(clean_file_names)
    path = "data/pre_calculated/" + file_name

    dict_of_market_dicts = dict_of_market_classes_to_dict_of_market_dicts(market_dict)

    # Generate json dump
    data_json_format = json.dumps(dict_of_market_dicts)

    # Write data to json file
    file = open(path,"w")
    file.write(data_json_format)
    file.close()


def get_filname_based_on_markets(market_names):
    logging.debug("get_filname_based_on_markets")
    #market_names.sort() #TODO: should i sort or not sort.
    joined_file_string = "".join(market_names)

    encoding = 0
    # Calculate integer code representing market_names
    for value, char in enumerate(joined_file_string): #TODO not garanteeing uniqe
        encoding += ord(char) * value
        encoding = encoding % sys.maxsize

    encoding = str(encoding) + ".json"

    return encoding
