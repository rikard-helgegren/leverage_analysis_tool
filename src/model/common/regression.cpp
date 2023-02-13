/**
 * Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
 *
 * This software is only allowed for private use. As a private user you are allowed to copy,
 * modify, use, and compile the software. You are NOT however allowed to publish, sell, or
 * distribute this software, either in source code form or as a compiled binary, for any purpose,
 * commercial or non-commercial, by any means.
 */

#include <vector>

#pragma once

// Calculate linear fit to data
std::vector<float> calcRegressionline(std::vector<float> xVec,
						std::vector<float> yVec,
						int size){

	float coeff;
	float constTerm;

	float sumXY{0.0f};
	float sumX{0.0f};
	float sumy{0.0f};

	float sumXSquare{0.0f};
	float sumYSquare{0.0f};
             
	float xPosI{0.0f};
	float yPosI{0.0f};

	// create sums // TODO use std librarys for scalar product and sum.
	for (int i = 0; i < size; i++) {
			// In a csv file all the values of
			// xi and yi are separated by commas
			xPosI = xVec[i];
			yPosI = yVec[i];
			sumXY += xPosI * yPosI;
			sumX += xPosI;
			sumy += yPosI;
			sumXSquare += xPosI * xPosI;
			sumYSquare += yPosI * yPosI;
	}

	float numerator{0.0f};
	float denominator{0.0f};
	float size_float = static_cast<float>(size);

	// Calc coefficient of slope
	numerator = ( size_float * sumXY - sumX * sumy);
	denominator = (size_float * sumXSquare - sumX * sumX);
	coeff = numerator / denominator;

	// Calc constant
	numerator	= (sumy * sumXSquare - sumX * sumXY);
	denominator = (size_float * sumXSquare - sumX * sumX);
	constTerm = numerator / denominator;

	std::vector<float> returnValues = {coeff, constTerm};

	return returnValues;

}


// Driver code
std::vector<float> regressionLine(float* inputvalues, int from_index, int to_index)
{	

	int size = to_index-from_index;

	std::vector<float> fittedValues;
	std::vector<float> yVec = std::vector<float>(inputvalues + from_index, inputvalues + to_index);
	std::vector<float> xVec;


    for (int i = 0; i < size; i++){
        xVec.push_back(static_cast<float>(i));
    }
	
	std::vector<float> constTermAndCoeff;
	
	constTermAndCoeff = calcRegressionline(xVec, yVec, size);
	
	float constTerm = constTermAndCoeff[1];
	float coeff = constTermAndCoeff[0];

	for (int i = 0; i < size; i++){
        fittedValues.push_back(constTerm + i * coeff);
    }

	return fittedValues;
}
