#!/usr/bin/env python3
#
# Copyright (C) 2024 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging

#TODO:Can probably be time improved (using +, sets, and union)
def make_union(time_interval_list):
        logging.debug("util: make_union")

        time_union = []

        for time_span in time_interval_list:
            for date in time_span:
                if date not in time_union:
                    time_union.append(date)

        time_union.sort()

        return time_union
