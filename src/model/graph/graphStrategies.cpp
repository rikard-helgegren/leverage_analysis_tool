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
#include <stdexcept>
#include <sstream>
#include <iterator>

#include "../constants.h"
#include "../common/sumFloats.cpp"
#include "../common/utils.cpp"
#include "../common/Parameters.cpp"
#include "../common/convertArrayChangeToTotalValue.cpp"
#include "../common/varianceAndVolatility.cpp"
#include "../../Logger.cpp"

#pragma once


void holdStrategy(Parameters parameters){
    //static Logger logger;
    //logger.log("graphStrategies: holdStrategy");

    float currentValues[parameters.nrOfInstruments];
    float referenceValue[parameters.nrOfInstruments];
    float cutOfValue = 0.0f;
    float loanPlusInterest = parameters.loan;

    parameters.outData[0] = 1;
    int startDay = 0;
    int lastDay = parameters.totNrDays;

    setStartValuesOfInstruments(parameters, currentValues);

    // Run trough all intervals and add result
    for (int day = startDay; day < lastDay; day++){
        for (int item = 0; item < parameters.nrOfInstruments; item++){ //TODO: could be faster by sorting and dont do rebalance on leverage 1 by using two loops
            
            // Update with daily change
            currentValues[item] = updateCurrentInstrumentValue(parameters, currentValues, item, day);

            // If leveraged instrument reaches cut off level it is sold before going lower
            if (parameters.instrumentLeverages[item] > 1 && currentValues[item] < cutOfValue){
                currentValues[item] = cutOfValue;
            }
        }

        if (parameters.includeFeeStatus){
            loanPlusInterest += loanPlusInterest * constants::loan_rate;
        }

        parameters.outData[day+1] = sumFloats(currentValues, parameters.nrOfInstruments) - loanPlusInterest;
    }
}

// Almost duplicate of cppRebalanceTimeAlgoSubPart due to speed
void harvestRefillStrategy(Parameters parameters){
    //static Logger logger;
    //logger.log("graphStrategies: harvestRefillStrategy");
    
    float currentValues[parameters.nrOfInstruments];
    float referenceValue[parameters.nrOfInstruments];
    float cutOfValue = 0.0f;
    float loanPlusInterest = parameters.loan;

    parameters.outData[0] = 1;
    int startDay = 0;
    int lastDay = parameters.totNrDays;

    int itemsToRebalance[parameters.nrOfInstruments];
    int itemsReaddyForrebalance = 0;

    setStartValuesOfInstruments(parameters, currentValues);

    // Run trough all intervals and add result
    for (int day = startDay; day < lastDay; day++){
        itemsReaddyForrebalance = 0;
        for (int item =0; item < parameters.nrOfInstruments; item++){ //TODO: could be faster by sorting and dont do rebalance on leverage 1 by using two loops

            // Update with daily change
            currentValues[item] = updateCurrentInstrumentValue(parameters, currentValues, item, day);

            // If instrument reaches cut off level it is sold before going lower
            if (parameters.instrumentLeverages[item] > 1 && currentValues[item] < cutOfValue){
                currentValues[item] = cutOfValue;
            }

            if  (checkPreConditionsHarvestRefill(parameters, referenceValue, currentValues,  item)){
                itemsToRebalance[itemsReaddyForrebalance] = item;
                itemsReaddyForrebalance = itemsReaddyForrebalance + 1;
            }
        }

        if (itemsReaddyForrebalance > 0){
            rebalanceInvestmentCirtificates(parameters, itemsToRebalance, itemsReaddyForrebalance, currentValues, referenceValue, day);
        }

        if (parameters.includeFeeStatus){
            loanPlusInterest += loanPlusInterest * constants::loan_rate;
        }

        parameters.outData[day+1] = sumFloats(currentValues, parameters.nrOfInstruments) - loanPlusInterest;
    }
}

