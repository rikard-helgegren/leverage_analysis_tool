#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import src.model.common.constants_model as constants_model
import src.constants as constants
import logging
from src.model.common.variance_and_volatility import calc_volatility
import src.model.graph.utils as utils 


def do_not_invest(end_pos):
    """
        The strategy of not investing
    """

    logging.debug("Graph Strategies: do_not_invest")
    #TODO inflation decline not implemented, need data
    total_results = []
    for day in range(0, end_pos):
        total_results.append(1)
    return total_results

def do_always_invest(end_pos, portfolio_items, loan, strategy, number_of_funds, proportion_leverage, model, harvest_point, refill_point, rebalance_period_months, number_of_leveraged_instruments):
    """
        All strageties that choose to always invest
    """

    logging.debug("Graph Strategies: do_always_invest")
    for day in range(0, end_pos):
        for item in portfolio_items:

            # update value with daily change
            use_fees = model.get_include_fees_status()
            new_value = utils.update_value_with_daily_change(item, day, use_fees)
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

    return portfolio_results_full_time

def do_sometimes_invest(end_pos, portfolio_items, loan, strategy, number_of_funds, proportion_leverage, model, harvest_point, refill_point, rebalance_period_months, number_of_leveraged_instruments):
    """
        All strageties that choose to somtimes just wait for better oppertuity
    """

    logging.debug("Graph Strategies: do_sometimes_invest")
    for day in range(model.get_volatility_strategie_sample_size(), end_pos):  # start with previous days to calc variance on
        for item in portfolio_items:
            if item.get_leverage() > 1:

                # get recent volatility
                total_value_list = utils.convert_change_to_total_value(item.get_daily_change()[day-model.get_volatility_strategie_sample_size():day])
                volatility = calc_volatility(total_value_list, model.get_variance_calc_sample_size())

                # if vola. too high jump to next day
                if (volatility > model.get_volatility_strategie_level()):
                    item.set_values(item.get_values() + [item.get_current_value()-loan/len(portfolio_items)])
                    item.set_has_done_action(False)
                    continue
            
            # make func cal to strategy and somtimes rebalance
            low_variance_strategy(item, loan, portfolio_items, day, number_of_funds, proportion_leverage, rebalance_period_months, number_of_leveraged_instruments, model)

    portfolio_results_full_time = utils.sum_porfolio_results_full_time(portfolio_items)

    return portfolio_results_full_time


def hold_strategy():
    """
        The strategy of not investing.
    """

    logging.debug("Graph Strategies: hold_strategy")
    return False

def harvest_refill(inspected_instrument, all_instruments, number_of_funds, harvest_point, refill_point):
    """
        Do a harvest or refill (rebalance) if the leveraged product have increased or 
        decresed enough to trigger the rule
    """

    logging.debug("Graph Strategies: harvest_refill")
    if not can_rebalance(inspected_instrument, number_of_funds, all_instruments):
        return False

    current_value = inspected_instrument.get_current_value()
    reference_value = inspected_instrument.get_reference_value()

    if current_value > harvest_point * reference_value or current_value < refill_point * reference_value:

       rebalence(current_value, reference_value, inspected_instrument, all_instruments, number_of_funds)

    return True

def rebalance_time_cycle(inspected_instrument, all_instruments, number_of_funds, day, rebalance_period_months):
    """
        Do the rebalance, if possible, baced on time cycle
    """

    logging.debug("Graph Strategies: rebalance_time_cycle")
    if not can_rebalance(inspected_instrument, number_of_funds, all_instruments):
        return False

    current_value = inspected_instrument.get_current_value()
    reference_value = inspected_instrument.get_reference_value()

    rebalance_period_days = rebalance_period_months*constants_model.MARKET_DAYS_IN_YEAR/constants_model.MONTHS_IN_YEAR

    if day % rebalance_period_days == 0:
       rebalence(current_value, reference_value, inspected_instrument, all_instruments, number_of_funds)

    return True

def can_rebalance(inspected_instrument, number_of_funds, all_instruments):
    """
        Check if a rebalance is possible
    """

    logging.debug("Graph Strategies: can_rebalance")
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
    """
        Rebalance the portfolio to what is set to be the prefered 
        balance between levreaged products and funds
    """

    logging.debug("Graph Strategies: rebalence")
    change_in_value = current_value - reference_value
    inspected_instrument.set_current_value(reference_value)

    if (change_in_value < 0):
        change_in_value = change_in_value*constants_model.SPREAD

    for instrument in all_instruments:
        if instrument.get_leverage() == 1:
            instrument.set_current_value(instrument.get_current_value()+(change_in_value/number_of_funds))


def low_variance_strategy(item, loan, portfolio_items, day, number_of_funds, proportion_leverage, rebalance_period_months, number_of_leveraged_instruments, model):
    """
        Strategy that only invests when the recent volatility has been low.
        When volatility is low it uses periodic rebalancing strategy.
    """

    logging.debug("Graph Strategies: low_variance_strategy")

    use_fees = model.get_include_fees_status()
    new_value = utils.update_value_with_daily_change(item, day, use_fees)

    if (not item.get_has_done_action()) and model.get_include_fees_status():
        item.set_has_done_action(True)
        new_value /= constants_model.SPREAD

    item.set_current_value(new_value)
    item.set_values(item.get_values() + [new_value-loan])

    # Apply rule
    applied_change = False
    applied_change = rebalance_time_cycle(item, portfolio_items, number_of_funds, day, rebalance_period_months)

    # Update reference values
    if applied_change:
        total_value = sum([i.get_current_value() for i in portfolio_items])
        for item in portfolio_items:
            if item.get_leverage() > 1:
                item.set_reference_value(total_value * proportion_leverage / number_of_leveraged_instruments)
