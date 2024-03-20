#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.


"""
from src.model.graph.utils import create_portfolio
from src.model.graph.utils import get_last_index_of_days_from_instrument
from src.model.graph.utils import calculate_nbr_of_funds_and_leverages
from src.model.graph.utils import set_initial_portfolio_values
from src.model.graph.utils import sum_porfolio_results_full_time
from src.model.graph.utils import convert_change_to_total_value
from src.model.graph.utils import update_value_with_daily_change
from src.model.graph.utils import getFeeLevel

import src.model.common.constants_model as constants_model
from tests.model.helpers.Model_Builder import Model_Builder
from tests.model.helpers.Market_Builder import Market_Builder
from tests.model.helpers.Portfolio_Item_Builder import Portfolio_Item_Builder


def test_create_portfolio():

    model = Model_Builder().instruments_selected([["A",1]]).build()

    number_of_leveraged_instruments = 0
    number_of_funds = 1

    portfolio_items = create_portfolio(model.instruments_selected,
                      number_of_leveraged_instruments,
                      model.loan,
                      model.proportion_funds,
                      number_of_funds,
                      model.proportion_leverage,
                      model.markets_selected)
    
    excpectedPortfolio = Portfolio_Item_Builder().build()
    
    assert portfolio_items[0].is_equal_to(excpectedPortfolio)



    model = Model_Builder().instruments_selected([["A",1], ["A",2]]).build()

    number_of_leveraged_instruments = 1
    number_of_funds = 1

    portfolio_items = create_portfolio(model.instruments_selected,
                      number_of_leveraged_instruments,
                      model.loan,
                      model.proportion_funds,
                      number_of_funds,
                      model.proportion_leverage,
                      model.markets_selected)
    
    excpectedPortfolio_item1 = Portfolio_Item_Builder().values([0.9]).reference_value(0.9).current_value(0.9).build()
    excpectedPortfolio_item2 = Portfolio_Item_Builder().values([0.1]).reference_value(0.1).current_value(0.1).leverage(2).build()
    
    assert portfolio_items[0].is_equal_to(excpectedPortfolio_item1)
    assert portfolio_items[1].is_equal_to(excpectedPortfolio_item2)


    model = Model_Builder().instruments_selected([["A",1], ["B",1]]).build()

    number_of_leveraged_instruments = 0
    number_of_funds = 2

    portfolio_items = create_portfolio(model.instruments_selected,
                      number_of_leveraged_instruments,
                      model.loan,
                      model.proportion_funds,
                      number_of_funds,
                      model.proportion_leverage,
                      model.markets_selected)
    
    excpectedPortfolio_item1 = Portfolio_Item_Builder() \
            .values([0.5]) \
            .reference_value(0.5) \
            .current_value(0.5) \
            .build()
    excpectedPortfolio_item2 = Portfolio_Item_Builder() \
            .values([0.5]) \
            .reference_value(0.5) \
            .current_value(0.5) \
            .build()
    
    assert portfolio_items[0].is_equal_to(excpectedPortfolio_item1)
    assert portfolio_items[1].is_equal_to(excpectedPortfolio_item2)


def test_get_last_index_of_days_from_instrument():

    market = Market_Builder().build()
    markets_selected = {market.name: market}
    a_instrument = ['A',1]
    end_time = market.get_time_span()[-1]

    index = get_last_index_of_days_from_instrument(a_instrument, markets_selected, end_time)
    
    assert index == len(market.get_time_span())-1

def test_calculate_nbr_of_funds_and_leverages():

    instruments_selected = [['A',1]] 

    funds_and_leverages = calculate_nbr_of_funds_and_leverages(instruments_selected)

    assert funds_and_leverages[0] == 1
    assert funds_and_leverages[1] == 0

    instruments_selected = [['A',3]] 

    funds_and_leverages = calculate_nbr_of_funds_and_leverages(instruments_selected)

    assert funds_and_leverages[0] == 0
    assert funds_and_leverages[1] == 1


    instruments_selected = [['A',1], ['B',1], ['C',3], ['A',7], ['E',4]] 

    funds_and_leverages = calculate_nbr_of_funds_and_leverages(instruments_selected)

    assert funds_and_leverages[0] == 2
    assert funds_and_leverages[1] == 3

# Only setting the values for first item in 'instruments_selected'
def test_set_initial_portfolio_values():

    instruments_selected = [['A',1]]  # Not needed but for context. 
    portfolio_item = Portfolio_Item_Builder().build()
    number_of_leveraged_instruments = 0
    loan = 0
    proportion_funds = 1
    number_of_funds = 1
    proportion_leverage = 0
    name='A'
    markets_selected = {'A':Market_Builder().build()}


    set_initial_portfolio_values(  \
            portfolio_item.leverage, \
            number_of_leveraged_instruments, \
            loan, proportion_funds, \
            number_of_funds, portfolio_item, \
            proportion_leverage, \
            name, markets_selected)

    assert portfolio_item.current_value == 1
    assert portfolio_item.reference_value == 1
    assert portfolio_item.country == 'a'
    assert portfolio_item.daily_change == [1.0, 0.5]
    assert portfolio_item.values == [1]


    instruments_selected = [['A',1],['B',1]]  # Not needed but for context. 
    portfolio_item = Portfolio_Item_Builder().build()
    number_of_leveraged_instruments = 0
    loan = 0
    proportion_funds = 1
    number_of_funds = 2
    proportion_leverage = 0
    name='A'
    markets_selected = {'A':Market_Builder().build()}


    set_initial_portfolio_values( \
            portfolio_item.leverage, \
            number_of_leveraged_instruments, \
            loan, \
            proportion_funds, \
            number_of_funds, \
            portfolio_item, \
            proportion_leverage, \
            name, \
            markets_selected)

    assert portfolio_item.current_value == 0.5
    assert portfolio_item.reference_value == 0.5
    assert portfolio_item.country == 'a'
    assert portfolio_item.daily_change == [1.0, 0.5]
    assert portfolio_item.values == [0.5]




    instruments_selected = [['A',2]]  # Not needed but for context. 
    portfolio_item = Portfolio_Item_Builder().leverage(2).build()
    loan = 0
    proportion_funds = 0
    number_of_funds = 0
    proportion_leverage = 1
    number_of_leveraged_instruments = 1
    name='A'
    markets_selected = {'A':Market_Builder().build()}


    set_initial_portfolio_values( \
            portfolio_item.leverage, \
            number_of_leveraged_instruments, \
            loan, \
            proportion_funds, \
            number_of_funds, \
            portfolio_item, \
            proportion_leverage, \
            name, \
            markets_selected)

    assert portfolio_item.current_value == 1
    assert portfolio_item.reference_value == 1
    assert portfolio_item.country == 'a'
    assert portfolio_item.daily_change == [1.0, 0.5]
    assert portfolio_item.values == [1]



    instruments_selected = [['A',2],['B',5]]  # Not needed but for context. 
    portfolio_item = Portfolio_Item_Builder().leverage(2).build()
    loan = 0
    proportion_funds = 0
    number_of_funds = 0
    proportion_leverage = 1
    number_of_leveraged_instruments = 2
    name='A'
    markets_selected = {'A':Market_Builder().build()}


    set_initial_portfolio_values(
            portfolio_item.leverage, \
            number_of_leveraged_instruments, \
            loan, \
            proportion_funds, \
            number_of_funds, \
            portfolio_item, \
            proportion_leverage, \
            name, \
            markets_selected)

    assert portfolio_item.current_value == 0.5
    assert portfolio_item.reference_value == 0.5
    assert portfolio_item.country == 'a'
    assert portfolio_item.daily_change == [1.0, 0.5]
    assert portfolio_item.values == [0.5]



def test_sum_porfolio_results_full_time():

    portfolio_item1 = Portfolio_Item_Builder().values([1,2,3]).build()
    portfolio_items = [portfolio_item1]

    portfolio_results_full_time = sum_porfolio_results_full_time(portfolio_items)

    assert portfolio_results_full_time == [1,2,3]


    portfolio_item1 = Portfolio_Item_Builder().values([1, 2, 3]).build()
    portfolio_item2 = Portfolio_Item_Builder().values([1.1, 2.0, 3.1]).build()
    portfolio_items = [portfolio_item1, portfolio_item2]

    portfolio_results_full_time = sum_porfolio_results_full_time(portfolio_items)

    assert portfolio_results_full_time == [2.1,4.0,6.1]


def test_convert_change_to_total_value():

    change_day_list = [1,1,1,1]

    total_value = convert_change_to_total_value(change_day_list)

    assert total_value == [1,2,4,8,16]


def test_update_value_with_daily_change():

    item = Portfolio_Item_Builder().daily_change([1,1]).build()
    day = 1
    use_fees = False

    new_value = update_value_with_daily_change(item, day, use_fees)

    assert new_value == 2

    item = Portfolio_Item_Builder().daily_change([1,1]).build()
    day = 1
    use_fees = True

    new_value = update_value_with_daily_change(item, day, use_fees)

    assert round(new_value,10) == 1.9999925926

    item = Portfolio_Item_Builder().values([0.1]).daily_change([1,1]).build()
    day = 1
    use_fees = False

    new_value = update_value_with_daily_change(item, day, use_fees)

    assert new_value == 0.2

    item = Portfolio_Item_Builder().values([1]).daily_change([1,2,2,2,2,2,2]).build()
    use_fees = False

    item.set_current_value(update_value_with_daily_change(item, 0, use_fees))
    item.set_current_value(update_value_with_daily_change(item, 1, use_fees))
    new_value = update_value_with_daily_change(item, 2, use_fees)

    assert new_value == 18

def test_getFeeLevel():

    leverage = 1
    fee_level = getFeeLevel(leverage)
    assert fee_level == constants_model.FEE_BULL_1

    leverage = 2
    fee_level = getFeeLevel(leverage)
    assert fee_level == constants_model.FEE_BULL_2_TO_4

    leverage = 3
    fee_level = getFeeLevel(leverage)
    assert fee_level == constants_model.FEE_BULL_2_TO_4

    leverage = 4
    fee_level = getFeeLevel(leverage)
    assert fee_level == constants_model.FEE_BULL_2_TO_4

    leverage = 5
    fee_level = getFeeLevel(leverage)
    assert fee_level == constants_model.FEE_BULL_5_AND_MORE
"""
