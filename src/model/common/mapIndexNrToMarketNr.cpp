/**
 * Copyright (C) 2024 Rikard Helgegren <rikard.helgegren@gmail.com>
 *
 * This software is only allowed for private use. As a private user you are allowed to copy,
 * modify, use, and compile the software. You are NOT however allowed to publish, sell, or
 * distribute this software, either in source code form or as a compiled binary, for any purpose,
 * commercial or non-commercial, by any means.
 */

#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <stdexcept>

#pragma once


/**
 * Makes mapping between each financial instrument and its market index
 *
 * key: instrument
 * value: market index
 */
void mapIndexNrToMarketNr(std::map<int,int> indexToMarket,
                          std::vector<std::string> marketNames,
                          int nrMarketsSelected,
                          std::vector<std::string> instrumentNames,
                          int nrOfInstruments){

    for (int instrumentNumber = 0; instrumentNumber < nrOfInstruments; instrumentNumber++){
        for (int number = 0; number < nrMarketsSelected; number++){
            if (marketNames[number] == instrumentNames[instrumentNumber]){
                indexToMarket.insert(std::pair<int, int>(instrumentNumber, number));
            }
        }
    }
}
