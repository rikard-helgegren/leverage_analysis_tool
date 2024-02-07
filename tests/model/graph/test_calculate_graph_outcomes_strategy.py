#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

"""
from tests.model.helpers.Model_Builder import Model_Builder
import pytest

from src.model.graph.calculate_graph import calculate_graph_outcomes


# TODO Make less specific asserts
def test_calculate_graph_outcomes():

    model = Model_Builder().instruments_selected([["A",1]]).build()
    calculate_graph_outcomes(model)
    assert model.get_portfolio_results_full_time() == \
            pytest.approx([1.0, 1.9999925, 2.999974])
    

    model = Model_Builder().instruments_selected([["A",2]]).build()
    calculate_graph_outcomes(model)
    assert model.get_portfolio_results_full_time() == \
            pytest.approx([1.0, 2.99999, 5.99995])



    model = Model_Builder().instruments_selected([["A",1], ["A",2]]).build()
    calculate_graph_outcomes(model)
    assert model.get_portfolio_results_full_time() == \
            pytest.approx([1.0, 2.099992, 3.299971])
    
    
"""