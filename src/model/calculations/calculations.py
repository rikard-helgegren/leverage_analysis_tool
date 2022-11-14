import numpy as np
import logging
import src.model.constants as constants


def calc_volatility(performance_full_time, sample_size = constants.DEFULT_VARIANCE_SAMPLE_SIZE):
    """Calculate volatility of time period"""
    return np.sqrt(calc_variance(performance_full_time, sample_size))

def calc_variance(performance_full_time, sample_size = constants.DEFULT_VARIANCE_SAMPLE_SIZE):
    """ Calculate the variance* of the full time period"""
    logging.debug("model, performance_key_values: calc_variance")

    # Look att mean values over <sample_size> values # TODO check that this is the right approach
    total_dif = 0
    elements_to_sum = (len(performance_full_time) - sample_size)
    for i in range(0, elements_to_sum, sample_size):

        sub_total = 0
        mean_line = calc_mean_line_fit(performance_full_time[i:sample_size+i])
        for j in range(sample_size):
            sub_total += ((performance_full_time[i+sample_size] - mean_line[j])/mean_line[j])**2  # NOTE: normalized variance

    total_dif += sub_total

    if elements_to_sum > 0:
        variance = total_dif/elements_to_sum
    else:
        logging.error("To few values to calculate variance from")
    return variance


def calc_mean_line_fit(value_data):
    """calculate a least square linear fit to data"""

    x = np.array([i+1 for i in range(len(value_data))])
    value_data_array = np.array(value_data)

    x_two_dimentional = np.vstack([x, np.ones(len(x))]).T  # Needs to be two dimensional, dont know why

    slope, rise = np.linalg.lstsq(x_two_dimentional, value_data_array, rcond=None)[0]  # Linear regression

    ret_list =[]
    for itteration_index in range(len(x)):
        ret_list.append(rise+(itteration_index+1)*slope)

    return ret_list
