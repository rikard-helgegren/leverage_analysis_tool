import src.model.constants as constants
import numpy as np
from src.model.histogram.histogram_cpp_adapter import rebalance_hist_ctypes
import logging


def calculate_histogram(model):
    logging.debug("Model: calculate_histogram")

    markets_selected     = model.get_markets_selected()
    instruments_selected = model.get_instruments_selected()

    # Check if empty
    if instruments_selected == []:
        logging.debug("NOTIFY: Model: calculate_histogram: instruments_selected is empty")
        model.set_results_for_intervals([])
        return

    if markets_selected == []:
        logging.debug("NOTIFY: Model: calculate_histogram: no loaded data files")
        model.set_results_for_intervals([])
        return

    #Return after construction
    strategy = model.get_portfolio_strategy()
    if strategy == constants.PORTFOLIO_STRATEGIES[0]:  # Hold
        return_data = do_nothing_hist(model)
    elif (strategy == constants.PORTFOLIO_STRATEGIES[1]) or (strategy == constants.PORTFOLIO_STRATEGIES[2]):  # Harvest/Refill or # Rebalance on time cycle
        return_data = rebalance_hist_ctypes(model)
    elif strategy == constants.PORTFOLIO_STRATEGIES[3]:  # Do nothing
        return_data = [1]  # TODO change when implementing inflation
    else:
        return_data = [1, 2, 2, 3]

    return model.set_results_for_intervals(return_data)


def do_nothing_hist(model):

    logging.debug("Model: calculate_histogram")
    markets_selected     = model.get_markets_selected()
    instruments_selected = model.get_instruments_selected()
    proportion_funds     = model.get_proportion_funds()
    proportion_leverage  = model.get_proportion_leverage()

    # Check if empty
    if instruments_selected == []:
        logging.debug("NOTIFY: Model: calculate_histogram: instruments_selected is empty")
        model.set_results_for_intervals([])
        return

    if markets_selected == []:
        logging.debug("NOTIFY: Model: calculate_histogram: no loaded data files")
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
        values_to_check = model.years_histogram_interval*constants.MARKET_DAYS_IN_YEAR

        if leverage == 1:
            number_of_non_leveraged_selected += 1
            performance = improved_calc(daily_change, leverage, cutoff, values_to_check)
            outcomes_of_normal_investments.append(performance)
        elif leverage > 1:
            number_of_leveraged_selected += 1
            performance = improved_calc(daily_change, leverage, cutoff, values_to_check)
            outcomes_of_leveraged_investments.append(performance)
        else:
            logging.error(" Non valid leverage used")

    combined_normal = combine_normal_instruments(number_of_non_leveraged_selected, outcomes_of_normal_investments)

    combined_leveraged = combine_leveraged_instruments(number_of_leveraged_selected,
                                                       outcomes_of_leveraged_investments)  # Unified list of leveraged instruments

    # Combine normal and leveraged
    if number_of_leveraged_selected == 0:
        return combined_normal
    elif number_of_non_leveraged_selected == 0:
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
    changes = []
    for i in range(len(values) - 1):
        changes.append((values[i + 1] - values[i]) / values[i])
    return changes

def improved_calc(daily_change, leverage, cutoff, values_to_check):
    """Uses the fact that lots of calculations in the naive version are repeated.
        This can be avoided if we know that nothing interesting will happen in the
        interval inspected.
    """

    changes = daily_change
    gains = []

    # calc once:
    value_thus_far = 1
    lowest_value = 1
    lowest_value_index = 0
    has_appended = False


    # Setup, a first run through
    for i, change in enumerate(changes[0:values_to_check]):
        value_thus_far *= 1 + change * leverage


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

    return gains
