/**
 * Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
 *
 * This software is only allowed for private use. As a private user you are allowed to copy,
 * modify, use, and compile the software. You are NOT however allowed to publish, sell, or
 * distribute this software, either in source code form or as a compiled binary, for any purpose,
 * commercial or non-commercial, by any means.
 */

#define CATCH_CONFIG_MAIN
#include "../../catch.hpp"
#include "../../../src/model/common/convertArrayChangeToTotalValue.cpp"


// Test convertArrayChangeToTotalValueIndex with a range of valid indices
TEST_CASE("convertArrayChangeToTotalValueIndex with valid indices", "[index]") {
    float changeValues[] = {0.01, 0.02, 0.03, 0.04, 0.05};
    int size = sizeof(changeValues) / sizeof(changeValues[0]);
    float totalValueList[size];

    convertArrayChangeToTotalValueIndex(changeValues, 1, 3, totalValueList);
    REQUIRE(totalValueList[0] == Approx(1.0));
    REQUIRE(totalValueList[1] == Approx(1.02));
    REQUIRE(totalValueList[2] == Approx(1.0506));
}
/**
// Test convertArrayChangeToTotalValueIndex with an invalid index
TEST_CASE("convertArrayChangeToTotalValueIndex with invalid index", "[index]") {
    float changeValues[] = {0.01, 0.02, 0.03, 0.04, 0.05};
    int size = sizeof(changeValues) / sizeof(changeValues[0]);
    float totalValueList[size];

    // This should throw an exception because the "from" index is greater than the "to" index
    REQUIRE_THROWS_AS(convertArrayChangeToTotalValueIndex(changeValues, 3, 1, totalValueList), std::out_of_range);
}*/

// Test convertArrayChangeToTotalValueSize with a range of valid sizes
TEST_CASE("convertArrayChangeToTotalValueSize with valid sizes", "[size]") {
    float changeValues[] = {0.01, 0.02, 0.03, 0.04, 0.05};
    int size = sizeof(changeValues) / sizeof(changeValues[0]);
    float totalValueList[size];

    convertArrayChangeToTotalValueSize(changeValues, 3, totalValueList);
    REQUIRE(totalValueList[0] == Approx(1.0));
    REQUIRE(totalValueList[1] == Approx(1.01));
    REQUIRE(totalValueList[2] == Approx(1.0302));
}
/**
// Test convertArrayChangeToTotalValueSize with an invalid size
TEST_CASE("convertArrayChangeToTotalValueSize with invalid size", "[size]") {
    float changeValues[] = {0.01, 0.02, 0.03, 0.04, 0.05};
    int size = sizeof(changeValues) / sizeof(changeValues[0]);
    float totalValueList[size];

    // This should throw an exception because the size is negative
    REQUIRE_THROWS_AS(convertArrayChangeToTotalValueSize(changeValues, -1, totalValueList), std::out_of_range);
}*/