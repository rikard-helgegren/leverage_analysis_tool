/**
 * Copyright (C) 2024 Rikard Helgegren <rikard.helgegren@gmail.com>
 *
 * This software is only allowed for private use. As a private user you are allowed to copy,
 * modify, use, and compile the software. You are NOT however allowed to publish, sell, or
 * distribute this software, either in source code form or as a compiled binary, for any purpose,
 * commercial or non-commercial, by any means.
 */

#define CATCH_CONFIG_MAIN
#include "../../catch.hpp"
#include "../../../src/model/graph/graphStrategies.cpp"

#include <iostream>
#include <vector>

#include "../../../src/model/common/utils.cpp"
#include "../helpers/ParametersBuilder.cpp"

// Test convertArrayChangeToTotalValueIndex with a range of valid indices
TEST_CASE("holdStrategy", "[holdStrategy]") {
    
    Parameters parameters = Parameters_builder().setup_complex_oneMarket().build();

    holdStrategy(parameters);

    REQUIRE(parameters.outData[0] == 1.0f);
    REQUIRE(parameters.outData[1] == 2.1f);
    REQUIRE(parameters.outData[2] == 4.5f);
    REQUIRE(parameters.outData[3] == 0.0f);
}
