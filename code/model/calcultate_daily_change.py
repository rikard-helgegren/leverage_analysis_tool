
def calcultate_daily_change(markets_dict):

    for market in markets_dict.values():

        market_values = market.get_values()

        daily_change = []

        #Calculate change in index value since last input
        for i, value in enumerate(market_values[1:]):
            change = (value-market_values[i])/market_values[i]
            daily_change.append(change)
        
        market.set_daily_change(daily_change)

    return markets_dict
