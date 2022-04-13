
import os
import json
import sys

from code.model.convert_between_market_and_dict import dict_of_market_dicts_to_dict_of_market_classes, dict_of_market_classes_to_dict_of_market_dicts

def are_files_preproccessed(clean_file_names):
    print("TRACE: are_files_preproccessed")

    file_name = get_filname_based_on_markets(clean_file_names)
    path = "data/pre_calculated/" + file_name

    # Does file exsist
    isFile = os.path.isfile(path)

    return isFile


def load_preproccessed_files(clean_file_names):
    print("TRACE: load_preproccessed_files")
    
    file_name = get_filname_based_on_markets(clean_file_names)
    path = "data/pre_calculated/" + file_name

    data = {}
    # Read data from json file
    with open(path) as json_file:
        data = json.load(json_file)

    dict_of_markets = dict_of_market_dicts_to_dict_of_market_classes(data)
    return dict_of_markets


def save_preproccessed_files(clean_file_names, market_dict):
    print("TRACE: save_preproccessed_files")
    
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
    print("TRACE: get_filname_based_on_markets")
    #market_names.sort() #TODO: should i sort or not sort.
    joined_file_string = "".join(market_names)

    encoding = 0
    # Calculate integer code representing market_names
    for value, char in enumerate(joined_file_string): #TODO not garanteeing uniqe
        encoding += ord(char) * value
        encoding = encoding % sys.maxsize

    encoding = str(encoding) + ".json"

    return encoding
