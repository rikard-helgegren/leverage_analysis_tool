###### DATA MANAGER ######
from code.test_code.test_callfile_in_different_folder import say_hi
from code.data_manager.check_if_data_files_are_clean import check_if_data_files_are_clean
from code.data_manager.read_and_manage_raw_data import read_and_manage_raw_data

##### CALCULATOR #######

from code.calculator.calcultate_daily_change import calcultate_daily_change

###### MODEL ######
import code.model.constants as constant



################ Data Files ################

data_files_path = "data/raw_data/old"
clean_file_names = []


################ Data Processed ################

data_index_dict = {}



def model_initiate():

    clean_file_names =check_if_data_files_are_clean(data_files_path)
    print("Clean files are:", clean_file_names)

    data_index_dict = read_and_manage_raw_data(data_files_path, clean_file_names)

    data_index_dict = calcultate_daily_change(data_index_dict)


    

def update_model():
    print("hi")

