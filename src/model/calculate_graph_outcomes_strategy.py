
from src.model.determine_longest_common_timespan   import determine_longest_common_timespan
from src.model.portfolio_item_class import Portfolio_Item
import src.model.constants as constants
import logging


def calculate_graph_outcomes(model):
    logging.debug("Model: calculate_graph_outcomes")
    markets_selected        = model.get_markets_selected()
    instruments_selected    = model.get_instruments_selected()
    proportion_funds        = model.get_proportion_funds()
    proportion_leverage     = model.get_proportion_leverage()
    strategy                = model.get_portfolio_strategy()
    loan                    = model.get_loan()
    harvest_point           = model.get_harvest_point() / 100  # dont keep percentage
    refill_point            = model.get_refill_point() / 100  # dont keep percentage
    rebalance_period_months = model.get_rebalance_period_months()


    # Check if empty
    if instruments_selected == []:
        logging.debug("NOTIFY: Model: calculate_graph_outcomes: instruments_selected is empty")
        model.set_portfolio_results_full_time([])
        return

    if markets_selected  == []:
        logging.debug("NOTIFY: Model: calculate_graph_outcomes: no loaded data files")
        model.set_portfolio_results_full_time([])
        return

    # Get common start and end time
    [start_time, end_time] = determine_longest_common_timespan(instruments_selected, markets_selected)

    ### Calculate the outcome ###

    # get days to calculate
    a_instrument = instruments_selected[0]
    market = markets_selected[a_instrument[0]]
    end_pos = market.get_time_span().index(end_time)

    # prepare right proportions
    number_of_funds = 0
    number_of_leveraged_instruments = 0
    for instrument in instruments_selected:
        if instrument[1] == 1:  # Leverage == 1
            number_of_funds += 1
        else:
            number_of_leveraged_instruments += 1

    # Create portfolio
    portfolio_items = []
    for instrument in instruments_selected:
        name = instrument[0]
        leverage = instrument[1]

        # create portfolio item
        portfolio_item = Portfolio_Item(name, leverage)

        ### set extra values ###
        if leverage == 1:
            if number_of_leveraged_instruments > 0:
                portfolio_item.set_current_value((1+loan) * proportion_funds/number_of_funds)
            else:
                portfolio_item.set_current_value((1+loan)/number_of_funds)
        else:
            if number_of_funds > 0:
                portfolio_item.set_current_value((1+loan) * proportion_leverage/number_of_leveraged_instruments)
            else:
                portfolio_item.set_current_value((1+loan)/number_of_leveraged_instruments)

        portfolio_item.set_reference_value(portfolio_item.get_current_value())
        portfolio_item.set_country(markets_selected[name].get_country())
        portfolio_item.set_daily_change(markets_selected[name].get_daily_change())
        portfolio_item.set_values([portfolio_item.get_current_value()-loan])

        portfolio_items.append(portfolio_item)

    for day in range(0, end_pos):
        for item in portfolio_items:

            # update value with daily change
            new_value = item.get_current_value() * (1 + item.get_daily_change()[day] * item.get_leverage())
            item.set_current_value(new_value)

            item.set_values(item.get_values() + [new_value-loan])

            # Apply rule
            applied_change = False
            if strategy == constants.PORTFOLIO_STRATEGIES[0]:  # Do nothing
                applied_change = hold_strategy()
            elif strategy == constants.PORTFOLIO_STRATEGIES[1]:  # Harvest/Refill
                applied_change = harvest_refill(item, portfolio_items, number_of_funds, harvest_point, refill_point)
            elif strategy == constants.PORTFOLIO_STRATEGIES[2]:  # Rebalance on time cycle
                applied_change = rebalance_time_cycle(item, portfolio_items, number_of_funds, day, rebalance_period_months)
            else:
                raise Exception("Strategy not implemeted for graph: ", strategy)

            # Update reference values
            if applied_change:
                total_value = sum([i.get_current_value() for i in portfolio_items])
                for i in portfolio_items:
                    if i.get_leverage() > 1:
                        i.set_reference_value(total_value * proportion_leverage / number_of_leveraged_instruments)

    # sum total results
    total_results = []
    for item in portfolio_items:
        if total_results == []:
            total_results = item.get_values()
        else:
            total_results = [start + adding for start, adding in zip(total_results, item.get_values())]

    portfolio_results_full_time = total_results

    model.set_portfolio_results_full_time(portfolio_results_full_time)


def hold_strategy():
    # Do nothing to the instruments
    return False


def harvest_refill(inspected_instrument, all_instruments, number_of_funds, harvest_point, refill_point):

    if not need_rebalance(inspected_instrument, number_of_funds, all_instruments):
        return False

    current_value = inspected_instrument.get_current_value()
    reference_value = inspected_instrument.get_reference_value()

    if current_value > harvest_point * reference_value or current_value < refill_point * reference_value:

       rebalence(current_value, reference_value, inspected_instrument, all_instruments, number_of_funds)

    return True

def rebalance_time_cycle(inspected_instrument, all_instruments, number_of_funds, day, rebalance_period_months):

    if not need_rebalance(inspected_instrument, number_of_funds, all_instruments):
        return False

    current_value = inspected_instrument.get_current_value()
    reference_value = inspected_instrument.get_reference_value()

    rebalance_period_days = rebalance_period_months*constants.MARKET_DAYS_IN_YEAR/constants.MONTHS_IN_YEAR

    if day % rebalance_period_days == 0:
       rebalence(current_value, reference_value, inspected_instrument, all_instruments, number_of_funds)

    return True

def need_rebalance(inspected_instrument, number_of_funds, all_instruments):
    # No fund can trigger this rule
    if inspected_instrument.get_leverage() == 1:
        return False

    # Need funds to do strategy
    if number_of_funds == 0:
        return False

    # Is there money for rebalancing
    current_value = inspected_instrument.get_current_value()
    reference_value = inspected_instrument.get_reference_value()

    tot_for_rebalancing = 0
    for instrument in all_instruments:
        if instrument.get_leverage() == 1:
            tot_for_rebalancing += instrument.get_current_value()

    if tot_for_rebalancing <= (reference_value - current_value):
        return False

    return True

def rebalence(current_value, reference_value, inspected_instrument, all_instruments, number_of_funds):

    change_in_value = current_value - reference_value
    inspected_instrument.set_current_value(reference_value)

    for instrument in all_instruments:
        if instrument.get_leverage() == 1:
            instrument.set_current_value(instrument.get_current_value()+(change_in_value/number_of_funds))