// Almost duplicate of cppHarvestRefillAlgoSubPart due to speed
void rebalanceTimeStrategy(Parameters parameters){
    //static Logger logger;
    //logger.log("graphStrategies: rebalanceTimeStrategy");

    float currentValues[parameters.nrOfInstruments];
    float referenceValue[parameters.nrOfInstruments];
    float cutOfValue = 0.0f; //TODO move to constants file
    float loanPlusInterest = parameters.loan;

    parameters.outData[0] = 1;
    int startDay = 0;
    int lastDay = parameters.totNrDays;

    int itemsToRebalance[parameters.nrOfInstruments];
    int itemsReaddyForrebalance = 0;

    
    setStartValuesOfInstruments(parameters, currentValues);

    // Run trough all intervals and add result
    for (int day = startDay; day < lastDay; day++){
        itemsReaddyForrebalance = 0;
        for (int item =0; item < parameters.nrOfInstruments; item++){ //TODO: could be faster by sorting and dont do rebalance on leverage 1 by using two loops

            // Update with daily change
            currentValues[item] = updateCurrentInstrumentValue(parameters, currentValues, item, day);

            // If instrument reaches cut off level it is sold before going lower
            if (parameters.instrumentLeverages[item] > 1 && currentValues[item] < cutOfValue){
                currentValues[item] = cutOfValue;
            }

            if (checkPreConditionsRebalanceTime(parameters, day-startDay, item)){
                itemsToRebalance[itemsReaddyForrebalance] = item;
                itemsReaddyForrebalance = itemsReaddyForrebalance + 1;
            }
        }

        if (itemsReaddyForrebalance > 0){
            rebalanceInvestmentCirtificates(parameters, itemsToRebalance, itemsReaddyForrebalance, currentValues, referenceValue, day);
        }
        
        
        if (parameters.includeFeeStatus){
            loanPlusInterest += loanPlusInterest * constants::loan_rate;
        }
        
        parameters.outData[day+1] = sumFloats(currentValues, parameters.nrOfInstruments) - loanPlusInterest;
    }
}

//TODO: Inclomplete
void rebalanceTimeStrategyIncLoan(Parameters parameters){
    //static Logger logger;
    //logger.log("graphStrategies: rebalanceTimeStrategyIncLoan");

    float currentValues[parameters.nrOfInstruments];
    float referenceValue[parameters.nrOfInstruments];
    float cutOfValue = 0.0f; //TODO move to constants file
    float loanPlusInterest = parameters.loan;
    float prevPortfolioValue = 1.0f;

    parameters.outData[0] = 1;
    int startDay = 0;
    int lastDay = parameters.totNrDays;

    int itemsToRebalance[parameters.nrOfInstruments];
    int itemsReaddyForrebalance = 0;

    
    setStartValuesOfInstruments(parameters, currentValues);

    // Run trough all intervals and add result
    for (int day = startDay; day < lastDay; day++){
        itemsReaddyForrebalance = 0;
        for (int item =0; item < parameters.nrOfInstruments; item++){ //TODO: could be faster by sorting and dont do rebalance on leverage 1 by using two loops

            // Update with daily change
            currentValues[item] = updateCurrentInstrumentValue(parameters, currentValues, item, day);

            // If instrument reaches cut off level it is sold before going lower
            if (parameters.instrumentLeverages[item] > 1 && currentValues[item] < cutOfValue){
                currentValues[item] = cutOfValue;
            }

            if (checkPreConditionsRebalanceTimeIncLoan(parameters, day-startDay, item)){
                itemsToRebalance[itemsReaddyForrebalance] = item;
                itemsReaddyForrebalance = itemsReaddyForrebalance + 1;
            }
        }

        if (itemsReaddyForrebalance > 0){
            rebalanceInvestmentCirtificatesIncLoan(parameters, itemsToRebalance, itemsReaddyForrebalance, currentValues, referenceValue, day, parameters.loan, prevPortfolioValue, loanPlusInterest);
        }
        
        
        if (parameters.includeFeeStatus){
            loanPlusInterest += loanPlusInterest * constants::loan_rate;
        }

         
        parameters.outData[day+1] = sumFloats(currentValues, parameters.nrOfInstruments) - loanPlusInterest;
    }
}


