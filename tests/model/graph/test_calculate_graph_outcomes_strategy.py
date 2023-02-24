#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.


from src.model.Market import Market
from src.model.Model import Model
from tests.model.Model_Builder import Model_Builder

from src.model.graph.calculate_graph_outcomes_strategy import calculate_graph_outcomes



def test_calculate_graph_outcomes():

    model = Model_Builder().instruments_selected([["A",1]]).build()

    calculate_graph_outcomes(model)

    assert model.get_portfolio_results_full_time() == [1.0, 1.9999925925925925, 2.999974074128944]
    
