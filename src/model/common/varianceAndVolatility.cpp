/**
 * Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
 *
 * This software is only allowed for private use. As a private user you are allowed to copy,
 * modify, use, and compile the software. You are NOT however allowed to publish, sell, or
 * distribute this software, either in source code form or as a compiled binary, for any purpose,
 * commercial or non-commercial, by any means.
 */

#include <cmath>
#include <iostream>
#include "regression.cpp"

#pragma once

/*
* Calculate fitting line to dataset
*/
std::vector<float> calcLeastSquareFit(float* performance_full_time, int fromIndex, int toIndex){

    return regressionLine(performance_full_time, fromIndex, toIndex);
}

/*
* Calculate the variance* of the full time period
*/
float calcVariance(float* performance_full_time, int sizeArray, int sample_size){
    float totalDif = 0.0f;
    int elementsToSum = (sizeArray - sample_size);
    float subTotal{0.0f};

    std::vector<float> meanLine;

    for (int i = 0; i<elementsToSum; i +=sample_size ){
        subTotal = 0.0f;
        meanLine = calcLeastSquareFit(performance_full_time, i,sample_size+i);
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
