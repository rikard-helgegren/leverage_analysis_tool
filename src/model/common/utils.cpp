/**
 * Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
 *
 * This software is only allowed for private use. As a private user you are allowed to copy,
 * modify, use, and compile the software. You are NOT however allowed to publish, sell, or
 * distribute this software, either in source code form or as a compiled binary, for any purpose,
 * commercial or non-commercial, by any means.
 */

#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <stdexcept>

#include "constants.h"
#include "sumFloats.cpp"
#include "Parameters.cpp"
#include "../../Logger.cpp"

#pragma once

/**
 * In start of new intervall the starting values have to be set
 */
void setStartValuesOfInstruments(Parameters parameters, float* currentValues){
    for (int i = 0; i<parameters.nrOfInstruments; i++){
        if (parameters.instrumentLeverages[i] == 1){
            if (parameters.numberOfLeveragedInstruments > 0){ 
                currentValues[i] = (1.0f + parameters.loan) * parameters.proportionFunds / static_cast<float>(parameters.numberOfFunds);
            }
            else{
                currentValues[i] = (1.0f + parameters.loan) / static_cast<float>(parameters.numberOfFunds);
            }
        }
        else{
            if (parameters.numberOfFunds > 0){
                currentValues[i] = (1.0f + parameters.loan) * parameters.proportionLeverage / static_cast<float>(parameters.numberOfLeveragedInstruments);
            }
            else{
                currentValues[i] = (1.0f + parameters.loan) / static_cast<float>(parameters.numberOfLeveragedInstruments);
            }
        }

    }
    
}

/**
 * Return the fee rate related to the different leverage levels
 */
float getFeeLevel(int leverage){
    if (leverage == 1){
        return constants::fee_bull_1;
    }
    else if (leverage >= 2 || leverage <= 4){
        return constants::fee_bull_2_to_4;
    }
    else if (leverage >= 5){
        return constants::fee_bull_5_and_more;
    }
    else{
        throw std::invalid_argument("received non positive value");
        return -1;
    }
}

/**
 * Update instrument value with the daily change times its leverage 
 */
float updateCurrentInstrumentValue(Parameters parameters, float* currentValues, int item, int day){
    static Logger logger;

    float currentValue = currentValues[item]; 
    float oneDayChange = currentValue * parameters.marketDailyChanges[parameters.indexToMarket[item]][day] * static_cast<float>(parameters.instrumentLeverages[item]);
    float currencyChange = 1.0f; //TODO change in currency for this day compared to choosen default currency
    float dailyFee;
    float newValue;

    if(parameters.includeFeeStatus){
        dailyFee = currentValue * getFeeLevel(parameters.instrumentLeverages[item]);
    }
    else{
        dailyFee = 0.0f;
    }

    if (newValue < 0){
        return 0;
    }
        
    return (currentValue + oneDayChange - dailyFee) * currencyChange; 
}


bool checkPreConditionsRebalanceTime(Parameters parameters, int day, int item){

    //  Rebalance only leveraged                     Need funds to do strategy
    if (parameters.instrumentLeverages[item] == 1 || parameters.numberOfFunds == 0 ){
        return false;
    }

    // Check it is the right day for rebalancing
    if (day % parameters.rebalance_period_months != 0  || day == 0){
        return false;
    }
    return true;
}


bool checkPreConditionsHarvestRefill(Parameters parameters,
                                     float* referenceValue,
                                     float* currentValues,
                                     int    item){
    
    //  Rebalance only leveraged                      Need funds to do strategy
    if (parameters.instrumentLeverages[item] == 1 || parameters.numberOfFunds == 0 ){
        return false;
    }

    // Check if not activating strategy
    if (currentValues[item] < parameters.harvestPoint * referenceValue[item] &&
        currentValues[item] > parameters.refillPoint * referenceValue[item]){

        return false;
    }
    return true;
}


void doRebalancing(Parameters &parameters,
                   float totForRebalancing,
                   float* referenceValue,
                   float* currentValues,
                   int item,
                   int currentDay){
    static Logger logger;
    
    // Do rebalancing
    if (totForRebalancing > (referenceValue[item] - currentValues[item])){
        float changeInValue = currentValues[item] - referenceValue[item];
        currentValues[item] = referenceValue[item];


        if (changeInValue < 0){
            changeInValue = changeInValue*constants::spread;
            if (parameters.graphParameters.isSet){
                parameters.graphParameters.transactionTypes[parameters.graphParameters.positionCounter] = 1; //Buy levrage
            }
        }
        else {
            if (parameters.graphParameters.isSet){
                parameters.graphParameters.transactionTypes[parameters.graphParameters.positionCounter] = 2; //Sell leverage
            }
        }

        if (parameters.graphParameters.isSet){
            
            parameters.graphParameters.transactionDates[parameters.graphParameters.positionCounter] = currentDay;
            parameters.graphParameters.positionCounter = parameters.graphParameters.positionCounter + 1; 
        }

        for (int instrument = 0; instrument< parameters.nrOfInstruments; instrument++){
            if (parameters.instrumentLeverages[instrument] == 1){
                currentValues[instrument] = currentValues[instrument] + (changeInValue / static_cast<float>(parameters.numberOfFunds));
            }
        }
    }
}


/**
 * Implement rebalance of investment cirtificates (items)
 */
//TODO decompose, and make tests
void rebalanceInvestmentCirtificates(Parameters &parameters,
            int item,
            float* currentValues,
            float* referenceValue,
            int currentDay){
                
    float totForRebalancing{0.0f};
    float changeInValue{0.0f};
    float totalValue{0.0f};

    // Check total value in funds available for rebalancing
    for (int instrument = 0; instrument< parameters.numberOfLeveragedInstruments; instrument++){
        if (parameters.instrumentLeverages[instrument] == 1){
            totForRebalancing += currentValues[instrument];
        }
    }

    // Update reference values
    totalValue = sumFloats(currentValues, parameters.nrOfInstruments);
    for (int i = 0; i< parameters.nrOfInstruments; i++){
        if (parameters.instrumentLeverages[i] > 1){
            referenceValue[i] = (totalValue * parameters.proportionLeverage / static_cast<float>(parameters.numberOfLeveragedInstruments));
        }
    }

    doRebalancing(parameters, totForRebalancing, referenceValue, currentValues, item, currentDay);
}
