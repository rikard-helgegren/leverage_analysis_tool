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
#include "../calculations/varianceAndVolatility.cpp"
#include "../conversions/convertArrayChangeToTotalValue.cpp"
#include "../conversions/convertCharPointerToStringVector.cpp"
#include "applicationSpecficFunctions.cpp"

// Almost duplicate of cppRebalanceTimeAlgoSubPart due to speed
void cppHarvestRefillAlgoSubPart(int                      numberOfFunds,
                                 int                      numberOfLeveragedInstruments,
                                 int                      firstStartDay,
                                 int                      lastStartDay,
                                 float                    loan,
                                 int*                     instrumentLeverages,
                                 int                      nrOfInstruments,
                                 std::vector<std::string> instrumentNames,
                                 float                    proportionFunds,
                                 float                    proportionLeverage,
                                 int                      totNrDays,
                                 int                      nrMarketsSelected,
                                 float**                  marketDailyChanges,
                                 std::vector<std::string> indexNames,
                                 int                      daysInvesting,
                                 float                    harvestPoint,
                                 float                    refillPoint,
                                 std::map<int, int>       indexToMarket,
                                 float*                   outData){
    
    // Set up needed variables
    float currentValues[nrOfInstruments];
    float referenceValue[nrOfInstruments];

    float cutOfValue = 0.0f;

    for (int startDay = firstStartDay; startDay < lastStartDay; startDay++){

        setStartValuesOfInstruments(nrOfInstruments, instrumentLeverages, numberOfLeveragedInstruments, currentValues, loan, proportionFunds, numberOfFunds, proportionLeverage);

        // Run trough all intervals and add result
        for (int day = startDay; day < (startDay+daysInvesting); day++){
            for (int item =0; item < nrOfInstruments; item++){ //TODO: could be faster by sorting and dont do rebalance on leverage 1 by using two loops

                // Update with daily change
                currentValues[item] = updateCurrentInstrumentValue(currentValues, item, marketDailyChanges, indexToMarket, day, instrumentLeverages);

                // If instrument reaches cut off level it is sold before going lower
                if (instrumentLeverages[item] > 1 && currentValues[item] < cutOfValue){
                    currentValues[item] = cutOfValue;
                }

                if  (checkPreConditionsHarvestRefill(harvestPoint, refillPoint, referenceValue, currentValues, instrumentLeverages, item, numberOfFunds)){
                    rebalance(instrumentLeverages, item, numberOfFunds, currentValues, referenceValue, numberOfLeveragedInstruments, nrOfInstruments, proportionLeverage);
                }
            }
        }

        outData[startDay] = sumFloats(currentValues, nrOfInstruments);
    }
}


// Almost duplicate of cppHarvestRefillAlgoSubPart due to speed
void cppRebalanceTimeAlgoSubPart(int                      numberOfFunds,
                                 int                      numberOfLeveragedInstruments,
                                 int                      firstStartDay,
                                 int                      lastStartDay,
                                 float                    loan,
                                 int*                     instrumentLeverages,
                                 int                      nrOfInstruments,
                                 std::vector<std::string> instrumentNames,
                                 float                    proportionFunds,
                                 float                    proportionLeverage,
                                 int                      totNrDays,
                                 int                      nrMarketsSelected,
                                 float**                  marketDailyChanges,
                                 std::vector<std::string> indexNames,
                                 int                      daysInvesting,
                                 int                      rebalance_period_months,
                                 std::map<int, int>       indexToMarket,
                                 float*                   outData){
    // Set up needed variables
    float currentValues[nrOfInstruments];
    float referenceValue[nrOfInstruments];

    float cutOfValue = 0.0f;

    for (int startDay = firstStartDay; startDay < lastStartDay; startDay++){

        setStartValuesOfInstruments(nrOfInstruments, instrumentLeverages, numberOfLeveragedInstruments, currentValues, loan, proportionFunds, numberOfFunds, proportionLeverage);

        // Run trough all intervals and add result
        for (int day = startDay; day < (startDay+daysInvesting); day++){
            for (int item =0; item < nrOfInstruments; item++){ //TODO: could be faster by sorting and dont do rebalance on leverage 1 by using two loops

                // Update with daily change
                currentValues[item] = updateCurrentInstrumentValue(currentValues, item, marketDailyChanges, indexToMarket, day, instrumentLeverages);

                // If instrument reaches cut off level it is sold before going lower
                if (instrumentLeverages[item] > 1 && currentValues[item] < cutOfValue){
                    currentValues[item] = cutOfValue;
                }

                if (checkPreConditionsRebalanceTime(day-startDay, rebalance_period_months, instrumentLeverages, item, numberOfFunds)){

                    rebalance(instrumentLeverages, item, numberOfFunds, currentValues, referenceValue, numberOfLeveragedInstruments, nrOfInstruments, proportionLeverage);
                }
            }
        }

        outData[startDay] = sumFloats(currentValues, nrOfInstruments);
    }
}


