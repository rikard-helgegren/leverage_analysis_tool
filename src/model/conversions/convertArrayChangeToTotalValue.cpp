#pragma once

/**
 * Convert the daily change to the values the investment would have at that day, using array indexes
 */
void convertArrayChangeToTotalValueIndex(float* changeValues,
                                           int from_index,
                                           int to_index,
                                           float* totalValueList){
    
    // First instance has no previous value
    totalValueList[0] = 1;

    for (int i = 1; i < to_index-from_index; i++) {
        totalValueList[i] = totalValueList[i-1] * ( 1 + changeValues[from_index+i]);
    }

}

/**
 * Convert the daily change to the values the investment would have at that day, using array size
*/
void  convertArrayChangeToTotalValueSize(float* changeValues,
                                           int size,
                                           float* totalValueList){
    convertArrayChangeToTotalValueIndex(changeValues, 0, size-1, totalValueList);
}

