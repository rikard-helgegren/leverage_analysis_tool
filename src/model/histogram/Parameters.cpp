/**
 * Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
 *
 * This software is only allowed for private use. As a private user you are allowed to copy,
 * modify, use, and compile the software. You are NOT however allowed to publish, sell, or
 * distribute this software, either in source code form or as a compiled binary, for any purpose,
 * commercial or non-commercial, by any means.
 */

#pragma once
#include <string>


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
        std::map<int, int>        indexToMarket;

         void print(){
            std::cout << "loan " << loan <<  std::endl;
            std::cout << "instrumentLeverages " << instrumentLeverages[0] <<" "<< instrumentLeverages[1] << std::endl;
            std::cout << "nrOfInstruments " << nrOfInstruments << std::endl;
            std::cout << "instrumentNames " << instrumentNames[0] << std::endl;
            std::cout << "proportionFunds " << proportionFunds << std::endl;
            std::cout << "proportionLeverage " << proportionLeverage << std::endl;
            std::cout << "totNrDays " << totNrDays << std::endl;
            std::cout << "nrMarketsSelected " << nrMarketsSelected << std::endl;
            std::cout << "marketDailyChanges " << marketDailyChanges[0][0] << std::endl;
            std::cout << "indexNames " << indexNames[0] << std::endl;
            std::cout << "daysInvesting " << daysInvesting << std::endl;
            std::cout << "harvestPoint " << harvestPoint << std::endl;
            std::cout << "refillPoint " << refillPoint << std::endl;
            std::cout << "rebalance_period_months " << rebalance_period_months << std::endl;
            std::cout << "strategy " << strategy << std::endl;
            std::cout << "volatilityStrategieSampleSize " << volatilityStrategieSampleSize << std::endl;
            std::cout << "varianceCalcSampleSize " << varianceCalcSampleSize << std::endl;
            std::cout << "volatilityStrategieLevel " << volatilityStrategieLevel << std::endl;
            //std::cout << "outData" << outData << std::endl;
            std::cout << "numberOfLeveragedInstruments " << numberOfLeveragedInstruments << std::endl;
            std::cout << "numberOfFunds " << numberOfFunds << std::endl;
            std::cout << "includeFeeStatus " << includeFeeStatus << std::endl;
            // indexToMarket
        }
};
