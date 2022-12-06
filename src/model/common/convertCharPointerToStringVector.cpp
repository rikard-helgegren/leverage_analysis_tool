/**
 * Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
 *
 * This software is only allowed for private use. As a private user you are allowed to copy,
 * modify, use, and compile the software. You are NOT however allowed to publish, sell, or
 * distribute this software, either in source code form or as a compiled binary, for any purpose,
 * commercial or non-commercial, by any means.
 */

#include <string>
#include <vector>
#include <sstream>
#include <iterator>

#pragma once

/**
* Converts indata of the format "name1,name2,...,nameN" to string array
* char array must end with .
*/
std::vector<std::string> convertCharPointerToStringVector(char* charPointer ){
    

    std::vector<std::string> vectorStringOut;
    std::string string_var = charPointer;
    std::stringstream strinStream(string_var);

    while (strinStream.good()) {
        std::string substr;
        std::getline(strinStream, substr, ',');
        vectorStringOut.push_back(substr);
    }

    return vectorStringOut;
}
