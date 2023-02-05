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
#include "../../../src/model/common/convertCharPointerToStringVector.cpp"

#include <string>
#include <vector>


// Test convertArrayChangeToTotalValueIndex with a range of valid indices
TEST_CASE("convertCharPointerToStringVector", "[convertArrayChangeToTotalValueSize]") {
    char charPointer[8] = "abc,efg";

    std::vector<std::string> vectorString;
    vectorString.push_back("abc");
    vectorString.push_back("efg");
    
    REQUIRE(typeid(convertCharPointerToStringVector(charPointer)) == typeid(vectorString));
    REQUIRE(vectorString == convertCharPointerToStringVector(charPointer));
}
