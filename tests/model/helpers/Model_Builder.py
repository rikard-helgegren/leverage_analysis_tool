#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

from copy import deepcopy
import logging

from src.model.Model import Model
from src.model.Performance_key_values import Performance_Key_values
from tests.model.helpers.Market_Builder import Market_Builder

import src.constants as constants
import src.model.common.constants_model as constants_model


class Model_Builder:
    """ This is the model of the application. It models stock market index
        instruments and calculates portfolio performance as well as other
        measures of interest.

        In order to model the instruments and support a range of portfolios
        the model have plenty of variables.
    """
    def __init__(self):
        logging.debug("Model_Builder: __init__")

        self.model = Model()

        ################ Data Files ################

        self.data_files_path  = constants_model.data_files_path
        self.clean_file_names = []

        ############## Config values ###################

        DEFAUT_LOAN = 0
        DEFAUT_YEARS_HISTOGRAM_INTERVAL = 1
        DEFAUT_HARVEST_POINT = 150
        DEFAUT_REFILL_POINT = 50
        DEFAUT_REBALANCE_PERIOD_MONTHS = 6
        DEFAUT_UPDATE_HARVEST_REFILL = 0
        DEFAUT_PROPORTION_FUNDS = 0.9
        DEFAUT_PROPORTION_LEVERAGE = 1 - DEFAUT_PROPORTION_FUNDS
        DEFAUT_INCLUDE_FEES_STATUS = True
        DEFAUT_REBALANCE_BETWEEN_INSTRUMENTS_STATUS = False
        DEFAUT_CORRECTION_OF_INFLATION_STATUS = True
        DEFAUT_CORRECTION_OF_CURRENCY_STATUS = True
        DEFAUT_DELAY_OF_CORRECTION = 0
        DEFAUT_VARIANCE_SAMPLE_SIZE = 10
        DEFAUT_VOLATILITY_STRATEGIE_SAMPLE_SIZE = 50
        DEFAUT_VOLATILITY_STRATEGIE_LEVEL = 0.01
        HIGHEST_LEVERAGE_AVAILABLE = 5

        self.model.loan                                     = DEFAUT_LOAN
        self.model.years_histogram_interval                 = DEFAUT_YEARS_HISTOGRAM_INTERVAL
        self.model.harvest_point                            = DEFAUT_HARVEST_POINT
        self.model.refill_point                             = DEFAUT_REFILL_POINT
        self.model.update_harvest_refill                    = DEFAUT_UPDATE_HARVEST_REFILL
        self.model.rebalance_period_months                  = DEFAUT_REBALANCE_PERIOD_MONTHS
        #self.model.proportion_cash                         = DEFAUT_PROPORTION_CASH
        self.model.proportion_funds                         = DEFAUT_PROPORTION_FUNDS 
        self.model.proportion_leverage                      = DEFAUT_PROPORTION_LEVERAGE
        self.model.include_fees_status                      = DEFAUT_INCLUDE_FEES_STATUS
        self.model.rebalance_between_instruments_status     = DEFAUT_REBALANCE_BETWEEN_INSTRUMENTS_STATUS
        self.model.correction_of_inflation_status           = DEFAUT_CORRECTION_OF_INFLATION_STATUS
        self.model.correction_of_currency_status            = DEFAUT_CORRECTION_OF_CURRENCY_STATUS
        self.model.delay_of_correction                      = DEFAUT_DELAY_OF_CORRECTION
        self.model.chosen_time_interval_start_date          = 0
        self.model.chosen_time_interval_end_date            = 0
        self.model.chosen_time_interval_status              = False
        self.model.portfolio_strategy                       = constants.PORTFOLIO_STRATEGIES[0]
        self.model.default_variance_sample_size              = DEFAUT_VARIANCE_SAMPLE_SIZE
        self.model.default_volatility_strategie_sample_size  = DEFAUT_VOLATILITY_STRATEGIE_SAMPLE_SIZE
        self.model.default_volatility_strategie_level        = DEFAUT_VOLATILITY_STRATEGIE_LEVEL


        ################ Data Processed ################

        self.model.markets = generate_markets()
        """ Dictionary of Market objects representing the data files
            Dictionary keys are same as the market abbreviation
        """

        self.model.instruments_selected = [["A",1],
                                           ["A",2],
                                           ["A",3],
                                           ["B",1],
                                           ["B",2],
                                           ["B",3],
                                           ["C",1],
                                           ["C",2],
                                           ["C",3],
                                           ["D",1],
                                           ["D",2],
                                           ["D",3]]
        """ List of the instruments selected from the GUI Instrument table
            each item is a list with instrument name and leverage
            e.g. [[SP500, 1], [SP500, 5], [OMXS30, 1], ...]
        """

        self.model.portfolio_results_full_time = []
        """ List of the portfolios value for each day with an update.
            The portfolio is made up of all selected instruments
        """

        self.model.portfolio_results_full_time_without_leverage = []
        """ List of the portfolios value for each day with an update.
            The portfolio is made up of only non leverage items. This is
            needed for some statistical performance meters.
        """

        self.model.common_time_interval = []
        """ List of all days in the time span that the selected instruments
            have data for. Missing days within the common time span are added
        """

        self.model.results_for_intervals = []
        """ List of results for all the continuous time intervals of length 
            'self.years_histogram_interval' in the time investigated.
            
            The purpose of this variable is to be ploted in histogram
        """

        self.model.key_values = Performance_Key_values(self)
    
    def instruments_selected(self, list_of_instruments):
        self.model.instruments_selected = list_of_instruments
        return self
    
    def portfolio_strategy(self, portfolio_strategy):
        self.model.portfolio_strategy = portfolio_strategy
        return self
    
    def rebalance_period_months(self, rebalance_period_months):
        self.rebalance_period_months = rebalance_period_months
        return self

    def build(self):
        self.model.markets_selected = markets_selected(self.model.instruments_selected, self.model.markets)
        return self.model


def markets_selected(instruments_selected, markets):
    """ Copy the markets of the instruments selected in the instrument
        table, into the variable self.markets_selected.
    """
    logging.debug("Model: update_market_selected")

    # TODO: this part maybe tries to add same market multiple times, takes some extra time
    markets_selected = {}
    for instrument in instruments_selected:
        name = instrument[0]
        markets_selected[name] = deepcopy(markets[name])

    return markets_selected


def generate_markets():

    marketA = Market_Builder() \
            .time_span([20200101,20200102,20200103]) \
            .values([1,2,3]) \
            .build()
    marketB = Market_Builder() \
            .time_span([20200102,20200103,20200104]) \
            .values([1,2,3]) \
            .build()
    marketC = Market_Builder() \
            .time_span([20100102,20100103,20100104]) \
            .values([1,1.1,1.2]) \
            .build()
    marketD = Market_Builder() \
            .time_span([20220102,20220103,20220104]) \
            .values([1,1,1]) \
            .build()

    markets = {"A": marketA,
               "B": marketB,
               "C": marketC,
               "D": marketD}

    return markets

