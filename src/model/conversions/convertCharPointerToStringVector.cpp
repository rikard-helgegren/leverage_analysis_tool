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
