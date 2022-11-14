#include <iostream>
#include <string>
#include <vector>
#include <map>

#pragma once

/**
 * Makes mapping between each financial instrument and its market index
 *
 * key: instrument
 * value: market index
 */
void mapIndexNrToMarketNr(std::map<int,int> indexToMarket,
                          std::vector<std::string> marketNames,
                          int nrMarketsSelected,
                          std::vector<std::string> instrumentNames,
                          int nrOfInstruments){

    for (int instrumentNumber = 0; instrumentNumber < nrOfInstruments; instrumentNumber++){
        for (int number = 0; number < nrMarketsSelected; number++){
            if (marketNames[number] == instrumentNames[instrumentNumber]){
                indexToMarket.insert(std::pair<int, int>(instrumentNumber, number));
            }
        }
    }
}

/**
 * In start of new intervall the starting values have to be set
 */
void setStartValuesOfInstruments(int nrOfInstruments,
                                int* instrumentLeverages,
                                int numberOfLeveragedInstruments,
                                float* currentValues,
                                float loan,
                                float proportionFunds,
                                int numberOfFunds,
                                float proportionLeverage){
    
    for (int i = 0; i<nrOfInstruments; i++){
        if (instrumentLeverages[i] == 1){
            if (numberOfLeveragedInstruments > 0){
                currentValues[i] = (1.0f + loan) * proportionFunds / static_cast<float>(numberOfFunds);
            }
            else{
                currentValues[i] = (1.0f + loan) / static_cast<float>(numberOfFunds);
            }
        }
        else{
            if (numberOfFunds > 0){
                currentValues[i] = (1.0f + loan) * proportionLeverage / static_cast<float>(numberOfLeveragedInstruments);
            }
            else{
                currentValues[i] = (1.0f + loan) / static_cast<float>(numberOfLeveragedInstruments);
            }
        }
    }
}

/**
 * Update instrument value with the daily change times its leverage 
 */
float updateCurrentInstrumentValue(float*             currentValues,
                                   int                item,
                                   float**            marketDailyChanges,
                                   std::map<int, int> indexToMarket,
                                   int                day,
                                   int*               instrumentLeverages){
    
    return currentValues[item] * (1.0f + marketDailyChanges[indexToMarket[item]][day] * static_cast<float>(instrumentLeverages[item]));
}


bool checkPreConditionsRebalanceTime(int day,
                                     int rebalance_period_months,
                                     int* instrumentLeverages,
                                     int item,
                                     int numberOfFunds){
    
    //  Rebalance only leveraged         Need funds to do strategy
    if (instrumentLeverages[item] == 1 || numberOfFunds == 0 ){
        return false;
    }

    // Check it is the right day for rebalancing
    if (day % rebalance_period_months != 0  || day == 0){
        return false;
    }
    return true;
}


bool checkPreConditionsHarvestRefill(float  harvestPoint,
                                     float  refillPoint,
                                     float* referenceValue,
                                     float* currentValues,
                                     int*   instrumentLeverages,
                                     int    item,
                                     int    numberOfFunds){
    
    //  Rebalance only leveraged         Need funds to do strategy
    if (instrumentLeverages[item] == 1 || numberOfFunds == 0 ){
        return false;
    }
    // Check if not activating strategy
    if (currentValues[item] < harvestPoint * referenceValue[item] &&
        currentValues[item] > refillPoint * referenceValue[item]){

        return false;
    }
    return true;
}


/**
 * Implement rebalance
 */
void rebalance(int* instrumentLeverages,
               int item,
               int numberOfFunds,
               float* currentValues,
               float* referenceValue,
               int numberOfLeveragedInstruments,
               int nrOfInstruments,
               float proportionLeverage){

    float totForRebalancing{0.0f};
    float changeInValue{0.0f};
    float totalValue{0.0f};

    // Check total value in funds available for rebalancing
    for (int instrument = 0; instrument< numberOfLeveragedInstruments; instrument++){
        if (instrumentLeverages[instrument] == 1){
            totForRebalancing += currentValues[instrument];
        }
    }

    // Update reference values
    totalValue = sumFloats(currentValues, nrOfInstruments);
    for (int i = 0; i< nrOfInstruments; i++){
        if (instrumentLeverages[i] > 1){
            referenceValue[i] = (totalValue * proportionLeverage / static_cast<float>(numberOfLeveragedInstruments));
        }
    }

    if (totForRebalancing > (referenceValue[item] - currentValues[item])){
        changeInValue = currentValues[item] - referenceValue[item];
        currentValues[item] = referenceValue[item];

        for (int instrument = 0; instrument< nrOfInstruments; instrument++){
            if (instrumentLeverages[instrument] == 1){
                currentValues[instrument] = currentValues[instrument] + (changeInValue / static_cast<float>(numberOfFunds));
            }
        }
    }
}
