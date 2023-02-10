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
#include "../../fakeit.hpp"
#include "../../../src/model/common/regression.cpp"

using namespace fakeit;

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

    calcRegressionline(xVec, yVec, size, &coeff, &constTerm);

    float expectedCoeff = 1;
    float expectedConstTerm = 1;

    REQUIRE(coeff == expectedCoeff);
    REQUIRE(constTerm == expectedConstTerm);


    yVec = {-2,-4, -6, -8};
    expectedCoeff = -2;
    expectedConstTerm = -2;

    calcRegressionline(xVec, yVec, size, &coeff, &constTerm);

    REQUIRE(coeff == expectedCoeff);
    REQUIRE(constTerm == expectedConstTerm);
}


TEST_CASE( "Test calcRegressionline function", "[calcRegressionline]" ) {

    float inputvalues[8] = {1,2,3,4,-2,-4,-6,-8};
    float fittedValues[8];
    int from_index = 0;
    int to_index =3;




    // Setup mock behavior.
    struct SomeInterface {
        virtual int calcRegressionline(
                std::vector<float>,
                std::vector<float>,
                int, 
                float*, 
                float*) = 0;
    };
    Mock<SomeInterface> mock;

    //When(Method(calcRegressionline)).; // Method mock.foo will return 1 once.
    Verify(Method(mock, calcRegressionline));

    float expectedFittedValues[4] = {1,2,3,4};

    regressionLine(inputvalues, fittedValues, from_index, to_index);

    REQUIRE(fittedValues == expectedFittedValues);
}
