#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import ctypes
import logging

import src.model.common.constants_model as constants_model
import src.constants as constants


def rebalance_hist_ctypes(model):

    ## C++ interactions ##
    cpp_compiled_so_file = constants_model.program_folder + constants_model.hist_harvest_refill_algo_file
    lib_object_cpp = ctypes.CDLL(cpp_compiled_so_file)

    ## get variables and pass to function ##
    cpp_algorithm = lib_object_cpp.calculateHistogramOutput # Set upp function call

    # input types and values
    [all_argtypes_list, all_values_list] = get_indata(model)
    cpp_algorithm.argtypes = all_argtypes_list
    cpp_algorithm.restype = ctypes.POINTER(ctypes.c_float)

    # make actual call
    return_data = cpp_algorithm(*all_values_list) #TODO fix return value is cpp float pointer
    
    nr_days_in_data = get_nbr_of_days_in_investment_items(model)

    size_return_data = nr_days_in_data - model.years_histogram_interval * constants_model.MARKET_DAYS_IN_YEAR

    # Do not include days only used for strategy
    if model.get_portfolio_strategy() == constants.PORTFOLIO_STRATEGIES[4]:
        return_data_python_format = [return_data[i] for i in range(model.get_volatility_strategie_sample_size(), size_return_data)]
    else:
        return_data_python_format = [return_data[i] for i in range(size_return_data)]

    return return_data_python_format


# Set up values and types that are to be sent to cpp
def get_indata(model):
    all_argtypes = []
    all_values = []

    ### loan ###
    all_argtypes.append(ctypes.c_float)
    all_values.append(model.get_loan())


    ### instrument selected ###
    instruments_selected = model.get_instruments_selected()
    names_instruments_selected, leverage_instruments_selected = zip(*instruments_selected)

    # leverage list
    all_argtypes.append(ctypes.c_int * len(instruments_selected))
    all_values.append((ctypes.c_int * len(leverage_instruments_selected))(*leverage_instruments_selected))

    # length of instruments_selected
    all_argtypes.append(ctypes.c_int)
    all_values.append(len(leverage_instruments_selected))

    # instrument names
    all_argtypes.append(ctypes.c_char_p)
    all_values.append((','.join(names_instruments_selected)).encode())


    ### proportion_funds ###
    all_argtypes.append(ctypes.c_float)
    all_values.append(model.get_proportion_funds())


    ### proportion_leverage ###
    all_argtypes.append(ctypes.c_float)
    all_values.append(model.get_proportion_leverage())


    ### markets_selected ###
    markets_selected = model.get_markets_selected()
    nr_days_in_data = get_nbr_of_days_in_investment_items(model)

    # end pos
    all_argtypes.append(ctypes.c_int)
    all_values.append(nr_days_in_data)

    # number of markets selected
    all_argtypes.append(ctypes.c_int)
    all_values.append(len(markets_selected.keys()))

    # prep variables
    countries = []
    daily_change = []
    for key in markets_selected.keys():
        countries.append(markets_selected[key].get_country())
        current_daily_change = markets_selected[key].get_daily_change()
        daily_change.append((ctypes.c_float * len(current_daily_change))(*current_daily_change))

    # daily change
    all_argtypes.append(ctypes.POINTER(ctypes.c_float) * len(markets_selected.keys()))
    all_values.append(((ctypes.POINTER(ctypes.c_float) * len(daily_change))(*daily_change)))  # passing list of float pointers

    # index names
    all_argtypes.append(ctypes.c_char_p)
    index_names = markets_selected.keys()
    all_values.append((','.join(index_names)).encode())  # make list to string and encode

    # time horizon days investing
    all_argtypes.append(ctypes.c_int)
    all_values.append(model.years_histogram_interval*constants_model.MARKET_DAYS_IN_YEAR)

    ### Harvest refill limits ###
    all_argtypes.append(ctypes.c_float)
    all_values.append(model.get_harvest_point()/constants.CONVERT_PERCENT)
    all_argtypes.append(ctypes.c_float)
    all_values.append(model.get_refill_point()/constants.CONVERT_PERCENT)

    ### rebalance period ###
    all_argtypes.append(ctypes.c_int)
    all_values.append(int(model.get_rebalance_period_months()*constants_model.MARKET_DAYS_IN_YEAR/constants_model.MONTHS_IN_YEAR))

    # strategy
    all_argtypes.append(ctypes.c_int)
    strategy = model.get_portfolio_strategy()
    if strategy == constants.PORTFOLIO_STRATEGIES[1]:
        all_values.append(1)
    elif strategy == constants.PORTFOLIO_STRATEGIES[2]:
        all_values.append(2)
    elif strategy == constants.PORTFOLIO_STRATEGIES[4]:
        all_values.append(4)
    else:
        logging.error("Unexpected startegy")


    ### Variance ###
    all_argtypes.append(ctypes.c_int)
    all_values.append(model.get_volatility_strategie_sample_size())
    
    all_argtypes.append(ctypes.c_int)
    all_values.append(model.get_variance_calc_sample_size())
    
    all_argtypes.append(ctypes.c_float)
    all_values.append(model.get_volatility_strategie_level())

    ### Use Fee ###
    all_argtypes.append(ctypes.c_bool)
    all_values.append(model.get_include_fees_status())

    ### Out data ###
    all_argtypes.append(ctypes.c_float * nr_days_in_data)
    return_data = [0] * nr_days_in_data  # initiate with zeros   # TODO whait should not this be too many? should be - days in intervall. but no?!?
    all_values.append((ctypes.c_float * len(return_data))(*return_data))

    return [all_argtypes, all_values]


def get_nbr_of_days_in_investment_items(model):
    """ All items have the same number of days.
        This function takes the first item and returns its number of days
    """
    instruments_selected = model.get_instruments_selected()
    markets_selected = model.get_markets_selected()
    a_instrument = instruments_selected[0]
    market = markets_selected[a_instrument[0]]
    nbr_of_days_in_investment_item = len(market.get_time_span())

    return nbr_of_days_in_investment_item
