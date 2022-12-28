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


program_folder = os.path.dirname(os.path.realpath(sys.argv[0]))
#program_folder = os.getcwd())
data_files_path = program_folder + "/data/raw_data/all"
hist_harvest_refill_algo_file = program_folder + '/src/compiled_code/calculateHistogramOutput.so'

MARKET_DAYS_IN_YEAR = 270  # 270 is not true for all markets but close if the union is considered
MONTHS_IN_YEAR = 12

FEE_BULL_1 = 0.002/MARKET_DAYS_IN_YEAR  # 0.2% each year
FEE_BULL_2_TO_4 = 0.00001  # 0.01% each day
FEE_BULL_5_AND_MORE = 0.00002  # 0.02% each day
SPREAD = 1  #No spread at Avanza (1% spread would result in const beeing 1.01)

