#include <vector>

// Calculate linear fit to data
void calcRegressionline(std::vector<float> xVec,
						std::vector<float> yVec,
						int size,
						float* coeff,
						float* constTerm){

	float sumXY{0.0f};
	float sumX{0.0f};
	float sumy{0.0f};

	float sumXSquare{0.0f};
	float sumYSquare{0.0f};

	float xPosI{0.0f};
	float yPosI{0.0f};

	// create sums
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
	*coeff = numerator / denominator;

	// Calc constant
	numerator	= (sumy * sumXSquare - sumX * sumXY);
	denominator = (size_float * sumXSquare - sumX * sumX);
	*constTerm = numerator / denominator;
}


// Driver code
void regressionLine(float* inputvalues, float* fittedValues, int from_index, int to_index)
{	
	std::vector<float> yVec = std::vector<float>(inputvalues + from_index, inputvalues + to_index);
	std::vector<float> xVec;

	int size = to_index-from_index;

    for (int i = 0; i < size; i++){
        xVec.push_back(static_cast<float>(i));
    }
	
	float constTerm{0.0f};
	float coeff{0.0f};

	calcRegressionline(xVec, yVec, size, &coeff, &constTerm);
	
	for (int i = 0; i < size; i++){
        fittedValues[i] = constTerm + i * coeff;
    }
}
