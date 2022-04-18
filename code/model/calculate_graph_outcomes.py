
import numpy as np

from code.model.determine_longest_common_timespan   import determine_longest_common_timespan

def calculate_graph_outcomes(self):
    print("TRACE: Model: calculate_graph_outcomes")
    markets_selected     = self.get_markets_selected()
    instruments_selected = self.get_instruments_selected()
    proportion_funds     = self.get_proportion_funds()
    proportion_leverage  = self.get_proportion_leverage()

    #Check if empty
    if instruments_selected == []:
        print("NOTIFY: Model: calculate_graph_outcomes: instruments_selected is empty")
        self.set_portfolio_results_full_time([])
        return

    if markets_selected  == []:
        print("NOTIFY: Model: calculate_graph_outcomes: no loaded data files")
        self.set_portfolio_results_full_time([])
        return

    #Get common start and end time
    [start_time, end_time] = determine_longest_common_timespan(instruments_selected, markets_selected)


    #Calculate the outcome
    portfolio_results_full_time = calculate_portfolio_results_full_time(start_time,
                                                                        end_time,
                                                                        instruments_selected,
                                                                        proportion_funds,
                                                                        proportion_leverage,
                                                                        markets_selected)

    self.set_portfolio_results_full_time(portfolio_results_full_time)


def calculate_portfolio_results_full_time(start_time,
                                          end_time,
                                          instruments_selected,
                                          proportion_funds,
                                          proportion_leverage,
                                          markets):

    combined_outcome = []
    outcomes_of_normal_investments = []
    outcomes_of_leveraged_investments = []

    number_of_leveraged_selected = 0
    number_of_non_leveraged_selected = 0



    for instrument in instruments_selected:

        leverage = instrument[1]

        #Get data with instrument name
        market = markets[instrument[0]]

        #Get index of start time for this instrument
        start_pos = market.get_time_span().index(start_time)
        end_pos   = market.get_time_span().index(end_time)


        relevant_daily_change = market.get_daily_change()[start_pos:end_pos]



        if leverage == 1:
            number_of_non_leveraged_selected += 1
            performance = simulate_normal_performance(relevant_daily_change)
            outcomes_of_normal_investments.append(performance)
        elif leverage > 1:
            number_of_leveraged_selected += 1
            performance = simulate_leverage_strategy(relevant_daily_change, leverage)
            outcomes_of_leveraged_investments.append(performance)
        else:
            print("ERROR: Non valid leverage used")



    combined_normal = combine_normal_instruments(number_of_non_leveraged_selected, outcomes_of_normal_investments)

    combined_leveraged = combine_leveraged_instruments(number_of_leveraged_selected, outcomes_of_leveraged_investments)#Unifed list of leveraged instruments

    # Combine normal and leveraged
    if number_of_leveraged_selected == 0:
        return combined_normal
    elif number_of_non_leveraged_selected == 0:
        return combined_leveraged
    else:
        combined_normal_proprtionally = np.multiply(proportion_funds, combined_normal) # take in to account how much of total is invested in normal funds
        combined_leveraged_proprtionally = np.multiply(proportion_leverage, combined_leveraged) # take in to account how much of total is invested in leveraged markets
        normal_and_leverage_combined = [normal + leverage for normal, leverage in zip(combined_normal_proprtionally, combined_leveraged_proprtionally)]
        return normal_and_leverage_combined

def combine_normal_instruments(number_of_non_leveraged_selected, outcomes_of_normal_investments):
    #Unifed list of normal instruments
    unified_normal = []
    if number_of_non_leveraged_selected == 1:
        unified_normal = outcomes_of_normal_investments[0]

    elif  number_of_non_leveraged_selected > 1:
        unified_normal = outcomes_of_normal_investments[0]

        for i in range(1, number_of_non_leveraged_selected):
            unified_normal = [a + b for a, b in zip(unified_normal, outcomes_of_normal_investments[i])]
        unified_normal = np.divide(unified_normal, number_of_non_leveraged_selected)

    return unified_normal

def combine_leveraged_instruments(number_of_leveraged_selected, outcomes_of_leveraged_investments):
    #Unifed list of leveraged instruments
    unified_leveraged = []
    if number_of_leveraged_selected == 1:
        unified_leveraged = outcomes_of_leveraged_investments[0]

    elif  number_of_leveraged_selected > 1:
        unified_leveraged = outcomes_of_leveraged_investments[0]

        for i in range(1, number_of_leveraged_selected):
            unified_leveraged = [a + b for a, b in zip(unified_leveraged, outcomes_of_leveraged_investments[i])]
        unified_leveraged = np.divide(unified_leveraged, number_of_leveraged_selected)
    return unified_leveraged

def simulate_normal_performance(relevant_daily_change):

    START_STOCK_VALUE_START = 1000
    stock_value = [START_STOCK_VALUE_START]

    for change in relevant_daily_change:
        new_value = stock_value[-1]*(1+change)
        stock_value.append(new_value)

    return stock_value


def simulate_leverage_strategy(relevant_daily_change, leverage):
    #TODO: No strategies implemented
    #TODO: No fees implemented

    START_STOCK_VALUE_START = 1000
    stock_value = [START_STOCK_VALUE_START]

    for change in relevant_daily_change:
        new_value = stock_value[-1]*(1+change*leverage)
        stock_value.append(new_value)

    return stock_value
