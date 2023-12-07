#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

from src.model.common.determine_longest_common_timespan import determine_longest_common_timespan
from src.model.common.check_data_is_empty               import check_data_is_empty
from src.model.Buy_sell_singelton                       import Buy_sell_singelton
import src.model.common.constants_model as constants_model
import src.constants as constants
import src.model.graph.strategies as strategies
import src.model.graph.utils as utils
import logging


def calculate_graph_outcomes(model):  #TODO, graph should not be able to have negative values, china X5
    """
        The main function for calculating the values of the portfolio shown in the graph.
    """
    logging.debug("Model: calculate_graph_outcomes")

    # TODO: use parameter class instead to have cleaner code
    markets_selected        = model.get_markets_selected()
    instruments_selected    = model.get_instruments_selected()
    proportion_funds        = model.get_proportion_funds()
    proportion_leverage     = model.get_proportion_leverage()
    strategy                = model.get_portfolio_strategy()
    loan                    = model.get_loan()
    harvest_point           = model.get_harvest_point() / constants.CONVERT_PERCENT
    refill_point            = model.get_refill_point() / constants.CONVERT_PERCENT
    rebalance_period_months = model.get_rebalance_period_months()
    #buy_sell                = model.get_buys_sells()

    if check_data_is_empty(instruments_selected, markets_selected):
        model.set_portfolio_results_full_time([])
        return

    [start_time, end_time] = determine_longest_common_timespan(instruments_selected, markets_selected)

    end_pos = utils.get_last_index_of_days_from_instrument(instruments_selected[0], markets_selected, end_time)

    number_of_funds, number_of_leveraged_instruments = utils.calculate_nbr_of_funds_and_leverages(instruments_selected)

    portfolio_items = utils.create_portfolio(instruments_selected, number_of_leveraged_instruments, loan, proportion_funds, number_of_funds, proportion_leverage, markets_selected)
   
    Buy_sell_singelton().clear_log()

    if strategy == constants.PORTFOLIO_STRATEGIES[3]:  # Do not invest money
        portfolio_results_full_time = strategies.do_not_invest(end_pos)
    elif strategy == constants.PORTFOLIO_STRATEGIES[4]:  # Paus leverage when volatile
        portfolio_results_full_time = strategies.do_sometimes_invest(end_pos, portfolio_items, loan, strategy, number_of_funds, proportion_leverage, model, harvest_point, refill_point, rebalance_period_months, number_of_leveraged_instruments)
    else:
        portfolio_results_full_time = strategies.do_always_invest(end_pos, portfolio_items, loan, strategy, number_of_funds, proportion_leverage, model, harvest_point, refill_point, rebalance_period_months, number_of_leveraged_instruments)
    
    model.set_portfolio_results_full_time(portfolio_results_full_time)
