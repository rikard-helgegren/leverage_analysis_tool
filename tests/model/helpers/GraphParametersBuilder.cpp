/**
 * Copyright (C) 2024 Rikard Helgegren <rikard.helgegren@gmail.com>
 *
 * This software is only allowed for private use. As a private user you are allowed to copy,
 * modify, use, and compile the software. You are NOT however allowed to publish, sell, or
 * distribute this software, either in source code form or as a compiled binary, for any purpose,
 * commercial or non-commercial, by any means.
 */


#pragma once
#include <string>
#include "../../../src/model/graph/GraphParameters.cpp"


class Graph_Parameters_Builder{

    private:
        GraphParameters graphParameters;

    public:
        Graph_Parameters_Builder(){
            this->graphParameters.isSet = true;
            this->graphParameters.positionCounter = 0;
            this->graphParameters.transactionDates = new int[10];
            this->graphParameters.transactionTypes = new int[10];
        }

        Graph_Parameters_Builder setIsSet(bool isSet){
            this->graphParameters.isSet = isSet;
            return *this;
        }

        Graph_Parameters_Builder setPositionCounter(int positionCounter){
            this->graphParameters.positionCounter = positionCounter;
            return *this;
        }

        Graph_Parameters_Builder setTransactionDates(int* transactionDates){
            this->graphParameters.transactionDates = transactionDates;
            return *this;
        }

        Graph_Parameters_Builder setTransactionTypes(int* transactionTypes){
            this->graphParameters.transactionTypes = transactionTypes;
            return *this;
        }

        GraphParameters build(){
            return this->graphParameters;
        }
};