void doNotInvestStrategy(Parameters parameters){
    //static Logger logger;
    //logger.log("graphStrategies: doNotInvestStrategy");

    parameters.outData[0] = 1;
    int startDay = 0;
    int lastDay = parameters.totNrDays;

    for (int day = startDay; day < lastDay; day++){
        parameters.outData[day+1] = 1;//TODO implement with inflation & loan
    }
}

// Almost duplicate of cppHarvestRefillAlgoSubPart due to speed
void varianceStrategy(Parameters parameters){
    //static Logger logger;
    //logger.log("graphStrategies: varianceStrategy");

    // Set up needed variables
    float currentValues[parameters.nrOfInstruments];
    float referenceValue[parameters.nrOfInstruments];
    bool hasDoneAction[parameters.nrOfInstruments];
    float total_value_list[parameters.volatilityStrategieSampleSize]; 
    float loanPlusInterest = parameters.loan;

    float cutOfValue = 0.0f;
    float volatility = 0.0f;
    int startDayForVariance = 0;

    parameters.outData[parameters.volatilityStrategieSampleSize] = 1;
    int startDay = parameters.volatilityStrategieSampleSize;
    int lastDay = parameters.totNrDays;

    int itemsToRebalance[parameters.nrOfInstruments];
    int itemsReaddyForrebalance = 0;

    //Avoid sending negative index values of array
    if (lastDay < parameters.volatilityStrategieSampleSize){
        return;
    }

    setStartValuesOfInstruments(parameters, currentValues);

    // Run trough all intervals and add result
    for (int day = startDay; day < lastDay; day++){
        itemsReaddyForrebalance = 0;
        for (int item =0; item < parameters.nrOfInstruments; item++){ //TODO: could be faster by sorting and dont do rebalance on leverage 1 by using two loops
            
            if (parameters.instrumentLeverages[item] > 1 ){
                startDayForVariance = day-parameters.volatilityStrategieSampleSize;
                convertArrayChangeToTotalValueIndex(parameters.marketDailyChanges[parameters.indexToMarket[item]], startDayForVariance, day, total_value_list);
                
                volatility = calcVolatility(total_value_list, parameters.volatilityStrategieSampleSize, parameters.varianceCalcSampleSize);

                //if vola. too high jump to next day
                if (volatility > parameters.volatilityStrategieLevel){
                    hasDoneAction[item] = false;
                    continue;
                }
            }
            // Update with daily change
            currentValues[item] = updateCurrentInstrumentValue(parameters, currentValues, item, day);
            
            if (!hasDoneAction[item] && parameters.includeFeeStatus){
                currentValues[item] /= constants::spread;
            }

            // If instrument reaches cut off level it is sold before going lower
            if (parameters.instrumentLeverages[item] > 1 && currentValues[item] < cutOfValue){
                currentValues[item] = cutOfValue;
            }

            if (checkPreConditionsRebalanceTime(parameters, day-startDay, item)){

                itemsToRebalance[itemsReaddyForrebalance] = item;
                itemsReaddyForrebalance = itemsReaddyForrebalance + 1;
            }
        }

        if (itemsReaddyForrebalance > 0){
            rebalanceInvestmentCirtificates(parameters, itemsToRebalance, itemsReaddyForrebalance, currentValues, referenceValue, day);
        }

        if (parameters.includeFeeStatus){
            loanPlusInterest += loanPlusInterest * constants::loan_rate;
        }

        parameters.outData[day+1] = sumFloats(currentValues, parameters.nrOfInstruments) - loanPlusInterest;
    }   
    
}
