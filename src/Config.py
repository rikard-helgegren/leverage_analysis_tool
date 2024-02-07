#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

from src.Json_reader import Json_reader

class Config():

    def __init__(self):
                
        json_data = Json_reader.read_config()

        self.DEFAUT_LOAN = json_data["DEFAUT_LOAN"]
        self.DEFAUT_YEARS_HISTOGRAM_INTERVAL = json_data["DEFAUT_YEARS_HISTOGRAM_INTERVAL"]
        self.DEFAUT_HARVEST_POINT = json_data["DEFAUT_HARVEST_POINT"]
        self.DEFAUT_REFILL_POINT = json_data["DEFAUT_REFILL_POINT"]
        self.DEFAUT_REBALANCE_PERIOD_MONTHS = json_data["DEFAUT_REBALANCE_PERIOD_MONTHS"]
        self.DEFAUT_UPDATE_HARVEST_REFILL = json_data["DEFAUT_UPDATE_HARVEST_REFILL"]
        self.DEFAUT_PROPORTION_FUNDS = json_data["DEFAUT_PROPORTION_FUNDS"]
        self.DEFAUT_PROPORTION_LEVERAGE = 1 - json_data["DEFAUT_PROPORTION_FUNDS"]
        self.DEFAUT_INCLUDE_FEES_STATUS = json_data["DEFAUT_INCLUDE_FEES_STATUS"]
        self.DEFAUT_REBALANCE_BETWEEN_INSTRUMENTS_STATUS = json_data["DEFAUT_REBALANCE_BETWEEN_INSTRUMENTS_STATUS"]
        self.DEFAUT_CORRECTION_OF_INFLATION_STATUS = json_data["DEFAUT_CORRECTION_OF_INFLATION_STATUS"]
        self.DEFAUT_CORRECTION_OF_CURRENCY_STATUS = json_data["DEFAUT_CORRECTION_OF_CURRENCY_STATUS"]
        self.DEFAUT_DELAY_OF_CORRECTION = json_data["DEFAUT_DELAY_OF_CORRECTION"]
        self.DEFAUT_VARIANCE_SAMPLE_SIZE = json_data["DEFAUT_VARIANCE_SAMPLE_SIZE"]
        self.DEFAUT_VOLATILITY_STRATEGIE_SAMPLE_SIZE = json_data["DEFAUT_VOLATILITY_STRATEGIE_SAMPLE_SIZE"]
        self.DEFAUT_VOLATILITY_STRATEGIE_LEVEL = json_data["DEFAUT_VOLATILITY_STRATEGIE_LEVEL"]
        self.HIGHEST_LEVERAGE_AVAILABLE = json_data["HIGHEST_LEVERAGE_AVAILABLE"]

        self.SORT_RANKING = [
            'DEBUG',
            'NASDAQ100',
            'SP500',
            'DIA',
            'OMXS30',
            'OSEAX',
            'OMXC',
            'OMXH',
            'DAX',
            'CAC'
        ]
