#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.



from src.model.graph.strategies import do_not_invest
from src.model.graph.strategies import do_always_invest
from src.model.graph.strategies import hold_strategy
from src.model.graph.strategies import can_rebalance
from src.model.graph.strategies import rebalence

import src.model.common.constants_model as constants_model
import src.constants as constants

import pytest

from tests.model.helpers.Model_Builder import Model_Builder
from tests.model.helpers.Market_Builder import Market_Builder
from tests.model.helpers.Portfolio_Item_Builder import Portfolio_Item_Builder

# TODO not testing inflation at the moment due to not added in program
def test_do_not_invest(): 

    end_pos = 3
    excpected_result = [1,1,1]

    result = do_not_invest(end_pos)



    assert result == excpected_result



def test_do_always_invest_strategy_0_no_leverage():
    model = Model_Builder() \
            .portfolio_strategy(constants.PORTFOLIO_STRATEGIES[0]) \
            .instruments_selected([['A',1]]) \
            .build()

    portfolio_item = Portfolio_Item_Builder().build()
    portfolio_items = [portfolio_item]

    number_of_funds = 1
    number_of_leveraged_instruments = 0
    end_pos = len(model.markets_selected['A'].values) -1


    portfolio_results_full_time = do_always_invest(
            end_pos,
            portfolio_items,
            model.loan,
            model.portfolio_strategy,
            number_of_funds,
            model.proportion_leverage,
            model,
            model.harvest_point / constants.CONVERT_PERCENT,
            model.refill_point / constants.CONVERT_PERCENT,
            model.rebalance_period_months,
            number_of_leveraged_instruments)
    
    assert portfolio_results_full_time == pytest.approx([1,1.9999925,2.999974])

def test_do_always_invest_strategy_0_leverage_no_founds():
    model = Model_Builder() \
            .portfolio_strategy(constants.PORTFOLIO_STRATEGIES[0]) \
            .instruments_selected([['A',3]]) \
            .build()

    portfolio_item = Portfolio_Item_Builder().leverage(3).build()
    portfolio_items = [portfolio_item]

    number_of_funds = 0
    number_of_leveraged_instruments = 1
    end_pos = len(model.markets_selected['A'].values) -1


    portfolio_results_full_time = do_always_invest(
            end_pos,
            portfolio_items,
            model.loan,
            model.portfolio_strategy,
            number_of_funds,
            model.proportion_leverage,
            model,
            model.harvest_point / constants.CONVERT_PERCENT,
            model.refill_point / constants.CONVERT_PERCENT,
            model.rebalance_period_months,
            number_of_leveraged_instruments)
    
    assert portfolio_results_full_time == pytest.approx([1, 3.99999, 9.9999350])

def test_do_always_invest_strategy_0_leverage_and_founds():  

    model = Model_Builder() \
            .portfolio_strategy(constants.PORTFOLIO_STRATEGIES[0]) \
            .instruments_selected([['A',1],['A',3]]) \
            .build()

    number_of_funds = 1
    number_of_leveraged_instruments = 1

    portfolio_item1 = Portfolio_Item_Builder().values([model.proportion_funds/number_of_funds]).leverage(1).build()
    portfolio_item2 = Portfolio_Item_Builder().values([model.proportion_leverage/number_of_leveraged_instruments]).leverage(3).build()
    portfolio_items = [portfolio_item1, portfolio_item2]

    end_pos = len(model.markets_selected['A'].values) -1

    portfolio_results_full_time = do_always_invest(
            end_pos,
            portfolio_items,
            model.loan,
            model.portfolio_strategy,
            number_of_funds,
            model.proportion_leverage,
            model,
            model.harvest_point / constants.CONVERT_PERCENT,
            model.refill_point / constants.CONVERT_PERCENT,
            model.rebalance_period_months,
            number_of_leveraged_instruments)
    assert portfolio_results_full_time == pytest.approx([1, 2.19999233333, 3.699970166])

