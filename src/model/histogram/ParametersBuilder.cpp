/**
 * Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
 *
 * This software is only allowed for private use. As a private user you are allowed to copy,
 * modify, use, and compile the software. You are NOT however allowed to publish, sell, or
 * distribute this software, either in source code form or as a compiled binary, for any purpose,
 * commercial or non-commercial, by any means.
 */

#include "Parameters.cpp"

#pragma once

class ParametersBuilder{
    private:
        Parameters parameters;

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
        int     daysInvesting;
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
        std::map<int, int>   indexToMarket;
    
    Parameters build(){
        return this->parameters;
    }

    ParametersBuilder setLoan (float loan){
        parameters.loan = loan;
        return *this;
    }
    ParametersBuilder setInstrumentLeverages (int* instrumentLeverages){
        parameters.instrumentLeverages = instrumentLeverages;
        return *this;
    }
    ParametersBuilder setNrOfInstruments (int nrOfInstruments){
        parameters.nrOfInstruments = nrOfInstruments;
        return *this;
    }
    ParametersBuilder setInstrumentNames (std::vector<std::string> instrumentNames){
        parameters.instrumentNames = instrumentNames;
        return *this;
    }
    ParametersBuilder setProportionFunds (float proportionFunds){
        parameters.proportionFunds = proportionFunds;
        return *this;
    }
    ParametersBuilder setProportionLeverage (float proportionLeverage){
        parameters.proportionLeverage = proportionLeverage;
        return *this;
    }
    ParametersBuilder setTotNrDays (int totNrDays){
        parameters.totNrDays = totNrDays;
        return *this;
    }
    ParametersBuilder setNrMarketsSelected (int nrMarketsSelected){
        parameters.nrMarketsSelected = nrMarketsSelected;
        return *this;
    }
    ParametersBuilder setMarketDailyChanges (float** marketDailyChanges){
        parameters.marketDailyChanges = marketDailyChanges;
        return *this;
    }
    ParametersBuilder setIndexNames (std::vector<std::string> indexNames){
        parameters.indexNames = indexNames;
        return *this;
    }
    ParametersBuilder setDaysInvesting (int daysInvesting){
        parameters.daysInvesting = daysInvesting;
        return *this;
    }
    ParametersBuilder setHarvestPoint (float harvestPoint){
        parameters.harvestPoint = harvestPoint;
        return *this;
    }
    ParametersBuilder setRefillPoint (float refillPoint){
        parameters.refillPoint = refillPoint;
        return *this;
    }
    ParametersBuilder setRebalance_period_months (int rebalance_period_months){
        parameters.rebalance_period_months = rebalance_period_months;
        return *this;
    }
    ParametersBuilder setStrategy (int strategy){
        parameters.strategy = strategy;
        return *this;
    }
    ParametersBuilder setVolatilityStrategieSampleSize (int volatilityStrategieSampleSize){
        parameters.volatilityStrategieSampleSize = volatilityStrategieSampleSize;
        return *this;
    }
    ParametersBuilder setVarianceCalcSampleSize (int varianceCalcSampleSize){
        parameters.varianceCalcSampleSize = varianceCalcSampleSize;
        return *this;
    }
    ParametersBuilder setVolatilityStrategieLevel (float volatilityStrategieLevel){
        parameters.volatilityStrategieLevel = volatilityStrategieLevel;
        return *this;
    }
    ParametersBuilder setNumberOfLeveragedInstruments(int numberOfLeveragedInstruments){
        parameters.numberOfLeveragedInstruments = numberOfLeveragedInstruments;
        return *this;
    }
    ParametersBuilder setNumberOfFunds(int numberOfFunds){
        parameters.numberOfFunds = numberOfFunds;
        return *this;
    }
    ParametersBuilder setIndexToMarket(std::map<int, int> indexToMarket){
        parameters.indexToMarket = indexToMarket;
        return *this;
    }
    ParametersBuilder setIncludeFeeStatus(bool includeFeeStatus){
        parameters.includeFeeStatus = includeFeeStatus;
        return *this;
    }
    ParametersBuilder setOutData (float* outData){
        parameters.outData = outData;
        return *this;
    }
    
};