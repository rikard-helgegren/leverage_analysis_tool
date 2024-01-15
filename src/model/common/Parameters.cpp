/**
 * Copyright (C) 2024 Rikard Helgegren <rikard.helgegren@gmail.com>
 *
 * This software is only allowed for private use. As a private user you are allowed to copy,
 * modify, use, and compile the software. You are NOT however allowed to publish, sell, or
 * distribute this software, either in source code form or as a compiled binary, for any purpose,
 * commercial or non-commercial, by any means.
 */

#pragma once

#include <vector>
#include <string>
#include <iostream>
#include <map>

#include "../graph/GraphParameters.cpp"
#include "../histogram/HistogramParameters.cpp"

class Parameters{
    public:
        float   loan;
        int*    instrumentLeverages;
        int     nrOfInstruments;
        std::vector<std::string>   instrumentNames;
        float   proportionFunds;
        float   proportionLeverage;
        int     totNrDays;
        int     nrMarketsSelected;
        float** marketDailyChanges;
        std::vector<std::string>    indexNames;
        float   harvestPoint;
        float   refillPoint;
        int     rebalance_period_months;
        int     strategy;
        int     volatilityStrategieSampleSize;
        int     varianceCalcSampleSize;
        float   volatilityStrategieLevel;
        float*  outData;
        int     numberOfLeveragedInstruments;
        int     numberOfFunds;
        bool    includeFeeStatus;
        std::map<int, int>        indexToMarket;

        HistogramParameters histogramParameters;
        GraphParameters     graphParameters;
};
