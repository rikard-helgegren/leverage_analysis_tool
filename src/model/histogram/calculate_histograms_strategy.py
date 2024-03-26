#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

from src.model.common.is_data_empty import is_data_empty
from src.model.histogram.histogram_cpp_adapter import rebalance_hist_ctypes

import src.model.constants_model as constants_model
import src.constants as constants
import numpy as np
import logging


def calculate_histogram(model):
    logging.debug("Model: calculate_histogram")

    markets_selected     = model.get_markets_selected()
    instruments_selected = model.get_instruments_selected()

    if is_data_empty(instruments_selected, markets_selected):
        model.set_results_for_intervals([])
        return

    #Return after construction
    strategy = model.get_portfolio_strategy()
    if strategy == constants.PORTFOLIO_STRATEGIES[0]:  # Hold
        return_data = do_nothing_hist(model)
    elif (strategy == constants.PORTFOLIO_STRATEGIES[1]) or (strategy == constants.PORTFOLIO_STRATEGIES[2]) or (strategy == constants.PORTFOLIO_STRATEGIES[4]) :  # Harvest/Refill or # Rebalance on time cycle or variance
        return_data = rebalance_hist_ctypes(model)
    elif strategy == constants.PORTFOLIO_STRATEGIES[3]:  # Do nothing
        return_data = [1]  # TODO change when implementing inflation
    else:
        logging.WARN("Strategy not implemented for histogram: ", strategy)
        return_data = [1, 2, 2, 3]

    model.set_results_for_intervals(return_data)
    return


def do_nothing_hist(model):

    logging.debug("Model: calculate_histogram")
    markets_selected     = model.get_markets_selected()
    instruments_selected = model.get_instruments_selected()
    proportion_funds     = model.get_proportion_funds()
    proportion_leverage  = model.get_proportion_leverage()
    include_fee_status   = model.get_include_fees_status()
    loan                 = model.get_loan()

    if is_data_empty(instruments_selected, markets_selected):
        model.set_results_for_intervals([])
        return

    outcomes_of_normal_investments = []
    outcomes_of_leveraged_investments = []

    number_of_leveraged_selected = 0
    number_of_non_leveraged_selected = 0

    for instrument in instruments_selected:

        leverage = instrument[1]

        # Get data with instrument name
        market = markets_selected[instrument[0]]
        daily_change = market.get_daily_change()
        cutoff = 0
        values_to_check = model.years_histogram_interval*constants_model.MARKET_DAYS_IN_YEAR

        if leverage == 1:
            number_of_non_leveraged_selected += 1
            performance = improved_calc(daily_change, leverage, cutoff, values_to_check, include_fee_status, loan)
            outcomes_of_normal_investments.append(performance)
        elif leverage > 1:
            number_of_leveraged_selected += 1
            performance = improved_calc(daily_change, leverage, cutoff, values_to_check, include_fee_status, loan)
            outcomes_of_leveraged_investments.append(performance)
        else:
            logging.error(" Non valid leverage used")

    combined_normal = combine_normal_instruments(number_of_non_leveraged_selected, outcomes_of_normal_investments)

    combined_leveraged = combine_leveraged_instruments(number_of_leveraged_selected,
                                                       outcomes_of_leveraged_investments)  # Unified list of leveraged instruments

    # Combine normal and leveraged
    if number_of_leveraged_selected == 0:
        if np.ndarray == type(combined_normal):
            return combined_normal.tolist()
        else:
            return combined_normal
    elif number_of_non_leveraged_selected == 0:
        if np.ndarray == type(combined_leveraged):
            return combined_leveraged.tolist()
        else:
            return combined_leveraged
    else:
        combined_normal_proportionally = np.multiply(proportion_funds,
                                                    combined_normal)  # take in to account how much of total is invested in normal funds
        combined_leveraged_proportionally = np.multiply(proportion_leverage,
                                                       combined_leveraged)  # take in to account how much of total is invested in leveraged markets
        normal_and_leverage_combined = [normal + leverage for normal, leverage in
                                        zip(combined_normal_proportionally, combined_leveraged_proportionally)]
        return normal_and_leverage_combined

def combine_normal_instruments(number_of_non_leveraged_selected, outcomes_of_normal_investments):
    # Unified list of normal instruments
    unified_normal = []
    if number_of_non_leveraged_selected == 1:
        unified_normal = outcomes_of_normal_investments[0]

    elif number_of_non_leveraged_selected > 1:
        unified_normal = outcomes_of_normal_investments[0]

        for i in range(1, number_of_non_leveraged_selected):
            unified_normal = [a + b for a, b in zip(unified_normal, outcomes_of_normal_investments[i])]
        unified_normal = np.divide(unified_normal, number_of_non_leveraged_selected)

    return unified_normal

