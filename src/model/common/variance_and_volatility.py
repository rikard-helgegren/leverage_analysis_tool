#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import numpy as np
import logging
import src.model.common.constants_model as constants_model
from src.Config import Config


def calc_volatility(performance_full_time, sample_size = Config().DEFAUT_VARIANCE_SAMPLE_SIZE):
    """Calculate volatility of time period"""
    return np.sqrt(calc_variance(performance_full_time, sample_size))

def calc_variance(performance_full_time, sample_size = Config().DEFAUT_VARIANCE_SAMPLE_SIZE):
    """ Calculate the variance* of the full time period"""
    logging.debug("model, performance_key_values: calc_variance")

    # Look att mean values over <sample_size> values # TODO check that this is the right approach
    total_dif = 0
    elements_to_sum = (len(performance_full_time) - sample_size)
    for i in range(0, elements_to_sum, sample_size):

        sub_total = 0
        mean_line = calc_least_square_fit(performance_full_time[i:sample_size+i])
        
        for j in range(sample_size):
            sub_total += ((performance_full_time[i + j] - mean_line[j])/mean_line[j])**2
            

        total_dif += sub_total

    if elements_to_sum > 0:
        variance = round(total_dif/elements_to_sum,10)
    else:
        variance = 1000 # set suitable large value
        logging.error("To few values to calculate variance from")
    return variance


def calc_least_square_fit(value_data):
    """calculate a least square linear fit to data"""

    x = np.array([i+1 for i in range(len(value_data))])
    value_data_array = np.array(value_data)

    x_two_dimentional = np.vstack([x, np.ones(len(x))]).T  # Needs to be two dimensional, dont know why

    slope, rise = np.linalg.lstsq(x_two_dimentional, value_data_array, rcond=None)[0]  # Linear regression

    ret_list =[]
    for itteration_index in range(len(x)):
        ret_list.append(round(rise + (itteration_index + 1) * slope, 10))

    return ret_list