def test_do_always_invest_strategy_1_no_leverage():
    
    model = Model_Builder() \
            .portfolio_strategy(constants.PORTFOLIO_STRATEGIES[1]) \
            .instruments_selected([['A',1]]) \
            .build()

    portfolio_item = Portfolio_Item_Builder().build()
    portfolio_items = [portfolio_item]

    number_of_funds = 1
    number_of_leveraged_instruments = 0
    end_pos = len(model.markets_selected['A'].values) -1


    portfolio_results_full_time = do_always_invest(
            end_pos,
            portfolio_items,
            model.loan,
            model.portfolio_strategy,
            number_of_funds,
            model.proportion_leverage,
            model,
            model.harvest_point / constants.CONVERT_PERCENT,
            model.refill_point / constants.CONVERT_PERCENT,
            model.rebalance_period_months,
            number_of_leveraged_instruments)
    
    assert portfolio_results_full_time == pytest.approx([1,1.9999925,2.999974])

def test_do_always_invest_strategy_1_leverage_no_founds():
    model = Model_Builder() \
            .portfolio_strategy(constants.PORTFOLIO_STRATEGIES[1]) \
            .instruments_selected([['A',3]]) \
            .build()

    portfolio_item = Portfolio_Item_Builder().leverage(3).build()
    portfolio_items = [portfolio_item]

    number_of_funds = 0
    number_of_leveraged_instruments = 1
    end_pos = len(model.markets_selected['A'].values) -1


    portfolio_results_full_time = do_always_invest(
            end_pos,
            portfolio_items,
            model.loan,
            model.portfolio_strategy,
            number_of_funds,
            model.proportion_leverage,
            model,
            model.harvest_point / constants.CONVERT_PERCENT,
            model.refill_point / constants.CONVERT_PERCENT,
            model.rebalance_period_months,
            number_of_leveraged_instruments)
    
    assert portfolio_results_full_time == pytest.approx([1, 3.99999, 9.9999350])

def test_do_always_invest_strategy_1_leverage_and_founds():

    model = Model_Builder() \
            .portfolio_strategy(constants.PORTFOLIO_STRATEGIES[1]) \
            .instruments_selected([['A',1],['A',3]]) \
            .build()

    number_of_funds = 1
    number_of_leveraged_instruments = 1

    portfolio_item1 = Portfolio_Item_Builder().values([model.proportion_funds/number_of_funds]).leverage(1).build()
    portfolio_item2 = Portfolio_Item_Builder().values([model.proportion_leverage/number_of_leveraged_instruments]).reference_value(model.proportion_leverage/number_of_leveraged_instruments).leverage(3).build()
    portfolio_items = [portfolio_item1, portfolio_item2]

    end_pos = len(model.markets_selected['A'].values) -1

    portfolio_results_full_time = do_always_invest(
            end_pos,
            portfolio_items,
            model.loan,
            model.portfolio_strategy,
            number_of_funds,
            model.proportion_leverage,
            model,
            model.harvest_point / constants.CONVERT_PERCENT,
            model.refill_point / constants.CONVERT_PERCENT,
            model.rebalance_period_months,
            number_of_leveraged_instruments)
    
    
    assert portfolio_results_full_time == pytest.approx([1, 2.19999233333, 3.399971944])

def test_do_always_invest_strategy_2_no_leverage():
    
    model = Model_Builder() \
            .portfolio_strategy(constants.PORTFOLIO_STRATEGIES[2]) \
            .instruments_selected([['A',1]]) \
            .build()

    portfolio_item = Portfolio_Item_Builder().build()
    portfolio_items = [portfolio_item]

    number_of_funds = 1
    number_of_leveraged_instruments = 0
    end_pos = len(model.markets_selected['A'].values) -1


    portfolio_results_full_time = do_always_invest(
            end_pos,
            portfolio_items,
            model.loan,
            model.portfolio_strategy,
            number_of_funds,
            model.proportion_leverage,
            model,
            model.harvest_point / constants.CONVERT_PERCENT,
            model.refill_point / constants.CONVERT_PERCENT,
            model.rebalance_period_months,
            number_of_leveraged_instruments)
    
    assert portfolio_results_full_time == pytest.approx([1,1.9999925,2.999974])

