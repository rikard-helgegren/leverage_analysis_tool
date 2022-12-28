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
#include "../../../src/model/common/sumFloats.cpp"

TEST_CASE( "Test sumFloats function", "[sumFloats]" ) {
    float floatArray[] = {1.0f, 2.0f, 3.0f};
    int nbrOfFloats = 3;
    float expectedSum = 6.0f;
    REQUIRE( sumFloats(floatArray, nbrOfFloats) == expectedSum );

    float floatArray2[] = {-1.0f, -2.0f, -3.0f};
    int nbrOfFloats2 = 3;
    float expectedSum2 = -6.0f;
    REQUIRE( sumFloats(floatArray2, nbrOfFloats2) == expectedSum2 );

    // Test with empty array
    float floatArray3[] = {};
    int nbrOfFloats3 = 0;
    float expectedSum3 = 0.0f;
    REQUIRE( sumFloats(floatArray3, nbrOfFloats3) == expectedSum3 );

    // Test with array of size 1
    float floatArray4[] = {5.0f};
    int nbrOfFloats4 = 1;
    float expectedSum4 = 5.0f;
    REQUIRE( sumFloats(floatArray4, nbrOfFloats4) == expectedSum4 );
}
