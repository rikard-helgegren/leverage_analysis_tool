#pragma once
#include <string>


class Parameters{

    public:
        float   loan;
        int*    instrumentLeverages;
        int     nrOfInstruments;
        std::vector<std::string>   instrumentNames;
        float   proportionFunds;
        float   proportionLeverage;
        int     totNrDays;
        int     nrMarketsSelected;
        float** marketDailyChanges;
        std::vector<std::string>    indexNames;
        int     daysInvesting;
        float   harvestPoint;
        float   refillPoint;
        int     rebalance_period_months;
        int     strategy;
        int     volatilityStrategieSampleSize;
        int     varianceCalcSampleSize;
        float   volatilityStrategieLevel;
        float*  outData;
        int     numberOfLeveragedInstruments;
        int     numberOfFunds;
        std::map<int, int>        indexToMarket;
};