/**
 * Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
 *
 * This software is only allowed for private use. As a private user you are allowed to copy,
 * modify, use, and compile the software. You are NOT however allowed to publish, sell, or
 * distribute this software, either in source code form or as a compiled binary, for any purpose,
 * commercial or non-commercial, by any means.
 */

#include <vector>

#define CATCH_CONFIG_MAIN
#include "../../catch.hpp"
#include "../../../src/model/common/regression.cpp"

//TODO: Tests only what it should do and not what it shouldnt
TEST_CASE( "Test calcRegressionline function", "[calcRegressionline]" ) {

    int size = 4;
    std::vector<float> yVec = {1, 2, 3, 4};
	std::vector<float> xVec;

    for (int i = 0; i < size; i++){
        xVec.push_back(static_cast<float>(i));
    }
	
	float constTerm{0.0f};
	float coeff{0.0f};

    std::vector<float> constTermAndCoeff;
	
	constTermAndCoeff = calcRegressionline(xVec, yVec, size);

    coeff = constTermAndCoeff[0];
    constTerm = constTermAndCoeff[1];

    float expectedCoeff = 1;
    float expectedConstTerm = 1;

    REQUIRE(coeff == expectedCoeff);
    REQUIRE(constTerm == expectedConstTerm);


    yVec = {-2,-4, -6, -8};
    expectedCoeff = -2;
    expectedConstTerm = -2;
	
	constTermAndCoeff = calcRegressionline(xVec, yVec, size);

    coeff = constTermAndCoeff[0];
    constTerm = constTermAndCoeff[1];

    REQUIRE(coeff == expectedCoeff);
    REQUIRE(constTerm == expectedConstTerm);
}


TEST_CASE( "Test regressionLine function", "[regressionLine]" ) {

    float inputvalues[4] = {1,2,3,4};
    std::vector<float> fittedValues;
    int from_index = 0;
    int to_index =3;

    std::vector<float> expectedFittedValues = {1,2,3};

    fittedValues = regressionLine(inputvalues, from_index, to_index);

    REQUIRE(fittedValues == expectedFittedValues);


    inputvalues[0] = -1;
    inputvalues[1] = -2;
    inputvalues[2] = -3;
    inputvalues[3] = -4;
    from_index = 0;
    to_index =3;

    expectedFittedValues = {-1,-2,-3};

    fittedValues = regressionLine(inputvalues, from_index, to_index);

    REQUIRE(fittedValues == expectedFittedValues);
}


