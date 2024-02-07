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
import numpy as np

import src.model.common.constants_model as constants_model
import src.constants as constants
import src.model.common.cpp_adapter as cpp_adapter


def graph_ctypes(model):
    logging.debug("graph_cpp_adapter: graph_ctypes")

    ## C++ interactions ##
    cpp_compiled_so_file = constants_model.calculate_graph_output_file
    lib_object_cpp = ctypes.CDLL(cpp_compiled_so_file)

    ## get variables and pass to function ##
    cpp_algorithm = lib_object_cpp.calculateGraphOutput # Set upp function call

    # input types and values
    [all_argtypes_list, all_values_list] = get_in_data_for_cpp(model)
    cpp_algorithm.argtypes = all_argtypes_list
    cpp_algorithm.restype = ctypes.POINTER(ctypes.c_float)

    # make actual call
    logging.debug("graph_cpp_adapter: Just before entering C++ realm")
    return_data = cpp_algorithm(*all_values_list) #TODO fix return value is cpp float pointer
    logging.debug("graph_cpp_adapter: returned from C++ realm")

    nr_days_in_data = cpp_adapter.get_nbr_of_days_in_investment_items(model)

    size_return_data = nr_days_in_data + 1 

    # Do not include days only used for strategy
    if model.get_portfolio_strategy() == constants.PORTFOLIO_STRATEGIES[4]:
        return_data_python_format = [return_data[i] for i in range(model.get_volatility_strategie_sample_size(), size_return_data -1)]
    else:
        return_data_python_format = [return_data[i] for i in range(size_return_data -1)] # TODO, unsure why need -1 but got graph data bug, read unitionated value from c-list
        #return_data_python_format = np.ctypeslib.as_array(return_data, shape=(size_return_data,))
    set_buy_sell_data_in_model(all_values_list, model)

    retList = return_data_python_format

    return retList



def get_in_data_for_cpp(model):
    logging.debug("graph_cpp_adapter: get_in_data_for_cpp")

    [common_argtypes_list, common_values_list] = cpp_adapter.get_common_indata(model)
    [graph_argtypes_list, graph_values_list] = get_graph_indata(model)

    all_argtypes_list = common_argtypes_list + graph_argtypes_list
    all_values_list = common_values_list + graph_values_list

    return [all_argtypes_list, all_values_list]

def get_graph_indata(model):
    logging.debug("graph_cpp_adapter: get_graph_indata")
    graph_argtypes_list = []
    graph_values_list = []

    nr_days_in_data = cpp_adapter.get_nbr_of_days_in_investment_items(model)

    # Data to be set in C++ then accessed uding pointer
    graph_argtypes_list.append(ctypes.c_int * nr_days_in_data)
    transaction_dates = [0] * nr_days_in_data  # initiate with zeros 
    graph_values_list.append((ctypes.c_int * len(transaction_dates))(*transaction_dates))

    graph_argtypes_list.append(ctypes.c_int * nr_days_in_data)
    transaction_type = [0] * nr_days_in_data  # initiate with zeros   
    graph_values_list.append((ctypes.c_int * len(transaction_type))(*transaction_type))

    return [graph_argtypes_list, graph_values_list]

def set_buy_sell_data_in_model(all_values_list, model):
    logging.debug("graph_cpp_adapter: set_buy_sell_data_in_model")

    transaction_dates_index = -2 #index of transaction dates in all_values_list
    transaction_action_index  = -1 #index of transaction action in all_values_list
    buy_sell_date   = all_values_list[transaction_dates_index]
    buy_sell_date   = [buy_sell_date[i] for i in range(len(buy_sell_date)) if buy_sell_date[i] != 0]
    buy_sell_type   = all_values_list[transaction_action_index]
    buy_sell_action = [buy_sell_type[i] for i in range(len(buy_sell_type)) if buy_sell_type[i] != 0]
    model.set_buy_sell_by_lists(buy_sell_date, buy_sell_action)