// Almost duplicate of cppHarvestRefillAlgoSubPart due to speed
void cppVarianceAlgoSubPart(int                      numberOfFunds,
                            int                      numberOfLeveragedInstruments,
                            int                      firstStartDay,
                            int                      lastStartDay,
                            float                    loan,
                            int*                     instrumentLeverages,
                            int                      nrOfInstruments,
                            std::vector<std::string> instrumentNames,
                            float                    proportionFunds,
                            float                    proportionLeverage,
                            int                      totNrDays,
                            int                      nrMarketsSelected,
                            float**                  marketDailyChanges,
                            std::vector<std::string> indexNames,
                            int                      daysInvesting,
                            int                      rebalance_period_months,
                            std::map<int, int>       indexToMarket,
                            int                      volatilityStrategieSampleSize,
                            int                      varianceCalcSampleSize,
                            float                    volatilityStrategieLevel,
                            float*                   outData){
    // Set up needed variables
    float currentValues[nrOfInstruments];
    float referenceValue[nrOfInstruments];
    float total_value_list[volatilityStrategieSampleSize]; 

    float cutOfValue = 0.0f;
    float volatility = 0.0f;
    int startDayForVariance = 0;

    //Avoid sending negative index values of array
    if (lastStartDay < volatilityStrategieSampleSize){
        return;
    }
    if (firstStartDay < volatilityStrategieSampleSize){
        firstStartDay = volatilityStrategieSampleSize;
    }

    for (int startDay = firstStartDay; startDay < lastStartDay; startDay++){
        setStartValuesOfInstruments(nrOfInstruments, instrumentLeverages, numberOfLeveragedInstruments, currentValues, loan, proportionFunds, numberOfFunds, proportionLeverage);

        // Run trough all intervals and add result
        for (int day = startDay; day < (startDay+daysInvesting); day++){
            for (int item =0; item < nrOfInstruments; item++){ //TODO: could be faster by sorting and dont do rebalance on leverage 1 by using two loops
                
                if (instrumentLeverages[item] > 1 ){
                    startDayForVariance = day-volatilityStrategieSampleSize;
                    convertArrayChangeToTotalValueIndex(marketDailyChanges[indexToMarket[item]], startDayForVariance, day, total_value_list);
                    
                    volatility = calcVolatility(total_value_list, volatilityStrategieSampleSize, varianceCalcSampleSize);

                    //if vola. too high jump to next day
                    if (volatility > volatilityStrategieLevel){
                        continue;
                    }
                }
                // Update with daily change
                currentValues[item] = updateCurrentInstrumentValue(currentValues, item, marketDailyChanges, indexToMarket, day, instrumentLeverages);
                
                // If instrument reaches cut off level it is sold before going lower
                if (instrumentLeverages[item] > 1 && currentValues[item] < cutOfValue){
                    currentValues[item] = cutOfValue;
                }

                if (checkPreConditionsRebalanceTime(day-startDay, rebalance_period_months, instrumentLeverages, item, numberOfFunds)){

                    rebalance(instrumentLeverages, item, numberOfFunds, currentValues, referenceValue, numberOfLeveragedInstruments, nrOfInstruments, proportionLeverage);
                }
            }
        }

        outData[startDay] = sumFloats(currentValues, nrOfInstruments);
    }
}

