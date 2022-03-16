###### IMPORT DATA MANAGER ######
from code.test_code.test_callfile_in_different_folder import say_hi
from code.data_manager.check_if_data_files_are_clean import check_if_data_files_are_clean
from code.data_manager.read_and_manage_raw_data import read_and_manage_raw_data

##### IMPORT CALCULATOR #######

from code.calculator.calcultate_daily_change import calcultate_daily_change

###### IMPORT MODEL ######
import code.model.constants as constants


class Model:
    def __init__(self):
        self.view = None 

        ################ Data Files ################

        self.data_files_path = "data/raw_data/old"
        self.clean_file_names = []


        ############## Simple values ###################

        self.loan                                 = constants.DEFULT_LOAN
        self.years_investigating                  = constants.DEFULT_YEARS_INVESTIGATING
        self.harvest_point                        = constants.DEFULT_HARVEST_POINT
        self.refill_point                         = constants.DEFULT_REFILL_POINT
        self.update_harvest_refill                = constants.DEFULT_UPDATE_HARVEST_REFILL
        self.amount_cash                          = constants.DEFULT_AMOUNT_CASH
        self.amount_funds                         = constants.DEFULT_AMOUNT_FUNDS 
        self.amount_leverage                      = constants.DEFULT_AMOUNT_LEVERAGE
        self.include_fees_status                  = constants.DEFULT_INCLUDE_FEES_STATUS
        self.rebalance_status                     = constants.DEFULT_REBALANCE_STATUS
        self.rebalance_between_instruments_status = constants.DEFULT_REBALANCE_BETWEEN_INSTRUMENTS_STATUS
        self.correctino_of_inflation_status       = constants.DEFULT_CORRECTION_OF_INFLATION_STATUS
        self.correctino_of_currency_status        = constants.DEFULT_CORRECTION_OF_CURRENCY_STATUS
        self.delay_of_correction                  = constants.DEFULT_DELAY_OF_CORRECTION

        ################ Data Processed ################

        self.data_index_dict = {}
        self.instruments_selected = [] # Tuples (index, leverage) 



    def model_initiate(self):

        clean_file_names = check_if_data_files_are_clean(self.data_files_path)
        print("Clean files are:", clean_file_names)
        self.data_index_dict = read_and_manage_raw_data(self.data_files_path, clean_file_names)
        self.data_index_dict = calcultate_daily_change(self.data_index_dict)
        print("dict:", self.data_index_dict['omx Stockholm 30.csv'].keys())
        

    def update_model():
        print("model: update_model")
        #TODO


    def set_include_fee_status(self, include_fee_status):
        print("Model, fee_status:", include_fee_status)
        self.include_fees_status = include_fee_status

