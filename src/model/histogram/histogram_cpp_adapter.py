#!/usr/bin/env python3
#
# Copyright (C) 2024 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import ctypes
import logging

import src.model.constants_model as constants_model
import src.constants as constants
import src.model.common.cpp_adapter as cpp_adapter


def rebalance_hist_ctypes(model):
    logging.debug("histogram_cpp_adapter: rebalance_hist_ctypes")

    ## C++ interactions ##
    cpp_compiled_so_file = constants_model.calculate_histogram_output_file
    lib_object_cpp = ctypes.CDLL(cpp_compiled_so_file)

    ## get variables and pass to function ##
    cpp_algorithm = lib_object_cpp.calculateHistogramOutput # Set upp function call

    # input types and values
    [all_argtypes_list, all_values_list] = get_in_data_for_cpp(model)
    cpp_algorithm.argtypes = all_argtypes_list
    cpp_algorithm.restype = ctypes.POINTER(ctypes.c_float)

    # make actual call
    logging.debug("histogram_cpp_adapter: Just before entering C++ realm")
    return_data = cpp_algorithm(*all_values_list) #TODO fix return value is cpp float pointer
    logging.debug("histogram_cpp_adapter: returned from C++ realm")
    
    nr_days_in_data = cpp_adapter.get_nbr_of_days_in_investment_items(model)

    size_return_data = nr_days_in_data - int(model.years_histogram_interval * constants_model.MARKET_DAYS_IN_YEAR)

    # Do not include days only used for strategy
    if model.get_portfolio_strategy() == constants.PORTFOLIO_STRATEGIES[4]:
        return_data_python_format = [return_data[i] for i in range(model.get_volatility_strategie_sample_size(), size_return_data)]
    else:
        return_data_python_format = [return_data[i] for i in range(size_return_data)]

    return return_data_python_format


def get_in_data_for_cpp(model):

    [common_argtypes_list, common_values_list] = cpp_adapter.get_common_indata(model)
    [histogram_argtypes_list, histogram_values_list] = get_hist_indata(model)

    all_argtypes_list = common_argtypes_list + histogram_argtypes_list
    all_values_list = common_values_list + histogram_values_list

    return [all_argtypes_list, all_values_list]

def get_hist_indata(model):
    hist_argtypes_list = []
    hist_values_list = []

    # time horizon days investing
    hist_argtypes_list.append(ctypes.c_int)
    hist_values_list.append(int(model.years_histogram_interval*constants_model.MARKET_DAYS_IN_YEAR))

    return [hist_argtypes_list, hist_values_list]
