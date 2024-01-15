/**
 * Copyright (C) 2024 Rikard Helgegren <rikard.helgegren@gmail.com>
 *
 * This software is only allowed for private use. As a private user you are allowed to copy,
 * modify, use, and compile the software. You are NOT however allowed to publish, sell, or
 * distribute this software, either in source code form or as a compiled binary, for any purpose,
 * commercial or non-commercial, by any means.
 */


// TODO clean and remove unused
#include <iostream>
#include <cstring>
#include <string>
#include <vector>
#include <stdexcept>
#include <future>  // library used for std::async and std::future
#include <map>
#include <sstream>
#include <iterator>

#include "../common/varianceAndVolatility.cpp"
#include "../common/convertArrayChangeToTotalValue.cpp"
#include "../common/convertCharPointerToStringVector.cpp"
#include "../common/mapIndexNrToMarketNr.cpp"
#include "../common/utils.cpp"
#include "../common/Parameters.cpp"
#include "../common/ParametersBuilder.cpp"
#include "../../Logger.cpp"
#include "graphStrategies.cpp"

// Check what startegy to use and launch it
void launchStartegy(Parameters parameters){
    static Logger logger;
    
    if (parameters.strategy == 0){
        holdStrategy(parameters);
    }
    else if (parameters.strategy == 1){
        harvestRefillStrategy(parameters);
    }
    else if (parameters.strategy == 2){
        rebalanceTimeStrategy(parameters);
    }
    else if (parameters.strategy == 3){
        doNotInvestStrategy(parameters);
    }
    else if (parameters.strategy == 4){
        varianceStrategy(parameters);
    }
}


extern "C" {
    float* calculateGraphOutput(float  loan,
            int*    instrumentLeverages,
            int     nrOfInstruments,
            char*   instrumentNames_chr,
            float   proportionFunds,
            float   proportionLeverage,
            int     totNrDays,
            int     nrMarketsSelected,
            float** marketDailyChanges,
            char*   indexNames_chr,
            float   harvestPoint,
            float   refillPoint,
            int     rebalance_period_months,
            int     strategy,
            int     volatilityStrategieSampleSize,
            int     varianceCalcSampleSize,
            float   volatilityStrategieLevel,
            bool    includeFeeStatus,
            float*  outData,
            int*    transactionDates,
            int*    transactionTypes){

        static Logger logger;
        std::vector<std::string> instrumentNames;
        std::vector<std::string> indexNames;
        
        instrumentNames = convertCharPointerToStringVector(instrumentNames_chr);
        indexNames      = convertCharPointerToStringVector(indexNames_chr);

        std::map<int, int> indexToMarket; 
        mapIndexNrToMarketNr(indexToMarket, indexNames, nrMarketsSelected, instrumentNames, nrOfInstruments);

        // TODO: make to seperate function and and make it return array or vector  
        // prepare right proportions
        int numberOfLeveragedInstruments = 0;
        int numberOfFunds = 0;
        for (int i = 0; i<nrOfInstruments; i++){
            if (instrumentLeverages[i] == 1){
                numberOfFunds += 1;
            }
            else{
                numberOfLeveragedInstruments += 1;
            }
        }

        Parameters parameters = ParametersBuilder()
                .setLoan(loan)
                .setInstrumentLeverages(instrumentLeverages)
                .setNrOfInstruments(nrOfInstruments)
                .setInstrumentNames(instrumentNames)
                .setProportionFunds(proportionFunds)
                .setProportionLeverage(proportionLeverage)
                .setTotNrDays(totNrDays)
                .setNrMarketsSelected(nrMarketsSelected)
                .setMarketDailyChanges(marketDailyChanges)
                .setIndexNames(indexNames)
                .setHarvestPoint(harvestPoint)
                .setRefillPoint(refillPoint)
                .setRebalance_period_months(rebalance_period_months)
                .setStrategy(strategy)
                .setVolatilityStrategieSampleSize(volatilityStrategieSampleSize)
                .setVarianceCalcSampleSize(varianceCalcSampleSize)
                .setVolatilityStrategieLevel(volatilityStrategieLevel)
                .setNumberOfLeveragedInstruments(numberOfLeveragedInstruments)
                .setNumberOfFunds(numberOfFunds)
                .setIndexToMarket(indexToMarket)
                .setIncludeFeeStatus(includeFeeStatus)
                .setOutData(outData)
                .setGraphParameters(transactionDates, transactionTypes)
                .build();

        if (parameters.graphParameters.isSet == true){
            logger.log("graphParam is set");
        }
        else {
            logger.log("graphParam is not set");
        }
        
        launchStartegy(parameters);

        return outData;
    }
}
