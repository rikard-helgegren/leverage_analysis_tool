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

#include "../calculations/sumFloats.cpp"
#include "applicationSpecficFunctions.cpp"
#include "Parameters.cpp"

#pragma once

// Almost duplicate of cppRebalanceTimeAlgoSubPart due to speed
void harvestRefillStrategy(Parameters parameters, int firstStartDay, int lastStartDay){
    
    // Set up needed variables
    float currentValues[parameters.nrOfInstruments];
    float referenceValue[parameters.nrOfInstruments];

    float cutOfValue = 0.0f;

    for (int startDay = firstStartDay; startDay < lastStartDay; startDay++){

        setStartValuesOfInstruments(parameters, currentValues);

        // Run trough all intervals and add result
        for (int day = startDay; day < (startDay+parameters.daysInvesting); day++){
            for (int item =0; item < parameters.nrOfInstruments; item++){ //TODO: could be faster by sorting and dont do rebalance on leverage 1 by using two loops
                
                // Update with daily change
                currentValues[item] = updateCurrentInstrumentValue(parameters, currentValues, item, day);

                // If instrument reaches cut off level it is sold before going lower
                if (parameters.instrumentLeverages[item] > 1 && currentValues[item] < cutOfValue){
                    currentValues[item] = cutOfValue;
                }

                if  (checkPreConditionsHarvestRefill(parameters, referenceValue, currentValues,  item)){
                    rebalance(parameters, item, currentValues, referenceValue);
                }
            }
        }
        
        parameters.outData[startDay] = sumFloats(currentValues, parameters.nrOfInstruments);
    }
}


// Almost duplicate of cppHarvestRefillAlgoSubPart due to speed
void rebalanceTimeStrategy(Parameters parameters, int firstStartDay, int lastStartDay){
    // Set up needed variables
    float currentValues[parameters.nrOfInstruments];
    float referenceValue[parameters.nrOfInstruments];

    float cutOfValue = 0.0f; //TODO move to constants file

    for (int startDay = firstStartDay; startDay < lastStartDay; startDay++){

        setStartValuesOfInstruments(parameters, currentValues);

        // Run trough all intervals and add result
        for (int day = startDay; day < (startDay+parameters.daysInvesting); day++){
            for (int item =0; item < parameters.nrOfInstruments; item++){ //TODO: could be faster by sorting and dont do rebalance on leverage 1 by using two loops

                // Update with daily change
                currentValues[item] = updateCurrentInstrumentValue(parameters, currentValues, item, day);

                // If instrument reaches cut off level it is sold before going lower
                if (parameters.instrumentLeverages[item] > 1 && currentValues[item] < cutOfValue){
                    currentValues[item] = cutOfValue;
                }

                if (checkPreConditionsRebalanceTime(parameters, day-startDay, item)){

                    rebalance(parameters, item, currentValues, referenceValue);
                }
            }
        }

        parameters.outData[startDay] = sumFloats(currentValues, parameters.nrOfInstruments);
    }
}


// Almost duplicate of cppHarvestRefillAlgoSubPart due to speed
void varianceStrategy(Parameters parameters, int firstStartDay, int lastStartDay){
    // Set up needed variables
    float currentValues[parameters.nrOfInstruments];
    float referenceValue[parameters.nrOfInstruments];
    float total_value_list[parameters.volatilityStrategieSampleSize]; 

    float cutOfValue = 0.0f;
    float volatility = 0.0f;
    int startDayForVariance = 0;

    //Avoid sending negative index values of array
    if (lastStartDay < parameters.volatilityStrategieSampleSize){
        return;
    }
    if (firstStartDay < parameters.volatilityStrategieSampleSize){
        firstStartDay = parameters.volatilityStrategieSampleSize;
    }

    for (int startDay = firstStartDay; startDay < lastStartDay; startDay++){
        setStartValuesOfInstruments(parameters, currentValues);

        // Run trough all intervals and add result
        for (int day = startDay; day < (startDay+parameters.daysInvesting); day++){
            for (int item =0; item < parameters.nrOfInstruments; item++){ //TODO: could be faster by sorting and dont do rebalance on leverage 1 by using two loops
                
                if (parameters.instrumentLeverages[item] > 1 ){
                    startDayForVariance = day-parameters.volatilityStrategieSampleSize;
                    convertArrayChangeToTotalValueIndex(parameters.marketDailyChanges[parameters.indexToMarket[item]], startDayForVariance, day, total_value_list);
                    
                    volatility = calcVolatility(total_value_list, parameters.volatilityStrategieSampleSize, parameters.varianceCalcSampleSize);

                    //if vola. too high jump to next day
                    if (volatility > parameters.volatilityStrategieLevel){
                        continue;
                    }
                }
                // Update with daily change
                currentValues[item] = updateCurrentInstrumentValue(parameters, currentValues, item, day);
                
                // If instrument reaches cut off level it is sold before going lower
                if (parameters.instrumentLeverages[item] > 1 && currentValues[item] < cutOfValue){
                    currentValues[item] = cutOfValue;
                }

                if (checkPreConditionsRebalanceTime(parameters, day-startDay, item)){

                    rebalance(parameters, item, currentValues, referenceValue);
                }
            }
        }

        parameters.outData[startDay] = sumFloats(currentValues, parameters.nrOfInstruments);
    }
}
