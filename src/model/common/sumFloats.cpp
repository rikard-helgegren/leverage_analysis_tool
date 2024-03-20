/**
 * Copyright (C) 2024 Rikard Helgegren <rikard.helgegren@gmail.com>
 *
 * This software is only allowed for private use. As a private user you are allowed to copy,
 * modify, use, and compile the software. You are NOT however allowed to publish, sell, or
 * distribute this software, either in source code form or as a compiled binary, for any purpose,
 * commercial or non-commercial, by any means.
 */

#pragma once

#include "../../Logger.cpp"

float sumFloats(float* floatArray, int nbrOfFloats){
    //static Logger logger;
    float sum = 0.0f;

    for (int i = 0; i < nbrOfFloats; i++){
        sum = sum + floatArray[i];
    }

    return sum;
}
