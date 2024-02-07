#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

""" Specific constants for model"""

import os
import sys
from enum import Enum


program_folder = os.path.dirname(os.path.realpath(sys.argv[0]))
#program_folder = os.getcwd())
data_files_path = program_folder + "/data/raw_data/all"
calculate_histogram_output_file = program_folder + '/src/compiled_code/calculateHistogramOutput.so'
calculate_graph_output_file = program_folder + '/src/compiled_code/calculateGraphOutput.so'

MARKET_DAYS_IN_YEAR = 270  # 270 is not true for all markets but close if the union is considered
MONTHS_IN_YEAR = 12

FEE_BULL_1 = 0.002/MARKET_DAYS_IN_YEAR   # 0.2% each year
FEE_BULL_2 = 0.0101/MARKET_DAYS_IN_YEAR  # 1.01% each year
FEE_BULL_3 = 0.0203/MARKET_DAYS_IN_YEAR  # 2.03% each year
FEE_BULL_4 = 0.0305/MARKET_DAYS_IN_YEAR  # 3.05% each year
FEE_BULL_5 = 0.0614/MARKET_DAYS_IN_YEAR  # 6.14% each year
FEE_BULL_6 = None  # no data
FEE_BULL_7 = None  # no data
FEE_BULL_8 = 0.2189/MARKET_DAYS_IN_YEAR  # 21.89% each year
FEE_BULL_9 = None  # no data
FEE_BULL_10 = 0.2865/MARKET_DAYS_IN_YEAR  # 28.65% each year
FEE_BULL_2_TO_4 = 0.00001  # 0.01% each day
FEE_BULL_5_AND_MORE = 0.00002  # 0.02% each day
SPREAD = 1  # No spread at Avanza (1% spread would result in const beeing 1.01)
SPREAD_BULL_1 = 1
SPREAD_BULL_2 = 1.002
SPREAD_BULL_3 = 1.003
SPREAD_BULL_4 = 1.004
SPREAD_BULL_5 = 1.0052
SPREAD_BULL_6 = None  # no data
SPREAD_BULL_7 = None  # no data
SPREAD_BULL_8 = 1.0112
SPREAD_BULL_9 = None  # no data
SPREAD_BULL_10 = 1.015

class Order(Enum):
    BUY = 1
    SELL = 2