def combine_leveraged_instruments(number_of_leveraged_selected, outcomes_of_leveraged_investments):
    # Unified list of leveraged instruments
    unified_leveraged = []
    if number_of_leveraged_selected == 1:
        unified_leveraged = outcomes_of_leveraged_investments[0]

    elif number_of_leveraged_selected > 1:
        unified_leveraged = outcomes_of_leveraged_investments[0]

        for i in range(1, number_of_leveraged_selected):
            unified_leveraged = [a + b for a, b in zip(unified_leveraged, outcomes_of_leveraged_investments[i])]
        unified_leveraged = np.divide(unified_leveraged, number_of_leveraged_selected)
    return unified_leveraged

def percentage_change(values):
    """ Calculate the relative change between two dadys e.g. increasing 2% or decreasing 1%
    """
    changes = []
    for i in range(len(values) - 1):
        changes.append((values[i + 1] - values[i]) / values[i])
    return changes

def improved_calc(daily_change, leverage, cutoff, values_to_check, include_fee_status, loan):
    """ Uses the fact that lots of calculations in the naive version are repeated.
        This can be avoided if we know that nothing interesting will happen in the
        interval inspected.
    """

    changes = daily_change
    gains = []

    # calc once:
    value_thus_far = 1 + loan
    lowest_value = 1 + loan
    lowest_value_index = 0
    has_appended = False
    lone_plus_rent = (1+loan)**(values_to_check/constants_model.MARKET_DAYS_IN_YEAR) - 1 

    # Setup, a first run through
    for i, change in enumerate(changes[0:values_to_check]):
        value_thus_far = update_value_with_daily_change(value_thus_far, change, leverage, include_fee_status)

        # Check if new extreme
        if value_thus_far < lowest_value:
            lowest_value = value_thus_far
            lowest_value_index = i

        if value_thus_far < cutoff:
            gains.append(cutoff)
            has_appended = True
            break

    if not has_appended:
        gains.append(value_thus_far)

    # Loop all possible start days
    for prev_i in range(0, len(daily_change) - values_to_check):
        has_appended = False

        # move interval and check effects on lowest value and end value
        lowest_value /= (1 + changes[prev_i] * leverage)
        value_thus_far /= (1 + changes[prev_i] * leverage)
        value_thus_far *= (1 + changes[prev_i + values_to_check] * leverage)

        if value_thus_far < lowest_value:
            lowest_value = value_thus_far
            lowest_value_index = prev_i + values_to_check

        if lowest_value < cutoff:
            if lowest_value_index <= prev_i:
                # The lowest recorded value is in the past! Need to recalculate a new lowest value.
                lowest_value = value_thus_far
                lowest_value_index = i
                value_thus_far = 1

                for j, change in enumerate(changes[i:i + values_to_check]):
                    value_thus_far *= 1 + change * leverage

                    if value_thus_far < lowest_value:
                        lowest_value = value_thus_far
                        lowest_value_index = i + j

            if lowest_value < cutoff:
                gains.append(cutoff)
                has_appended = True

        if not has_appended:
            gains.append(value_thus_far)

    gains = [(gain_item * (1 + loan))- lone_plus_rent for gain_item in gains]
    return gains

def update_value_with_daily_change(current_value, change, leverage, fees_status):
    """
        Update instrument value with the daily change times its leverage 
    """  
    logging.debug("Graph utils: update_value_with_daily_change")
    
    oneDayChange = current_value * change * leverage
    
    currencyChange = 1  #TODO requires dat and implementation

    if (fees_status is True):
        dailyFee = current_value * getFeeLevel(leverage)
    else:
        dailyFee = 0

    return (current_value  + oneDayChange - dailyFee) * currencyChange 

def getFeeLevel(leverage):
    """
        Return the fee rate related to the different leverage levels
    """
    logging.debug("calculate_histogram_stategy: getFeeLevel")
    if (leverage == 1):
        return constants_model.FEE_BULL_1
    elif (leverage >= 2 or leverage <= 4):
        return constants_model.FEE_BULL_2_TO_4
    elif (leverage >= 5):
        return constants_model.FEE_BULL_5_AND_MORE
    else:
        return -1
