from copy import deepcopy

###### IMPORT DATA MANAGER ######
from code.data_manager.check_if_data_files_are_clean import check_if_data_files_are_clean
from code.data_manager.read_and_manage_raw_data      import read_and_manage_raw_data
from code.data_manager.manage_preproccessed_data     import are_files_preproccessed
from code.data_manager.manage_preproccessed_data     import load_preproccessed_files
from code.data_manager.manage_preproccessed_data     import save_preproccessed_files

###### IMPORT MODEL ######
from code.model.calcultate_daily_change          import calcultate_daily_change
from code.model.calculate_graph_outcomes         import calculate_graph_outcomes
from code.model.fill_in_missing_dates            import fill_in_missing_dates
from code.model.fill_in_missing_dates_improved   import fill_gaps_data
from code.model.calculate_common_time_interval   import calculate_common_time_interval

from code.model.convert_between_market_and_dict import dict_of_market_dicts_to_dict_of_market_classes, dict_of_market_classes_to_dict_of_market_dicts


import code.model.constants as constants

class Model:
    """ This is the model of the application. It models stock market index
        instruments and calculates portfolio performance as well as other
        measures of intrest.

        In order to model the instruments and suport a range of portfolios
        the model have plenty of variables.
    """
    def __init__(self):
        print("TRACE: Model: __init__")

        ################ Data Files ################

        self.data_files_path  = "data/raw_data/all"
        self.clean_file_names = []


        ############## Simple values ###################

        self.loan                                 = constants.DEFULT_LOAN
        self.years_investigating                  = constants.DEFULT_YEARS_INVESTIGATING
        self.harvest_point                        = constants.DEFULT_HARVEST_POINT
        self.refill_point                         = constants.DEFULT_REFILL_POINT
        self.update_harvest_refill                = constants.DEFULT_UPDATE_HARVEST_REFILL
        self.proportion_cash                      = constants.DEFULT_PROPORTION_CASH
        self.proportion_funds                     = constants.DEFULT_PROPORTION_FUNDS 
        self.proportion_leverage                  = constants.DEFULT_PROPORTION_LEVERAGE
        self.include_fees_status                  = constants.DEFULT_INCLUDE_FEES_STATUS
        self.rebalance_status                     = constants.DEFULT_REBALANCE_STATUS
        self.rebalance_between_instruments_status = constants.DEFULT_REBALANCE_BETWEEN_INSTRUMENTS_STATUS
        self.correctino_of_inflation_status       = constants.DEFULT_CORRECTION_OF_INFLATION_STATUS
        self.correctino_of_currency_status        = constants.DEFULT_CORRECTION_OF_CURRENCY_STATUS
        self.delay_of_correction                  = constants.DEFULT_DELAY_OF_CORRECTION

        ################ Data Processed ################

        self.markets                          = {}
        """ Dictionary of Market objects representing the data files
            Dictionary keys are same as the market abbriviation
        """

        self.markets_selected                 = {}
        """ Dictionary of Market objects selected from the GUI Instrument table
            Coppies of the self.markets, and theese will be modified as needed to be compatible
        """

        self.instruments_selected             = []
        """ List of the instruments selected from the GUI Instrument table
            each item is a list with instrument name and leverage
            e.g. [[SP500, 1], [SP500, 5], [OMXS30, 1], ...]
        """

        self.portfolio_results_full_time      = []
        """ List of the portfolios value for each day with an update.
            The portfolio is made up of all selected instruments
        """

        self.common_time_intervall            = []
        """ List of all days in the time span that the selected instruments
            have data for. Missing days within the common time span are added
        """

    ######################
    # Central methods
    ######################

    def model_import_data(self):
        """ Check if data fiels are clean and store the market data in
            Market class objects
        """
        print("TRACE: Model: model_import_data")
        clean_file_names = check_if_data_files_are_clean(self.data_files_path)
        self.markets = read_and_manage_raw_data(self.data_files_path, clean_file_names)


    def update_model(self):
        """ Make the markets selected compatible, and calculate the new results"""
        print("TRACE: Model: update_model")

        self.markets_selected = fill_gaps_data(self.markets_selected)
        self.markets_selected = calcultate_daily_change(self.markets_selected)

        calculate_graph_outcomes(self)
        self.common_time_intervall = calculate_common_time_interval(self) # TODO: doing double work

        #TODO self.calculate_hist()


    ######################
    # Other methods
    ######################


    def update_instrument_selected(self, table_focus_item_data ):
        """ Update the instruments selected based on what item was
            selected in the table of instruments.

            Param: table_focus_item_data: [Name: String, leverage: Int]
        """
        print("TRACE: Model: update_instrument_selected")
        if table_focus_item_data in self.instruments_selected:
            self.instruments_selected.remove(table_focus_item_data)
        else:
            self.instruments_selected.append(table_focus_item_data)

        self.update_market_selected()


    def update_market_selected(self):
        """ Coppy the markets of the instruments selected in the instrument
            table, into the variable self.markets_selected.
        """
        print("TRACE: Model: update_market_selected")

        #TODO: can try to add same instrument multiple times, takes some extra time
        self.markets_selected = {}
        for instrument in self.instruments_selected:
            name = instrument[0]
            self.markets_selected[name] = deepcopy(self.markets[name])




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

    def get_proportion_cash(self):
        print("TRACE: Model: get_proportion_cash")
        return self.proportion_cash
    def set_proportion_cash(self, proportion_cash):
        print("TRACE: Model: set_proportion_cash")
        self.proportion_cash = proportion_cash

    def get_proportion_funds(self):
        print("TRACE: Model: get_proportion_funds")
        return self.proportion_funds
    def set_proportion_funds(self, proportion_funds):
        print("TRACE: Model: set_proportion_funds")
        self.proportion_funds = proportion_funds

    def get_proportion_leverage(self):
        return self.proportion_leverage
        print("TRACE: Model: get_proportion_leverage")
    def set_proportion_leverage(self, proportion_leverage):
        print("TRACE: Model: set_proportion_leverage")
        self.proportion_leverage = proportion_leverage

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

    def get_markets(self):
        print("TRACE: Model: get_markets")
        return self.markets
    def set_markets(self, markets):
        print("TRACE: Model: set_markets")
        self.markets = markets

    def get_instruments_selected(self):
        print("TRACE: Model: get_instruments_selected")
        return self.instruments_selected
    def set_instruments_selected(self, instruments_selected):
        print("TRACE: Model: set_instruments_selected")
        self.instruments_selected = instruments_selected

    def get_portfolio_results_full_time(self):
        print("TRACE: Model: get_portfolio_results_full_time")
        return self.portfolio_results_full_time
    def set_portfolio_results_full_time(self, portfolio_results_full_time):
        print("TRACE: Model: set_portfolio_results_full_time")
        self.portfolio_results_full_time = portfolio_results_full_time

    def get_common_time_intervall(self):
        print("TRACE: Model: get_common_time_intervall")
        return self.common_time_intervall
    def set_common_time_intervall(self, common_time_intervall):
        print("TRACE: Model: set_common_time_intervall")
        self.common_time_intervall = common_time_intervall

    def get_markets_selected(self):
        print("TRACE: Model: get_markets_selected")
        return self.markets_selected
    def set_markets_selected(self, markets_selected):
        print("TRACE: Model: set_markets_selected")
        slef.markets_selected = markets_selected

