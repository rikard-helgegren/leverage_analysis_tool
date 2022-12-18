/**
 * Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
 *
 * This software is only allowed for private use. As a private user you are allowed to copy,
 * modify, use, and compile the software. You are NOT however allowed to publish, sell, or
 * distribute this software, either in source code form or as a compiled binary, for any purpose,
 * commercial or non-commercial, by any means.
 */


#if !defined(MYLIB_CONSTANTS_H)
#define MYLIB_CONSTANTS_H 1

namespace constants{

    const int market_days_in_year = 270;  // 270 is not true for all markets but close if the union is considered
    const int months_in_year = 12;

    const float fee_bull_1 = 0.002/static_cast<float>(market_days_in_year); //  0.2% each year
    const float fee_bull_2_to_4 = 0.00001f;  // 0.01% each day
    const float fee_bull_5_and_more = 0.00002f;  // 0.02% each day

    const float spread = 1.00f; //No spread at Avanza (1% spread would result in const beeing 1.01)

    std::string portfolio_strategies[5] = {"Hold", "Harvest/Refill", "Rebalance Time", "Do not invest", "Variance Dependent"};

    const int convert_percent = 100;
    const int highest_leverage_available = 5;
}

#endif
