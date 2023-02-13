/**
 * Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
 *
 * This software is only allowed for private use. As a private user you are allowed to copy,
 * modify, use, and compile the software. You are NOT however allowed to publish, sell, or
 * distribute this software, either in source code form or as a compiled binary, for any purpose,
 * commercial or non-commercial, by any means.
 */

#include <iostream>
#include <vector>

#pragma once

#define CATCH_CONFIG_MAIN
#include "../../catch.hpp"
#include "../../../src/model/common/varianceAndVolatility.cpp"

//TODO: Might not be correct, wht about size n sample n. should run once right
TEST_CASE( "Test calcVariance function", "[calcVariance]" ) {

    float performance_full_time[5] = {1, 1, 1, 1, 1};
    int sizeArray = 5;
    int sample_size = 4;

    float excpectedVarinace = 0;

    float variance = calcVariance(performance_full_time, sizeArray, sample_size);

    REQUIRE(variance == excpectedVarinace);


    performance_full_time[0] = 1;
    performance_full_time[1] = 0;
    performance_full_time[2] = 0;
    performance_full_time[3] = 1;
    performance_full_time[4] = 1;
    sizeArray = 5;
    sample_size = 4;

    excpectedVarinace = 4;

    variance = calcVariance(performance_full_time, sizeArray, sample_size);

    REQUIRE(variance == excpectedVarinace);
}
