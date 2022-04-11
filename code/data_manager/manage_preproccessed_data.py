
import os
import json
import sys

def are_files_preproccessed(clean_file_names):
    print("TRACE: are_files_preproccessed")

    file_name = get_filname_from_indexes(clean_file_names)
    path = "data/pre_calculated/" + file_name

    # Does file exsist
    isFile = os.path.isfile(path)

    return isFile


def load_preproccessed_files(clean_file_names):
    print("TRACE: load_preproccessed_files")
    
    file_name = get_filname_from_indexes(clean_file_names)
    path = "data/pre_calculated/" + file_name

    data = {}
    # Read data from json file
    with open(path) as json_file:
        data = json.load(json_file)
        
    return data


def save_preproccessed_files(clean_file_names, dict_of_indexes):
    print("TRACE: save_preproccessed_files")
    
    file_name = get_filname_from_indexes(clean_file_names)
    path = "data/pre_calculated/" + file_name

    # Generate json dump
    data_json_format = json.dumps(dict_of_indexes)

    # Write data to json file
    file = open(path,"w")
    file.write(data_json_format)
    file.close()


def get_filname_from_indexes(indexes): 
    print("TRACE: get_filname_from_indexes")
    #indexes.sort() #TODO: should i sort or not sort. 
    joined_file_string = "".join(indexes)

    encoding = 0
    # Calculate integer code representing indexes
    for value, char in enumerate(joined_file_string): #TODO not garanteeing uniqe
        encoding += ord(char) * value
        encoding = encoding % sys.maxsize

    encoding = str(encoding) + ".json"

    return encoding
