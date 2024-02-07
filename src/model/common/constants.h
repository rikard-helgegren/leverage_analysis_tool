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

    const float fee_bull_2_to_4 = 0.00001f;  // 0.01% each day
    const float fee_bull_5_and_more = 0.00002f;  // 0.02% each day

    const float fee_bull_1 = 0.002f / static_cast<float>(market_days_in_year); // 0.2% each year
    const float fee_bull_2 = 0.0101f / static_cast<float>(market_days_in_year); // 1.01% each year
    const float fee_bull_3 = 0.0203f / static_cast<float>(market_days_in_year); // 2.03% each year
    const float fee_bull_4 = 0.0305f / static_cast<float>(market_days_in_year); // 3.05% each year
    const float fee_bull_5 = 0.0614f / static_cast<float>(market_days_in_year); // 6.14% each year
    const float fee_bull_6 = 0.0f; // no data
    const float fee_bull_7 = 0.0f; // no data
    const float fee_bull_8 = 0.2189f / static_cast<float>(market_days_in_year); // 21.89% each year
    const float fee_bull_9 = 0.0f; // no data
    const float fee_bull_10 = 0.2865f / static_cast<float>(market_days_in_year); // 28.65% each year
   
    const float spread = 1.0f; // No spread at Avanza (1% spread would result in const being 1.01)
    const float spread_bull_1 = 1.0f;
    const float spread_bull_2 = 1.002f;
    const float spread_bull_3 = 1.003f;
    const float spread_bull_4 = 1.004f;
    const float spread_bull_5 = 1.0052f;
    const float spread_bull_6 = 0.0f; // no data
    const float spread_bull_7 = 0.0f; // no data
    const float spread_bull_8 = 1.0112f;
    const float spread_bull_9 = 0.0f; // no data
    const float spread_bull_10 = 1.015f;




    std::string portfolio_strategies[5] = {"Hold", "Harvest/Refill", "Rebalance Time", "Do not invest", "Variance Dependent"};

    const int convert_percent = 100;
    const int highest_leverage_available = 5;
}

#endif
