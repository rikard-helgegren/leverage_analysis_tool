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

#include "../../Logger.cpp"

class Parameters{
    public:
        float   loan;
        float   loanPlussInterest;
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

    void printLog() const {
        std::ostringstream oss;
        std::string tmpString;

        //static Logger logger;
        //logger.log( "Loan: " + std::to_string(loan) );
        //logger.log(  "Instrument Leverages: ");
        for (int i = 0; i < nrOfInstruments; ++i) {
            //logger.log(  std::to_string(instrumentLeverages[i]) + " ");
        }
        //logger.log(  "\n");
        //logger.log(  "Number of Instruments: " + std::to_string(nrOfInstruments) );
        //logger.log(  "Instrument Names: ");
        for (const auto& name : instrumentNames) {
            //logger.log(  name + " ");
        }
        //logger.log(  "\n");
        //logger.log(  "Proportion Funds: " + std::to_string(proportionFunds) );
        //logger.log(  "Proportion Leverage: " + std::to_string(proportionLeverage) );
        //logger.log(  "Total Number of Days: " + std::to_string(totNrDays) );
        //logger.log(  "Number of Markets Selected: " + std::to_string(nrMarketsSelected) );

        //logger.log(  "marketDailyChanges: ");
        for (int i =0; i<nrOfInstruments; i++){
            for (int j =0; j<totNrDays && j<5; j++){
                //logger.log(  std::to_string(marketDailyChanges[i][j]) + " ");
            }
        }
        //logger.log(  "\n");

        //logger.log(  "indexNames: ");
        for (const auto& name : indexNames) {
            //logger.log( name + " ");
        }
        //logger.log(  "\n");


        //logger.log(  "harvestPoint: " + std::to_string(harvestPoint) );
        //logger.log(  "refillPoint: " + std::to_string(refillPoint) );
        //logger.log(  "rebalance_period_months: " + std::to_string(rebalance_period_months) );
        //logger.log(  "strategy: " + std::to_string(strategy) );
        //logger.log(  "volatilityStrategieSampleSize: " + std::to_string(volatilityStrategieSampleSize) );
        //logger.log(  "varianceCalcSampleSize: " + std::to_string(varianceCalcSampleSize) );
        //logger.log(  "volatilityStrategieLevel: " + std::to_string(volatilityStrategieLevel) );

        //logger.log(  "outdata: ");
        for (int i =0; i<totNrDays && i<5; i++){
                //logger.log(  std::to_string(outData[i]) + " ");
            }
        //logger.log(  "\n");
        
        //logger.log(  "numberOfLeveragedInstruments: " + std::to_string(numberOfLeveragedInstruments) );
        //logger.log(  "numberOfFunds: " + std::to_string(numberOfFunds) );
        //logger.log(  "includeFeeStatus: " + std::to_string(includeFeeStatus) );

        //logger.log(  "indexToMarket Map: ");
        for (const auto& pair : indexToMarket) {
        //logger.log( "Key: " + std::to_string(pair.first) + ", Value: " + std::to_string(pair.second) + " ");
        }
        //logger.log( "\n");
    }
};
