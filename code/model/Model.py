#!/usr/bin/env python3

###### IMPORT DATA MANAGER ######
from code.data_manager.check_if_data_files_are_clean import check_if_data_files_are_clean
from code.data_manager.read_and_manage_raw_data import read_and_manage_raw_data

##### IMPORT CALCULATOR #######

from code.model.calcultate_daily_change import calcultate_daily_change
from code.model.calculate_outcomes import calculate_outcomes
from code.model.fill_in_missing_dates import fill_in_missing_dates

###### IMPORT MODEL ######
import code.model.constants as constants


class Model:
    def __init__(self):
        print("TRACE: Model: __init__")
        self.view = None 

        ################ Data Files ################

        self.data_files_path  = "data/raw_data/old_fixed"
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

        self.data_index_dict      = {}
        self.instruments_selected = [] # Tuples (index, leverage)
        self.combined_outcomes_time_intervall = []
        self.combined_outcomes_full_time = []



    def model_initiate(self):
        print("TRACE: Model: model_initiate")

        clean_file_names = check_if_data_files_are_clean(self.data_files_path)
        print("Clean files are:", clean_file_names)
        self.data_index_dict = read_and_manage_raw_data(self.data_files_path, clean_file_names)
        self.data_index_dict = fill_in_missing_dates(self.data_index_dict)
        self.data_index_dict = calcultate_daily_change(self.data_index_dict)
        print("TMP: dict omx:", self.data_index_dict['omx Stockholm 30.csv'].keys())
        

    def update_model(self):
        print("TRACE: Model: update_model")

        calculate_outcomes(self)

        #TODO

        #self.calculate_graph()
        #self.calculate_hist()




    ##########################
    #  Getters and Setters
    ##########################
    def get_loan(self):
        print("TRACE: Model: get_loan")
        return self.loan
    def set_loan(self, loan):
        print("TRACE: Model: set_loan")
        self.loan = loan
    
    def get_years_investigating(self):
        print("TRACE: Model: get_years_investigating")
        return self.years_investigating
    def set_years_investigating(self, years):
        print("TRACE: Model: set_years_investigating")
        self.years_investigating = years

    def get_harvest_point(self):
        print("TRACE: Model: get_harvest_point")
        return self.harvest_point
    def set_harvest_point(self, harvest_point):
        print("TRACE: Model: set_harvest_point")
        self.harvest_point = harvest_point

    def get_refill_point(self):
        print("TRACE: Model: get_refill_point")
        return self.refill_point
    def set_refill_point(self, refill_point):
        print("TRACE: Model: set_refill_point")
        self.refill_point = refill_point

    def get_update_harvest_refill(self):
        print("TRACE: Model: get_update_harvest_refill")
        return self.update_harvest_refill
    def set_update_harvest_refill(self, update_harvest_refill):
        self.update_harvest_refill = update_harvest_refill

    def get_amount_cash(self):
        print("TRACE: Model: get_amount_cash")
        return self.amount_cash
    def set_amount_cash(self, amount_cash):
        print("TRACE: Model: set_amount_cash")
        self.amount_cash = amount_cash

    def get_amount_funds(self):
        print("TRACE: Model: get_amount_funds")
        return self.amount_funds
    def set_amount_funds(self, amount_funds):
        print("TRACE: Model: set_amount_funds")
        self.amount_funds = amount_funds

    def get_amount_leverage(self):
        return self.amount_leverage
        print("TRACE: Model: get_amount_leverage")
    def set_amount_leverage(self, amount_leverage):
        print("TRACE: Model: set_amount_leverage")
        self.amount_leverage = amount_leverage

    def get_include_fees_status(self):
        print("TRACE: Model: get_include_fees_status")
        return self.include_fee_status
    def set_include_fee_status(self, include_fee_status):
        print("TRACE: Model: set_include_fee_status")
        self.include_fees_status = include_fee_status
        print("Model, fee_status:", include_fee_status)

    def get_rebalance_status(self):
        print("TRACE: Model: get_rebalance_status")
        return self.rebalance_status
    def set_rebalance_status(self, rebalance_status):
        print("TRACE: Model: set_rebalance_status")
        self.set_rebalance_status = rebalance_status

    def get_rebalance_between_instruments_status(self):
        print("TRACE: Model: get_rebalance_between_instruments_status")
        return self.rebalance_between_instruments_status
    def set_rebalance_between_instruments_status(self, rebalance_between_instruments_status):
        print("TRACE: Model: set_rebalance_between_instruments_status")
        self.rebalance_between_instruments_status = rebalance_between_instruments_status

    def get_correctino_of_inflation_status(self):
        print("TRACE: Model: get_correctino_of_inflation_status")
        return self.correctino_of_inflation_status
    def set_correctino_of_inflation_status(self, correctino_of_inflation_status):
        print("TRACE: Model: set_rebalance_between_instruments_status")
        self.correctino_of_inflation_status = correctino_of_inflation_status

    def get_correctino_of_currency_status(self):
        print("TRACE: Model: get_correctino_of_currency_status")
        return self.correctino_of_currency_status
    def set_correctino_of_currency_status(self, correctino_of_currency_status):
        print("TRACE: Model: set_correctino_of_currency_status")
        self.correctino_of_currency_status = correctino_of_currency_status

    def get_delay_of_correction(self):
        print("TRACE: Model: get_delay_of_correction")
        return self.delay_of_correction
    def set_delay_of_correction(self, delay_of_correction):
        print("TRACE: Model: set_delay_of_correction")
        self.delay_of_correction = delay_of_correction

    def get_data_index_dict(self):
        print("TRACE: Model: get_data_index_dict")
        return self.data_index_dict
    def set_data_index_dict(self, data_index_dict):
        print("TRACE: Model: set_data_index_dict")
        self.data_index_dict = data_index_dict

    def get_instruments_selected(self):
        print("TRACE: Model: get_instruments_selected")
        return self.instruments_selected
    def set_instruments_selected(self, instruments_selected):
        print("TRACE: Model: set_instruments_selected")
        self.instruments_selected = instruments_selected

    def get_combined_outcomes_time_intervall(self):
        print("TRACE: Model: get_combined_outcomes_time_intervall")
        return self.combined_outcomes_time_intervall
    def set_combined_outcomes_time_intervall(self, combined_outcomes_time_intervall):
        print("TRACE: Model: set_combined_outcomes_time_intervall")
        self.combined_outcomes_time_intervall = combined_outcomes_time_intervall

    def get_combined_outcomes_full_time(self):
        print("TRACE: Model: get_combined_outcomes_full_time")
        return self.combined_outcomes_full_time
    def set_combined_outcomes_full_time(self, combined_outcomes_full_time):
        print("TRACE: Model: set_combined_outcomes_full_time")
        self.combined_outcomes_full_time = combined_outcomes_full_time




    ######################
    #
    ######################





    def update_instrument_selected(self, table_focus_item ):
        print("TRACE: Model: update_instrument_selected")
        if table_focus_item in self.instruments_selected:
            self.instruments_selected.remove(table_focus_item)
        else:
            self.instruments_selected.append(table_focus_item)
