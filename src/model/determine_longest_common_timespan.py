#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging


def determine_longest_common_timespan(instruments_selected, market_dict):
    logging.debug("Model: determine_longest_common_timespan")

    min_time = []
    max_time = []

    for instrument in instruments_selected:
        min_time.append(market_dict[instrument[0]].get_first_day()) #Get all first days (select highest)
        max_time.append(market_dict[instrument[0]].get_last_day()) #Get all last days (select lowest)

    start_time = max(min_time)
    end_time   = min(max_time)

    return [start_time, end_time]
