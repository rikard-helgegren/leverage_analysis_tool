#include <cmath>
#include <iostream>
#include "regression.cpp"

#pragma once

/*
* Calculate fitting line to dataset
*/
void calc_mean_line_fit(float* performance_full_time, int fromIndex, int toIndex, float* meanLine){

    regressionLine(performance_full_time, meanLine, fromIndex, toIndex);
}

/*
* Calculate the variance* of the full time period
*/
float calcVariance(float* performance_full_time, int sizeArray, int sample_size){
    float totalDif = 0.0f;
    int elementsToSum = (sizeArray - sample_size);
    float subTotal{0.0f};

    float meanLine[sample_size];

    for (int i = 0; i<elementsToSum; i +=sample_size ){
        subTotal = 0.0f;
        calc_mean_line_fit(performance_full_time, i,sample_size+i, meanLine);
        for (int j = 0; j<sample_size; j++){
            subTotal += ((performance_full_time[i+sample_size] - meanLine[j])/meanLine[j])*((performance_full_time[i+sample_size] - meanLine[j])/meanLine[j]);
        }
    
        totalDif += subTotal;
    }

    if (elementsToSum > 0){
        return totalDif/static_cast<float>(elementsToSum);
    }
    else{
        //logging logging.error("To few values to calculate variance from")
    }
    return 0;
    
}


//TODO: double check with unit test, first value is too large and sacled compared to python implementation
/*
* Calculate the volatility* of the full time period
*/
float calcVolatility(float* performance_full_time, int sizeArray, int sample_size){ 
    return std::sqrt(calcVariance(performance_full_time, sizeArray, sample_size));
}
