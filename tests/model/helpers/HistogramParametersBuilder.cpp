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
#include "../../../src/model/histogram/HistogramParameters.cpp"


class Histogram_Parameters_Builder{

    private:
        HistogramParameters histogramParameters;

    public:
        Histogram_Parameters_Builder(){
            this->histogramParameters.isSet = true;
            this->histogramParameters.daysInvesting = 1;
        }

        Histogram_Parameters_Builder setIsSet(bool isSet){
            this->histogramParameters.isSet = isSet;
            return *this;
        }

        Histogram_Parameters_Builder setDaysInvesting(int daysInvesting){
            this->histogramParameters.daysInvesting = daysInvesting;
            return *this;
        }

        HistogramParameters build(){
            return this->histogramParameters;
        }
};