// Check what startegy to use and launch it
void launchStartegy(int                      numberOfFunds,
                    int                      numberOfLeveragedInstruments,
                    int                      firstStartDay,
                    int                      lastStartDay,
                    float                    loan,
                    int*                     instrumentLeverages,
                    int                      nrOfInstruments,
                    std::vector<std::string> instrumentNames,
                    float                    proportionFunds,
                    float                    proportionLeverage,
                    int                      totNrDays,
                    int                      nrMarketsSelected,
                    float**                  marketDailyChanges,
                    std::vector<std::string> indexNames,
                    int                      daysInvesting,
                    float                    harvestPoint,
                    float                    refillPoint,
                    int                      rebalance_period_months,
                    int                      strategy,
                    std::map<int, int>       indexToMarket,
                    int                      volatilityStrategieSampleSize,
                    int                      varianceCalcSampleSize,
                    float                    volatilityStrategieLevel,
                    float*                   outData){

    std::vector<std::future<void>> m_Futures; //vector to store async reply

    if (strategy == 1){  //Harvest Refill
        m_Futures.push_back(std::async (std::launch::async,             // do async launch
                                        cppHarvestRefillAlgoSubPart,    // function pointer
                                        numberOfFunds,                  // all input parameters
                                        numberOfLeveragedInstruments,
                                        firstStartDay,
                                        lastStartDay,
                                        loan,
                                        instrumentLeverages,
                                        nrOfInstruments,
                                        instrumentNames,
                                        proportionFunds,
                                        proportionLeverage,
                                        totNrDays,
                                        nrMarketsSelected,
                                        marketDailyChanges,
                                        indexNames,
                                        daysInvesting,
                                        harvestPoint,
                                        refillPoint,
                                        indexToMarket,
                                        outData));
    }
    else if (strategy == 2){  // Rebalance Time
        m_Futures.push_back(std::async (std::launch::async,                     // do async launch
                                                cppRebalanceTimeAlgoSubPart,    // function pointer
                                                numberOfFunds,                  // all input parameters
                                                numberOfLeveragedInstruments,
                                                firstStartDay,
                                                lastStartDay,
                                                loan,
                                                instrumentLeverages,
                                                nrOfInstruments,
                                                instrumentNames,
                                                proportionFunds,
                                                proportionLeverage,
                                                totNrDays,
                                                nrMarketsSelected,
                                                marketDailyChanges,
                                                indexNames,
                                                daysInvesting,
                                                rebalance_period_months,
                                                indexToMarket,
                                                outData));
    }
    else if (strategy == 4){  // Variance dependent satrategy
        m_Futures.push_back(std::async (std::launch::async,                     // do async launch
                                                cppVarianceAlgoSubPart,    // function pointer
                                                numberOfFunds,                  // all input parameters
                                                numberOfLeveragedInstruments,
                                                firstStartDay,
                                                lastStartDay,
                                                loan,
                                                instrumentLeverages,
                                                nrOfInstruments,
                                                instrumentNames,
                                                proportionFunds,
                                                proportionLeverage,
                                                totNrDays,
                                                nrMarketsSelected,
                                                marketDailyChanges,
                                                indexNames,
                                                daysInvesting,
                                                rebalance_period_months,
                                                indexToMarket,
                                                volatilityStrategieSampleSize,
                                                varianceCalcSampleSize,
                                                volatilityStrategieLevel,
                                                outData));
    }
}

extern "C" {
    void cppRebalanceAlgo(float  loan,
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
                          float*  outData){

        std::vector<std::string> instrumentNames;
        std::vector<std::string> indexNames;

        instrumentNames = convertCharPointerToStringVector(instrumentNames_chr);
        indexNames      = convertCharPointerToStringVector(indexNames_chr);

        std::map<int, int> indexToMarket;
        mapIndexNrToMarketNr(indexToMarket, indexNames, nrMarketsSelected, instrumentNames, nrOfInstruments);

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

        // Loop all possible start days
        int startDay = 0;
        int stepSize = 100;
        int veryLastDay = (totNrDays - daysInvesting);
        while ( startDay < veryLastDay){
            int firstStartDay;
            int lastStartDay;

            // walk steps of stepSize
            if (startDay+stepSize < veryLastDay){
                firstStartDay = startDay;
                lastStartDay = startDay + stepSize;
                startDay = startDay + stepSize;
            }
            else{ // if step would pass veryLastDay
                firstStartDay = startDay;
                lastStartDay = veryLastDay;
                startDay = veryLastDay;
            }

            launchStartegy(numberOfFunds, numberOfLeveragedInstruments, firstStartDay, lastStartDay, loan, instrumentLeverages, nrOfInstruments, instrumentNames, proportionFunds, proportionLeverage, totNrDays, nrMarketsSelected, marketDailyChanges, indexNames, daysInvesting, harvestPoint, refillPoint, rebalance_period_months, strategy, indexToMarket, volatilityStrategieSampleSize, varianceCalcSampleSize, volatilityStrategieLevel, outData);
        }
    }
}