def test_do_always_invest_strategy_2_leverage_no_founds():

    model = Model_Builder() \
            .portfolio_strategy(constants.PORTFOLIO_STRATEGIES[2]) \
            .instruments_selected([['A',3]]) \
            .build()

    portfolio_item = Portfolio_Item_Builder().leverage(3).build()
    portfolio_items = [portfolio_item]

    number_of_funds = 0
    number_of_leveraged_instruments = 1
    end_pos = len(model.markets_selected['A'].values) -1


    portfolio_results_full_time = do_always_invest(
            end_pos,
            portfolio_items,
            model.loan,
            model.portfolio_strategy,
            number_of_funds,
            model.proportion_leverage,
            model,
            model.harvest_point / constants.CONVERT_PERCENT,
            model.refill_point / constants.CONVERT_PERCENT,
            model.rebalance_period_months,
            number_of_leveraged_instruments)    

    assert portfolio_results_full_time == pytest.approx([1, 3.99999, 9.9999350])

def test_do_always_invest_strategy_2_leverage_and_founds():
    #TODO: currently not testing that rebalance is triggerd as should, only that not when shudnt (in some cases)
    model = Model_Builder() \
            .portfolio_strategy(constants.PORTFOLIO_STRATEGIES[2]) \
            .instruments_selected([['A',1],['A',3]]) \
            .build()
    
    model.rebalance_period_months = 1

    number_of_funds = 1
    number_of_leveraged_instruments = 1

    portfolio_item1 = Portfolio_Item_Builder().values([model.proportion_funds/number_of_funds]).leverage(1).build()
    portfolio_item2 = Portfolio_Item_Builder().values([model.proportion_leverage/number_of_leveraged_instruments]).reference_value(model.proportion_leverage/number_of_leveraged_instruments).leverage(3).build()
    portfolio_items = [portfolio_item1, portfolio_item2]

    end_pos = len(portfolio_item1.get_daily_change())

    portfolio_results_full_time = do_always_invest(
            end_pos,
            portfolio_items,
            model.loan,
            model.portfolio_strategy,
            number_of_funds,
            model.proportion_leverage,
            model,
            model.harvest_point / constants.CONVERT_PERCENT,
            model.refill_point / constants.CONVERT_PERCENT,
            model.rebalance_period_months,
            number_of_leveraged_instruments)
    
    assert portfolio_results_full_time == pytest.approx([1, 2.19999233333, 3.699970166])

def test_do_always_invest_strategy_2_leverage_and_founds2():
    model = Model_Builder() \
            .portfolio_strategy(constants.PORTFOLIO_STRATEGIES[2]) \
            .instruments_selected([['A',1],['A',3]]) \
            .build()

    number_of_funds = 1
    number_of_leveraged_instruments = 1
    daily_change = [0.001 for i in range(1,1000)]
    model.rebalance_period_months = 1

    portfolio_item1 = Portfolio_Item_Builder() \
            .values([model.proportion_funds/number_of_funds]) \
            .leverage(1) \
            .daily_change(daily_change) \
            .build()
    portfolio_item2 = Portfolio_Item_Builder() \
            .values([model.proportion_leverage/number_of_leveraged_instruments]) \
            .reference_value(model.proportion_leverage/number_of_leveraged_instruments) \
            .daily_change(daily_change) \
            .leverage(3) \
            .build()
    portfolio_items = [portfolio_item1, portfolio_item2]

    end_pos = len(daily_change)

    portfolio_results_full_time = do_always_invest(
            end_pos,
            portfolio_items,
            model.loan,
            model.portfolio_strategy,
            number_of_funds,
            model.proportion_leverage,
            model,
            model.harvest_point / constants.CONVERT_PERCENT,
            model.refill_point / constants.CONVERT_PERCENT,
            model.rebalance_period_months,
            number_of_leveraged_instruments)
    
    assert portfolio_results_full_time[-1] == pytest.approx(3.2839186671)

