#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging


def check_data_is_empty(instruments_selected, markets_selected):
    logging.debug("Common utils: check_data_is_empty")
    
    if instruments_selected == []:
        logging.debug("NOTIFY: Model: instruments_selected is empty")
        return True

    if markets_selected  == []:
        logging.debug("NOTIFY: Model: no loaded data files")
        return True
        