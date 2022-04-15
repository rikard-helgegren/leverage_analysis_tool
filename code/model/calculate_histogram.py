import numpy as np
def calculate_histogram(self):
    print("TRACE: Model: calculate_histogram")

    markets_selected     = self.get_markets_selected()
    instruments_selected = self.get_instruments_selected()
    proportion_funds     = self.get_proportion_funds()
    proportion_leverage  = self.get_proportion_leverage()

    # Check if empty
    if instruments_selected == []:
        print("NOTIFY: Model: calculate_histogram: instruments_selected is empty")
        self.set_results_for_intervalls([])
        return

    if markets_selected == []:
        print("NOTIFY: Model: calculate_histogram: no loaded data files")
        self.set_results_for_intervalls([])
        return

    # Duplicate code of  calc graph
    outcomes_of_normal_investments = []
    outcomes_of_leveraged_investments = []

    number_of_leveraged_selected = 0
    number_of_non_leveraged_selected = 0

    for instrument in instruments_selected:

        leverage = instrument[1]

        # Get data with instrument name
        market = markets_selected[instrument[0]]
        list_of_values = market.get_values()
        cutoff = 0
        values_to_check = self.years_investigating*300

        if leverage == 1:
            number_of_non_leveraged_selected += 1
            performance = improved_calc(list_of_values, leverage, cutoff, values_to_check)
            outcomes_of_normal_investments.append(performance)
        elif leverage > 1:
            number_of_leveraged_selected += 1
            performance = improved_calc(list_of_values, leverage, cutoff, values_to_check)
            outcomes_of_leveraged_investments.append(performance)
        else:
            print("ERROR: Non valid leverage used")

    combined_normal = combine_normal_instruments(number_of_non_leveraged_selected, outcomes_of_normal_investments)

    combined_leveraged = combine_leveraged_instruments(number_of_leveraged_selected,
                                                       outcomes_of_leveraged_investments)  # Unified list of leveraged instruments

    # Combine normal and leveraged
    if number_of_leveraged_selected == 0:
        return self.set_results_for_intervalls(combined_normal)
    elif number_of_non_leveraged_selected == 0:
        return self.set_results_for_intervalls(combined_leveraged)
    else:
        combined_normal_proprtionally = np.multiply(proportion_funds,
                                                    combined_normal)  # take in to account how much of total is invested in normal funds
        combined_leveraged_proprtionally = np.multiply(proportion_leverage,
                                                       combined_leveraged)  # take in to account how much of total is invested in leveraged markets
        normal_and_leverage_combined = [normal + leverage for normal, leverage in
                                        zip(combined_normal_proprtionally, combined_leveraged_proprtionally)]
        return self.set_results_for_intervalls(normal_and_leverage_combined)

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
    # End duplicate code of  calc graph


    #######################################################
    ###                  Algorithms                     ###
    #######################################################

def percentage_change(values):
    changes = []
    for i in range(len(values) - 1):
        changes.append((values[i + 1] - values[i]) / values[i])
    return changes

def naive_calc(list_of_values, leverage, cutoff, values_to_check):
    changes = percentage_change(list_of_values)
    gains = []
    has_appended = False
    for i in range(0, len(list_of_values) - values_to_check):
        value_thus_far = 1
        has_appended = False

        for change in changes[i:i + values_to_check]:
            value_thus_far *= 1 + change * leverage

            if value_thus_far < cutoff:
                gains.append(cutoff)
                has_appended = True
                break

        if not has_appended:
            gains.append(value_thus_far)

    return gains

def improved_calc(list_of_values, leverage, cutoff, values_to_check):
    """ Uses the fact that lots of calculations in the naive version are repeated.
        This can be avoided if we know that nothing interesting will happen in the
        interval inspected.
    """
    changes = percentage_change(list_of_values)
    gains = []
    has_appended = False

    # calc once:
    value_thus_far = 1
    lowest_value = 1
    lowest_value_index = 0
    has_appended = False

    for i, change in enumerate(changes[0:values_to_check]):
        value_thus_far *= 1 + change * leverage

        if value_thus_far < lowest_value:
            lowest_value = value_thus_far
            lowest_value_index = i

        if value_thus_far < cutoff:
            gains.append(cutoff)
            has_appended = True
            break

    if not has_appended:
        gains.append(value_thus_far)

    for prev_i in range(0, len(list_of_values) - values_to_check - 1):
        has_appended = False

        # move interval to check
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
