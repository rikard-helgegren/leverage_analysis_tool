/**
 * Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
 *
 * This software is only allowed for private use. As a private user you are allowed to copy,
 * modify, use, and compile the software. You are NOT however allowed to publish, sell, or
 * distribute this software, either in source code form or as a compiled binary, for any purpose,
 * commercial or non-commercial, by any means.
 */

#include "Parameters.cpp"
#include "../../Logger.cpp"

#pragma once

class ParametersBuilder{
    private:
        Parameters parameters;

    public:

    Parameters build(){
        //static Logger logger;
        //logger.log("ParametersBuilder: build");
        return this->parameters;
    }

    ParametersBuilder setLoan (float loan){
        //static Logger logger;
        //logger.log("ParametersBuilder: loan");
        parameters.loan = loan;
        return *this;
    }
    ParametersBuilder setInstrumentLeverages (int* instrumentLeverages){
        //static Logger logger;
        //logger.log("ParametersBuilder: instrumentLeverages");
        parameters.instrumentLeverages = instrumentLeverages;
        return *this;
    }
    ParametersBuilder setNrOfInstruments (int nrOfInstruments){
        //static Logger logger;
        //logger.log("ParametersBuilder: nrOfInstruments");
        parameters.nrOfInstruments = nrOfInstruments;
        return *this;
    }
    ParametersBuilder setInstrumentNames (std::vector<std::string> instrumentNames){
        //static Logger logger;
        //logger.log("ParametersBuilder: instrumentNames");
        parameters.instrumentNames = instrumentNames;
        return *this;
    }
    ParametersBuilder setProportionFunds (float proportionFunds){
        //static Logger logger;
        //logger.log("ParametersBuilder: proportionFunds");
        parameters.proportionFunds = proportionFunds;
        return *this;
    }
    ParametersBuilder setProportionLeverage (float proportionLeverage){
        //static Logger logger;
        //logger.log("ParametersBuilder: proportionLeverage");
        parameters.proportionLeverage = proportionLeverage;
        return *this;
    }
    ParametersBuilder setTotNrDays (int totNrDays){
        //static Logger logger;
        //logger.log("ParametersBuilder: totNrDays");
        parameters.totNrDays = totNrDays;
        return *this;
    }
    ParametersBuilder setNrMarketsSelected (int nrMarketsSelected){
        //static Logger logger;
        //logger.log("ParametersBuilder: nrMarketsSelected");
        parameters.nrMarketsSelected = nrMarketsSelected;
        return *this;
    }
    ParametersBuilder setMarketDailyChanges (float** marketDailyChanges){
        //static Logger logger;
        //logger.log("ParametersBuilder: marketDailyChanges");
        parameters.marketDailyChanges = marketDailyChanges;
        return *this;
    }
    ParametersBuilder setIndexNames (std::vector<std::string> indexNames){
        //static Logger logger;
        //logger.log("ParametersBuilder: indexNames");
        parameters.indexNames = indexNames;
        return *this;
    }
    ParametersBuilder setHarvestPoint (float harvestPoint){
        //static Logger logger;
        //logger.log("ParametersBuilder: harvestPoint");
        parameters.harvestPoint = harvestPoint;
        return *this;
    }
    ParametersBuilder setRefillPoint (float refillPoint){
        //static Logger logger;
        //logger.log("ParametersBuilder: refillPoint");
        parameters.refillPoint = refillPoint;
        return *this;
    }
    ParametersBuilder setRebalance_period_months (int rebalance_period_months){
        //static Logger logger;
        //logger.log("ParametersBuilder: rebalance_period_months");
        parameters.rebalance_period_months = rebalance_period_months;
        return *this;
    }
    ParametersBuilder setStrategy (int strategy){
        //static Logger logger;
        //logger.log("ParametersBuilder: strategy");
        parameters.strategy = strategy;
        return *this;
    }
    ParametersBuilder setVolatilityStrategieSampleSize (int volatilityStrategieSampleSize){
        //static Logger logger;
        //logger.log("ParametersBuilder: volatilityStrategieSampleSize");
        parameters.volatilityStrategieSampleSize = volatilityStrategieSampleSize;
        return *this;
    }
    ParametersBuilder setVarianceCalcSampleSize (int varianceCalcSampleSize){
        //static Logger logger;
        //logger.log("ParametersBuilder: varianceCalcSampleSize");
        parameters.varianceCalcSampleSize = varianceCalcSampleSize;
        return *this;
    }
    ParametersBuilder setVolatilityStrategieLevel (float volatilityStrategieLevel){
        //static Logger logger;
        //logger.log("ParametersBuilder: volatilityStrategieLevel");
        parameters.volatilityStrategieLevel = volatilityStrategieLevel;
        return *this;
    }
    ParametersBuilder setNumberOfLeveragedInstruments(int numberOfLeveragedInstruments){
        //static Logger logger;
        //logger.log("ParametersBuilder: numberOfLeveragedInstruments");
        parameters.numberOfLeveragedInstruments = numberOfLeveragedInstruments;
        return *this;
    }
    ParametersBuilder setNumberOfFunds(int numberOfFunds){
        //static Logger logger;
        //logger.log("ParametersBuilder: numberOfFunds");
        parameters.numberOfFunds = numberOfFunds;
        return *this;
    }
    ParametersBuilder setIndexToMarket(std::map<int, int> indexToMarket){
        //static Logger logger;
        //logger.log("ParametersBuilder: indexToMarket");
        parameters.indexToMarket = indexToMarket;
        return *this;
    }
    ParametersBuilder setIncludeFeeStatus(bool includeFeeStatus){
        //static Logger logger;
        //logger.log("ParametersBuilder: includeFeeStatus");
        parameters.includeFeeStatus = includeFeeStatus;
        return *this;
    }
    ParametersBuilder setOutData (float* outData){
        //static Logger logger;
        //logger.log("ParametersBuilder: outData");
        parameters.outData = outData;
        return *this;
    }

    ParametersBuilder setGraphParameters (int* transactionDates,
            int* transactionTypes){
        //static Logger logger;
        //logger.log("ParametersBuilder: transactionTypes");
        
        GraphParameters graphParameters;
        graphParameters.isSet = true;
        graphParameters.positionCounter = 0;
        graphParameters.transactionDates = transactionDates;
        graphParameters.transactionTypes = transactionTypes;

        parameters.graphParameters = graphParameters;
        return *this;
    }

    ParametersBuilder setHistogramParameters (
            int daysInvesting){
        //static Logger logger;
        //logger.log("ParametersBuilder: daysInvesting");
        HistogramParameters histogramParameters;
        histogramParameters.isSet = true;
        histogramParameters.daysInvesting = daysInvesting;

        parameters.histogramParameters = histogramParameters;
        return *this;
    }
};
