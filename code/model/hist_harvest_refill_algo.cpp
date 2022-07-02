#include <stdio.h>
#include <iostream>
#include <cstring>
#include <string>
#include <vector>
#include <stdexcept>
#include <future>         // library used for std::async and std::future

#include <iostream>
#include <stdlib.h>
#include <iomanip>


/**
* Converts indata of the format "name1,name2,...,nameN." to string array
* char array must end with .
*/
void char_pointer_to_string_array(char* charPointer, std::string* stringArray_out){
    int noStringsAdded = 0;
    for(int i =0; charPointer[i] != '.'; i++){ // char array ends with '.'

        if (charPointer[i] == ','){ // splitter char
            noStringsAdded += 1;
        }
        else{
            stringArray_out[noStringsAdded] = stringArray_out[noStringsAdded] + charPointer[i];
        }
    }
}


int MapInstrumentNumberToMarketNumber(const std::string* marketNames,
                                      const std::string* instrumentNames,
                                      int instrumentNumber,
                                      int nrMarketsSelected){

    for (int number = 0; number < nrMarketsSelected; number++){
        if (marketNames[number] == instrumentNames[instrumentNumber]){
            return number;
        }
    }

    //country not found throw error
    throw std::invalid_argument( "Index not found" );
    return -1;
}

void SumPortfolioItems(float* currentValue, int nrOfInstruments, float &totalValue_out){
    totalValue_out = 0.0f;

    for (int i =0; i< nrOfInstruments; i++){
        totalValue_out = totalValue_out + currentValue[i];
    }
}


void cpp_harvest_refill_algo1(int            numberOfFunds,
                              int            numberOfLeveragedInstruments,
                              int            firstStartDay,
                              int            lastStartDay,
                              float          loan,
                              int*           instrumentLeverages,    // instrument selected
                              int            nrOfInstruments,
                              std::string*   instrumentNames,
                              float          proportionFunds,
                              float          proportionLeverage,
                              int            totNrDays,
                              int            nrMarketsSelected,
                              std::string*   countries,
                              float**        dailyChange,
                              std::string*   indexNames,
                              int            daysInvesting,
                              float          harvestPoint,
                              float          refillPoint,
                              float*         outData){

    // Set up needed variables
    float currentValue[nrOfInstruments];
    float referenceValue[nrOfInstruments];

    int   marketNumber;
    float changeInValue;
    float totalValue;
    float totalResults;
    float cutOfValue = 0.0f;
    bool  appliedChange = false;
    float totForRebalancing;


    for (int startDay = firstStartDay; startDay < lastStartDay; startDay++){
        // Prepare start values for each instrument
        for (int i = 0; i<nrOfInstruments; i++){
            if (instrumentLeverages[i] == 1){
                if (numberOfLeveragedInstruments > 0){
                    currentValue[i] = (1.0f+loan) * proportionFunds/(float)numberOfFunds;
                }
                else{
                    currentValue[i] = (1.0f+loan)/(float)numberOfFunds;
                }
            }
            else{
                if (numberOfFunds > 0){
                    currentValue[i] = (1.0f+loan) * proportionLeverage/(float)numberOfLeveragedInstruments;
                }
                else{
                    currentValue[i] = (1.0f+loan)/(float)numberOfLeveragedInstruments;
                }
            }
        }



        // Run trough one interval and add result
        for (int day = startDay; day < (startDay+daysInvesting); day++){ // -2 to not get out of bounds understand
            for (int item =0; item < nrOfInstruments; item++){
                // set to default
                appliedChange = false;

                // Update with daily change
                marketNumber = MapInstrumentNumberToMarketNumber(indexNames, instrumentNames, item, nrMarketsSelected);
                currentValue[item] = currentValue[item] * (1.0f + dailyChange[marketNumber][day] * (float)instrumentLeverages[item]);

                // If instrument reaches cut off level it is sold before going lower
                if (instrumentLeverages[item] > 1 && currentValue[item] < cutOfValue){
                    currentValue[item] = cutOfValue;
                }

                ///// rebalance harvest \\\\\\\\\\
                //  No fund can trigger this rule    Need funds to do strategy
                if (instrumentLeverages[item] != 1 && numberOfFunds != 0){
                    // Check if activating strategy
                    if (currentValue[item] > harvestPoint * referenceValue[item] ||
                        currentValue[item] < refillPoint * referenceValue[item]){

                        totForRebalancing = 0;
                        for (int instrument = 0; instrument< numberOfLeveragedInstruments; instrument++){
                            if (instrumentLeverages[instrument] == 1){
                                totForRebalancing += currentValue[instrument];
                            }
                        }

                        // Update reference values
                        SumPortfolioItems(currentValue, nrOfInstruments, totalValue);
                        for (int i = 0; i< nrOfInstruments; i++){
                            if (instrumentLeverages[i] > 1){
                                referenceValue[i] = (totalValue * proportionLeverage / (float)numberOfLeveragedInstruments);
                            }
                        }

                        if (totForRebalancing > (referenceValue[item] - currentValue[item])){

                            changeInValue = currentValue[item] - referenceValue[item];
                            currentValue[item] = referenceValue[item];

                            for (int instrument = 0; instrument< nrOfInstruments; instrument++){
                                if (instrumentLeverages[instrument] == 1){
                                    currentValue[instrument] = currentValue[instrument] +(changeInValue / (float)numberOfFunds);
                                }
                            }
                        }
                    }
                }
            }
        }

        // sum total results
        totalResults = 0.0f;
        for (int item = 0; item < nrOfInstruments; item++){
            totalResults += currentValue[item];
        }

        outData[startDay] = totalResults; // add result of interval to array sent back to python
    }
}

extern "C" {
    // changes compared to do nothing calculations when oly holding one non leverage fund. should not happen.
    void cpp_harvest_refill_algo(float  loan,
                                int*    instrumentLeverages,    // instrument selected
                                int     nrOfInstruments,
                                char*   instrumentNames_chr,
                                float   proportionFunds,
                                float   proportionLeverage,
                                int     totNrDays,
                                int     nrMarketsSelected,
                                char*   countries_chr,
                                float** dailyChange,
                                char*   indexNames_chr,
                                int     daysInvesting,
                                float   harvestPoint,
                                float   refillPoint,
                                float*  outData){

        ////setup needs only once \\\\\

        // convert comma separated car* to string*
        std::string instrumentNames[nrOfInstruments];
        char_pointer_to_string_array(instrumentNames_chr, instrumentNames);

        std::string countries[nrMarketsSelected];
        char_pointer_to_string_array(countries_chr, countries);

        std::string indexNames[nrMarketsSelected];
        char_pointer_to_string_array(indexNames_chr, indexNames);

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
        std::vector<std::future<void>> m_Futures; //vector to store async reply
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

            m_Futures.push_back(std::async (std::launch::async,             // do async launch
                                            cpp_harvest_refill_algo1,       // name of function
                                            numberOfFunds,                  //all in parameters
                                            numberOfLeveragedInstruments,
                                            firstStartDay,
                                            lastStartDay,
                                            loan,
                                            instrumentLeverages,    // instrument selected
                                            nrOfInstruments,
                                            &instrumentNames[0],
                                            proportionFunds,
                                            proportionLeverage,
                                            totNrDays,
                                            nrMarketsSelected,
                                            &countries[0],
                                            dailyChange,
                                            &indexNames[0],
                                            daysInvesting,
                                            harvestPoint,
                                            refillPoint,
                                            outData));
        }
    }
}
