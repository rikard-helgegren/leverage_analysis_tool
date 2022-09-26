#include <iostream>
#include <cstring>
#include <string>
#include <vector>
#include <stdexcept>
#include <future>  // library used for std::async and std::future
#include <map>
#include <sstream>
#include <iterator>


/**
* Converts indata of the format "name1,name2,...,nameN" to string array
* char array must end with .
*/
std::vector<std::string> convertCharPointerToStringVector(char* charPointer ){

    std::vector<std::string> vectorStringOut;
    std::string string_var = charPointer;
    std::stringstream strinStream(string_var);
 
    while (strinStream.good()) {
        std::string substr;
        std::getline(strinStream, substr, ',');
        vectorStringOut.push_back(substr);
    }
   
    return vectorStringOut;
}

/**
 * Each financial instrument is coupled to a market index
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

float sumFloats(float* floatArray, int nrOfFloats){
    float sum = 0.0f;

    for (int i =0; i< nrOfFloats; i++){
        sum = sum + floatArray[i];
    }

    return sum;
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
                currentValues[i] = (1.0f+loan) * proportionFunds/static_cast<float>(numberOfFunds);
            }
            else{
                currentValues[i] = (1.0f+loan)/static_cast<float>(numberOfFunds);
            }
        }
        else{
            if (numberOfFunds > 0){
                currentValues[i] = (1.0f+loan) * proportionLeverage/static_cast<float>(numberOfLeveragedInstruments);
            }
            else{
                currentValues[i] = (1.0f+loan)/static_cast<float>(numberOfLeveragedInstruments);
            }
        }
    }

}

/**
 * Check and mplement if harvest or refill is needed.
 */
void rebalanceAndHarvest(int* instrumentLeverages,
                         int item,
                         int numberOfFunds,
                         float* currentValues,
                         float harvestPoint,
                         float refillPoint,
                         float* referenceValue,
                         int numberOfLeveragedInstruments,
                         int nrOfInstruments,
                         float proportionLeverage){

    float totForRebalancing{0.0f};
    float changeInValue{0.0f};
    float totalValue{0.0f};

    //  No fund can trigger this rule    Need funds to do strategy
    if (instrumentLeverages[item] != 1 && numberOfFunds != 0){
        // Check if activating strategy
        if (currentValues[item] > harvestPoint * referenceValue[item] ||
            currentValues[item] < refillPoint * referenceValue[item]){

            totForRebalancing = 0;
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
                        currentValues[instrument] = currentValues[instrument] +(changeInValue / static_cast<float>(numberOfFunds));
                    }
                }
            }
        }
    }
}


void cppHarvestRefillAlgoSubPart(int                numberOfFunds,
                                 int                numberOfLeveragedInstruments,
                                 int                firstStartDay,
                                 int                lastStartDay,
                                 float              loan,
                                 int*               instrumentLeverages,
                                 int                nrOfInstruments,
                                 std::vector<std::string>       instrumentNames,
                                 float              proportionFunds,
                                 float              proportionLeverage,
                                 int                totNrDays,
                                 int                nrMarketsSelected,
                                 float**            marketDailyChanges,
                                 std::vector<std::string>       indexNames,
                                 int                daysInvesting,
                                 float              harvestPoint,
                                 float              refillPoint,
                                 std::map<int, int> indexToMarket,
                                 float*             outData){
    // Set up needed variables
    float currentValues[nrOfInstruments];
    float referenceValue[nrOfInstruments];

    float cutOfValue = 0.0f;
    

    for (int startDay = firstStartDay; startDay < lastStartDay; startDay++){
        
        setStartValuesOfInstruments(nrOfInstruments,
                                    instrumentLeverages,
                                    numberOfLeveragedInstruments,
                                    currentValues,
                                    loan,
                                    proportionFunds,
                                    numberOfFunds,
                                    proportionLeverage);

        // Run trough all intervals and add result
        for (int day = startDay; day < (startDay+daysInvesting); day++){
            for (int item =0; item < nrOfInstruments; item++){ //TODO: could be faster by sorting and dont do rebalance on leverage 1 by using two loops

                // Update with daily change
                currentValues[item] = currentValues[item] * (1.0f + marketDailyChanges[indexToMarket[item]][day] * static_cast<float>(instrumentLeverages[item]));

                // If instrument reaches cut off level it is sold before going lower
                if (instrumentLeverages[item] > 1 && currentValues[item] < cutOfValue){
                    currentValues[item] = cutOfValue;
                }

                rebalanceAndHarvest(instrumentLeverages,
                                    item,
                                    numberOfFunds,
                                    currentValues,
                                    harvestPoint,
                                    refillPoint,
                                    referenceValue,
                                    numberOfLeveragedInstruments,
                                    nrOfInstruments,
                                    proportionLeverage);
                
            }
        }
        
        outData[startDay] = sumFloats(currentValues, nrOfInstruments);
    
    }
}

extern "C" {
    void cppHarvestRefillAlgo(float  loan,
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
    }
}
