/**
 * Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
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
#include "utils.cpp"
#include "Parameters.cpp"
#include "ParametersBuilder.cpp"
#include "histogramStrategies.cpp"


// Check what startegy to use and launch it
void launchStartegy(Parameters parameters, int firstStartDay, int lastStartDay){
    
    std::vector<std::future<void>> m_Futures; //vector to store async reply

    if (parameters.strategy == 1){
        m_Futures.push_back(std::async (std::launch::async, harvestRefillStrategy, parameters, firstStartDay, lastStartDay));
    }
    else if (parameters.strategy == 2){
        m_Futures.push_back(std::async (std::launch::async, rebalanceTimeStrategy, parameters, firstStartDay, lastStartDay));
    }
    else if (parameters.strategy == 4){
        m_Futures.push_back(std::async (std::launch::async, varianceStrategy, parameters, firstStartDay, lastStartDay));
    }
}

void runAsyncCalculations(Parameters parameters){
    // Loop all possible start days
    
    int startDay = 0;
    int stepSize = 100;
    int veryLastDay = (parameters.totNrDays - parameters.daysInvesting);
    while ( startDay < veryLastDay){
        int startDayBatch;
        int lastDayBatch;

        // walk steps of stepSize
        if (startDay+stepSize < veryLastDay){
            startDayBatch = startDay;
            lastDayBatch = startDay + stepSize;
            startDay = startDay + stepSize;
        }
        else{ // if step would pass veryLastDay
            startDayBatch = startDay;
            lastDayBatch = veryLastDay;
            startDay = veryLastDay;
        }

        launchStartegy(parameters, startDayBatch, lastDayBatch);
    }
}


extern "C" {
    float* calculateHistogramOutput(float  loan,
                                  int*    instrumentLeverages,
                                  int     nrOfInstruments,
                                  char*   instrumentNames_chr,
                                  float   proportionFunds,
                                  float   proportionLeverage,
                                  int     totNrDays,
                                  int     nrMarketsSelected,
                                  float** marketDailyChanges,
                                  char*   indexNames_chr,
                                  int     daysInvesting,
                                  float   harvestPoint,
                                  float   refillPoint,
                                  int     rebalance_period_months,
                                  int     strategy,
                                  int     volatilityStrategieSampleSize,
                                  int     varianceCalcSampleSize,
                                  float   volatilityStrategieLevel,
                                  bool    includeFeeStatus,
                                  float*  outData){

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

        Parameters parameters = ParametersBuilder().setLoan(loan)
                                                   .setInstrumentLeverages(instrumentLeverages)
                                                   .setNrOfInstruments(nrOfInstruments)
                                                   .setInstrumentNames(instrumentNames)
                                                   .setProportionFunds(proportionFunds)
                                                   .setProportionLeverage(proportionLeverage)
                                                   .setTotNrDays(totNrDays)
                                                   .setNrMarketsSelected(nrMarketsSelected)
                                                   .setMarketDailyChanges(marketDailyChanges)
                                                   .setIndexNames(indexNames)
                                                   .setDaysInvesting(daysInvesting)
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
                                                   .build();
        

        runAsyncCalculations(parameters);

        return outData;
    }
}