def test_do_always_invest_strategy_2_leverage_and_founds3():
    model = Model_Builder() \
            .portfolio_strategy(constants.PORTFOLIO_STRATEGIES[2]) \
            .instruments_selected([['A',1],['A',3]]) \
            .build()

    number_of_funds = 1
    number_of_leveraged_instruments = 1
    daily_change = [0.001 for i in range(1,1000)]
    model.rebalance_period_months = 3

    portfolio_item1 = Portfolio_Item_Builder() \
            .values([model.proportion_funds/number_of_funds]) \
            .leverage(1) \
            .daily_change(daily_change) \
            .build()
    portfolio_item2 = Portfolio_Item_Builder() \
            .values([model.proportion_leverage/number_of_leveraged_instruments]) \
            .reference_value(model.proportion_leverage/number_of_leveraged_instruments) \
            .daily_change(daily_change) \
            .leverage(3) \
            .build()
    portfolio_items = [portfolio_item1, portfolio_item2]

    end_pos = len(daily_change)

    portfolio_results_full_time = do_always_invest(
            end_pos,
            portfolio_items,
            model.loan,
            model.portfolio_strategy,
            number_of_funds,
            model.proportion_leverage,
            model,
            model.harvest_point / constants.CONVERT_PERCENT,
            model.refill_point / constants.CONVERT_PERCENT,
            model.rebalance_period_months,
            number_of_leveraged_instruments)
    
    bull_before_rebalance = portfolio_item2.values[68]
    bull_after_rebalance = portfolio_item2.values[72] 
    assert bull_before_rebalance > bull_after_rebalance

    assert portfolio_results_full_time[-1] == pytest.approx(3.278708851455)
   

# TODO (currently not prioretized)
#def do_sometimes_invest():


def test_hold_strategy():
    
    assert hold_strategy() == False #To be updated when inflation is implemented


def test_can_rebalance():
    
    inspected_instrument = Portfolio_Item_Builder().leverage(1).build()
    number_of_funds = 1
    all_instruments = Portfolio_Item_Builder().build()

    rebalance_possible = can_rebalance(inspected_instrument, number_of_funds, all_instruments)
    
    assert rebalance_possible == False 


    inspected_instrument = Portfolio_Item_Builder().leverage(2).build()
    number_of_funds = 0
    all_instruments = Portfolio_Item_Builder().build()

    rebalance_possible = can_rebalance(inspected_instrument, number_of_funds, all_instruments)
    
    assert rebalance_possible == False 


    inspected_instrument = Portfolio_Item_Builder().leverage(2).current_value(0).reference_value(1).build()
    fund_instrument = Portfolio_Item_Builder().leverage(1).current_value(0.5).build()
    number_of_funds = 1
    all_instruments = [inspected_instrument, fund_instrument]

    rebalance_possible = can_rebalance(inspected_instrument, number_of_funds, all_instruments)
    
    assert rebalance_possible == False 


    inspected_instrument = Portfolio_Item_Builder().leverage(2).current_value(2).reference_value(1).build()
    fund_instrument = Portfolio_Item_Builder().leverage(1).current_value(0).build()
    number_of_funds = 1
    all_instruments = [inspected_instrument, fund_instrument]

    rebalance_possible = can_rebalance(inspected_instrument, number_of_funds, all_instruments)
    
    assert rebalance_possible == True 


    inspected_instrument = Portfolio_Item_Builder().leverage(2).current_value(1).reference_value(3).build()
    fund_instrument1 = Portfolio_Item_Builder().leverage(1).current_value(1.5).build()
    fund_instrument2 = Portfolio_Item_Builder().leverage(1).current_value(1.5).build()
    number_of_funds = 2
    all_instruments = [inspected_instrument, fund_instrument1, fund_instrument2]

    rebalance_possible = can_rebalance(inspected_instrument, number_of_funds, all_instruments)
    
    assert rebalance_possible == True


def test_rebalance():
    
    inspected_instrument = Portfolio_Item_Builder().leverage(2).current_value(2).reference_value(1).build()
    fund_instrument = Portfolio_Item_Builder().leverage(1).current_value(0).build()
    number_of_funds = 1
    all_instruments = [inspected_instrument, fund_instrument]

    rebalence(inspected_instrument, all_instruments, number_of_funds)

    assert inspected_instrument.get_current_value() == 1
    assert fund_instrument.get_current_value() == 1


    inspected_instrument = Portfolio_Item_Builder().leverage(2).current_value(1).reference_value(3).build()
    fund_instrument1 = Portfolio_Item_Builder().leverage(1).current_value(1.5).build()
    fund_instrument2 = Portfolio_Item_Builder().leverage(1).current_value(2).build()
    number_of_funds = 2
    all_instruments = [inspected_instrument, fund_instrument1, fund_instrument2]

    rebalence(inspected_instrument, all_instruments, number_of_funds)

    assert inspected_instrument.get_current_value() == 3
    assert fund_instrument1.get_current_value() == 0.5
    assert fund_instrument2.get_current_value() == 1
