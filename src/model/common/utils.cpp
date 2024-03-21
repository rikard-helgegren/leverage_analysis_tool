/**
 * Copyright (C) 2024 Rikard Helgegren <rikard.helgegren@gmail.com>
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

#include "../constants.h"
#include "sumFloats.cpp"
#include "Parameters.cpp"
#include "../../Logger.cpp"

#pragma once


/**
 * In start of new intervall the starting values have to be set
 */
void setStartValuesOfInstruments(Parameters parameters, float* currentValues){
    //static Logger logger;
    //logger.log("utils: setStartValuesOfInstruments");
    for (int i = 0; i<parameters.nrOfInstruments; i++){
        if (parameters.instrumentLeverages[i] == 1){
            if (parameters.numberOfLeveragedInstruments > 0){ //dont save time with this if. can remove and only use the genereal calculation
                currentValues[i] = (1.0f + parameters.loan) * parameters.proportionFunds / static_cast<float>(parameters.numberOfFunds);
            }
            else{
                currentValues[i] = (1.0f + parameters.loan) / static_cast<float>(parameters.numberOfFunds);
            }
        }
        else{
            if (parameters.numberOfFunds > 0){ //dont save time with this if. can remove and only use the genereal calculation
                currentValues[i] = (1.0f + parameters.loan) * parameters.proportionLeverage / static_cast<float>(parameters.numberOfLeveragedInstruments);
            }
            else{
                currentValues[i] = (1.0f + parameters.loan) / static_cast<float>(parameters.numberOfLeveragedInstruments);
            }
        }

    }
    
}

float getSpread(int leverage){
    //static Logger logger;
    //logger.log("utils: setStartValuesOfInstruments");
    switch (leverage){
        case 1:
            return constants::spread_bull_1;
        case 2:
            return constants::spread_bull_2;
        case 3:
            return constants::spread_bull_3;
        case 4:
            return constants::spread_bull_4;
        case 5:
            return constants::spread_bull_5;
        case 6: //No data available
        case 7: //No data available
        case 8:
            return constants::spread_bull_8;
        case 9: //No data available
        case 10:
            return constants::spread_bull_10;
        default:
            if (leverage > 10) {
                return constants::spread_bull_10;
            } else {
                throw std::invalid_argument("received non positive leverage: " + std::to_string(leverage));
                return -1;
            }    
    }
}

/**
 * Return the fee rate related to the different leverage levels
 */
float getFeeLevel(int leverage){
    //static Logger logger;
    //logger.log("utils: getFeeLevel");
    switch (leverage){
        case 1:
            return constants::fee_bull_1;
        case 2:
            return constants::fee_bull_2;
        case 3:
            return constants::fee_bull_3;
        case 4:
            return constants::fee_bull_4;
        case 5:
            return constants::fee_bull_5;
        case 6: //No data available
        case 7: //No data available
        case 8:
            return constants::fee_bull_8;
        case 9: //No data available
        case 10:
            return constants::fee_bull_10;
        default:
            if (leverage > 10) {
                return constants::spread_bull_10;
            } else {
                throw std::invalid_argument("received non positive leverage: " + std::to_string(leverage));
                return -1;
            }    
    }
}

/**
 * Update instrument value with the daily change times its leverage 
 */
float updateCurrentInstrumentValue(Parameters parameters, float* currentValues, int item, int day){
    //static Logger logger;
    //logger.log("utils: updateCurrentInstrumentValue, item " + std::to_string(item));

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
    //static Logger logger;
    //logger.log("utils: checkPreConditionsRebalanceTime");
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
    //static Logger logger;
    //logger.log("utils: checkPreConditionsHarvestRefill");
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
    //static Logger logger;
    //logger.log("utils: doRebalancing");
    
    // Do rebalancing
    if (totForRebalancing > (referenceValue[item] - currentValues[item])){
        float changeInValue = currentValues[item] - referenceValue[item];
        currentValues[item] = referenceValue[item];

        if (changeInValue < 0){
            if (parameters.includeFeeStatus){
            changeInValue = changeInValue*getSpread(parameters.instrumentLeverages[item]);
            }
            else {
            changeInValue = changeInValue*getSpread(parameters.instrumentLeverages[item]);
            }
            
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
    //static Logger logger;
    //logger.log("utils: rebalanceInvestmentCirtificates");                
    float totForRebalancing{0.0f};
    float changeInValue{0.0f};
    float totalValue{0.0f};

    // Check total value in funds available for rebalancing
    for (int instrument = 0; instrument< parameters.nrOfInstruments; instrument++){
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
