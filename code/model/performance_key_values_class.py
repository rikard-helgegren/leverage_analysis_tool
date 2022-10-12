import numpy as np
import logging
import code.model.constants as constants

class Performance_Key_values:
    """ A class for all performance parameters for easier access.

        e.g. Mean, median, volatility, beta
    """
    logging.debug("model, Performance_Key_values: __init__")

    def __init__(self, model):

        self.model = model

        self.mean = 0
        self.median = 0
        self.volatility = 0
        self.variance = 0
        self.beta = 0
        self.alpha = 0
        self.severity = 0
        self.percentile_5 = 0
        self.percentile_25 = 0
        self.percentile_50 = 0
        self.percentile_75 = 0
        self.percentile_95 = 0
        self.fees_payed = 0
        self.risk = 0
        self.worst_fall_10_days = 0
        self.worst_fall_30_days = 0
        self.rpi = 0
        self.apr = 0
        self.boiling_band = 0
        self.mac_d = 0
        self.moving_average = 0
        self.mean_inflation_first_index = 0
        self.mean_inflation_all_index = 0
        self.proportion_returns_funds = 0
        self.proportion_returns_leverage = 0
        self.exposure_funds_mean = 0
        self.exposure_leverage_mean = 0
        self.exposure_funds_median = 0
        self.exposure_leverage_median = 0
        self.sharpe_ratio = 0

    def update_values(self, performance_intervals, performance_full_time):
        """Update key values du to changes in the model"""
        logging.debug("model, performance_key_values: update_values")

        #set all key values to default value
        if performance_full_time == []:
            self.mean = 0
            self.median = 0
            self.volatility = 0
            self.variance = 0
            self.beta = 0
            self.alpha = 0
            self.severity = 0
            self.percentile_5 = 0
            self.percentile_25 = 0
            self.percentile_50 = 0
            self.percentile_75 = 0
            self.percentile_95 = 0
            self.fees_payed = 0
            self.risk = 0
            self.worst_fall_10_days = 0
            self.worst_fall_30_days = 0
            self.rpi = 0
            self.apr = 0
            self.boiling_band = 0
            self.mac_d = 0
            self.moving_average = 0
            self.mean_inflation_first_index = 0
            self.mean_inflation_all_index = 0
            self.proportion_returns_funds = 0
            self.proportion_returns_leverage = 0
            self.exposure_funds_mean = 0
            self.exposure_leverage_mean = 0
            self.exposure_funds_median = 0
            self.exposure_leverage_median = 0
            self.sharpe_ratio = 0

        #calculate key values
        else:
            self.variance = round(calc_variance(performance_full_time), 2)
            self.volatility = round(np.sqrt(calc_variance(performance_full_time)), 2)
            self.worst_fall_10_days = round(calc_worst_fall_X_days(performance_full_time, 10), 2)
            self.worst_fall_30_days = round(calc_worst_fall_X_days(performance_full_time, 30), 2)

            if performance_intervals == [] :
                self.mean = 0
                self.median = 0
                self.percentile_5 = 0
                self.percentile_25 = 0
                self.percentile_50 = 0
                self.percentile_75 = 0
                self.percentile_95 = 0
            else:
                self.mean = round(np.mean(performance_intervals), 2)
                self.median = round(np.median(performance_intervals), 2)
                self.percentile_5  = round(np.percentile(performance_intervals, 5), 2)
                self.percentile_25 = round(np.percentile(performance_intervals, 25), 2)
                self.percentile_50 = round(np.percentile(performance_intervals, 50), 2)
                self.percentile_75 = round(np.percentile(performance_intervals, 75), 2)
                self.percentile_95 = round(np.percentile(performance_intervals, 95), 2)
                self.risk = round(calc_risk(performance_intervals),2)  # TODO: should be risk neg returns, risk losing 10%, risk losing 50%

        # TODO: Have not been properly set yet, some wait for larger code implementations
        self.beta = 0
        self.alpha = 0
        self.severity = 0
        self.fees_payed = 0  # needs to be set in calculations
        self.rpi = 0
        self.apr = 0
        self.boiling_band = 0
        self.mac_d = 0
        self.moving_average = 0
        self.mean_inflation_first_index = 0
        self.mean_inflation_all_index = 0
        self.proportion_returns_funds = 0
        self.proportion_returns_leverage = 0
        self.exposure_funds_mean = 0
        self.exposure_leverage_mean = 0
        self.exposure_funds_median = 0
        self.exposure_leverage_median = 0
        self.sharpe_ratio = 0



    ################## Getters and setters ##############

    def get_all_values(self):
        return {"Mean": self.mean,
                "Median": self.median,
                "5th Percentile": self.percentile_5,
                "25th Percentile": self.percentile_25,
                "50th Percentile": self.percentile_50,
                "75th Percentile": self.percentile_75,
                "95th Percentile": self.percentile_95,
                "Volatility": self.volatility,
                "Variance": self.variance,
                "Beta": self.beta,
                "Alpha": self.alpha,
                "Severity": self.severity,
                "Fees Payed": self.fees_payed,
                "Risk": str(self.risk*constants.CONVERT_PERCENT)+"%",
                "Worst fall in 10 days": str(self.worst_fall_10_days*constants.CONVERT_PERCENT)+"%",
                "Worst fall in 30 days": str(self.worst_fall_30_days*constants.CONVERT_PERCENT)+"%",
                "RPI": self.rpi,
                "APR": self.apr,
                "Boiling band": self.boiling_band,
                "macD": self.mac_d,
                "Moving average": self.moving_average,
                "Mean inflation XYZ": self.mean_inflation_first_index,  # TODO fix insertion of index name
                "Mean inflation all indexes": self.mean_inflation_all_index,
                "Returns funds": self.proportion_returns_funds,
                "Returns leverage": self.proportion_returns_leverage,
                "Exposure funds mean": self.exposure_funds_mean,
                "Exposure leverage mean": self.exposure_leverage_mean,
                "Exposure funds median": self.exposure_funds_median,
                "Exposure leverage median": self.exposure_leverage_median,
                "Sharpe_ratio":self.sharpe_ratio}

    def set_mean(self, mean):
        self.mean = mean
    def get_mean(self):
        return self.mean

    def set_median(self, median):
        self.median = median
    def get_median(self):
        return self.median

    def set_volatility(self, volatility):
        self.volatility = volatility
    def get_volatility(self):
        return self.volatility

    def set_variance(self, variance):
        self.variance = variance
    def get_variance(self):
        return self.variance

    def set_beta(self, beta):
        self.beta = beta
    def get_beta(self):
        return self.beta

    def set_alpha(self, alpha):
        self.alpha = alpha
    def get_alpha(self):
        return self.alpha

    def set_severity(self, severity):
        self.severity = severity
    def get_severity(self):
        return self.severity

    def set_percentile_5(self, percentile_5):
        self.percentile_5 = percentile_5
    def get_percentile_5(self):
        return self.percentile_5

    def set_percentile_25(self, percentile_25):
        self.percentile_25 = percentile_25
    def get_percentile_25(self):
        return self.percentile_25

    def set_percentile_50(self, percentile_50):
        self.percentile_50 = percentile_50
    def get_percentile_50(self):
        return self.percentile_50

    def set_percentile_75(self, percentile_75):
        self.percentile_75 = percentile_75
    def get_percentile_75(self):
        return self.percentile_75

    def set_percentile_95(self, percentile_95):
        self.percentile_95 = percentile_95
    def get_percentile_95(self):
        return self.percentile_95

    def set_fees_payed(self, fees_payed):
        self.fees_payed = fees_payed
    def get_fees_payed(self):
        return self.fees_payed

    def set_risk(self, risk):
        self.risk = risk
    def get_risk(self):
        return self.risk

    def set_worst_fall_10_days(self, worst_fall_10_days):
        self.worst_fall_10_days = worst_fall_10_days
    def get_worst_fall_10_days(self):
        return self.worst_fall_10_days

    def set_worst_fall_30_days(self, worst_fall_30_days):
        self.worst_fall_30_days = worst_fall_30_days
    def get_worst_fall_30_days(self):
        return self.worst_fall_30_days

    def set_rpi(self, rpi):
        self.rpi = rpi
    def get_rpi(self):
        return self.rpi

    def set_apr(self, apr):
        self.apr = apr
    def get_apr(self):
        return self.apr

    def set_boiling_band(self, boiling_band):
        self.boiling_band = boiling_band
    def get_boiling_band(self):
        return self.boiling_band

    def set_mac_d(self, mac_d):
        self.mac_d = mac_d
    def get_mac_d(self):
        return self.mac_d

    def set_moving_average(self, moving_average):
        self.moving_average = moving_average
    def get_moving_average(self):
        return self.moving_average

    def set_mean_inflation_first_index(self, mean_inflation_first_index):
        self.mean_inflation_first_index = mean_inflation_first_index
    def get_mean_inflation_first_index(self):
        return self.mean_inflation_first_index

    def set_mean_inflation_all_index(self, mean_inflation_all_index):
        self.mean_inflation_all_index = mean_inflation_all_index

    def get_mean_inflation_all_index(self):
        return self.mean_inflation_all_index

    def set_proportion_returns_funds(self, proportion_returns_funds):
        self.proportion_returns_funds = proportion_returns_funds
    def get_proportion_returns_funds(self):
        return self.proportion_returns_funds

    def set_proportion_returns_leverage(self, proportion_returns_leverage):
        self.proportion_returns_leverage = proportion_returns_leverage
    def get_proportion_returns_leverage(self):
        return self.proportion_returns_leverage

    def set_exposure_funds_mean(self, exposure_funds_mean):
        self.exposure_funds_mean = exposure_funds_mean
    def get_exposure_funds_mean(self):
        return self.exposure_funds_mean

    def set_exposure_leverage_mean(self, exposure_leverage_mean):
        self.exposure_leverage_mean = exposure_leverage_mean
    def get_exposure_leverage_mean(self):
        return self.exposure_leverage_mean

    def set_exposure_funds_mean(self, exposure_funds_mean):
        self.exposure_funds_mean = exposure_funds_mean
    def get_exposure_funds_mean(self):
        return self.exposure_funds_mean

    def set_exposure_leverage_median(self, exposure_leverage_median):
        self.exposure_leverage_median = exposure_leverage_median
    def get_exposure_leverage_median(self):
        return self.exposure_leverage_median
    
    def set_sharpe_ratio(self, sharpe_ratio):
        self.sharpe_ratio = sharpe_ratio
    def get_sharpe_ratio(self):
        return self.sharpe_ratio




def calc_worst_fall_X_days(performance_full_time, x_days):
    """ Calculate the largest loss during a time span of x_days measured in percent.
        A positive loss value is a negative change.
    """
    logging.debug("model, performance_key_values: calc_worst_fall_X_days")
    worst_fall = 0

    for i in range(len(performance_full_time) - x_days):
        this_fall = (performance_full_time[i + x_days] - performance_full_time[i])/(performance_full_time[i]+10**(-10))
        worst_fall = max(worst_fall, this_fall)

    return worst_fall

def calc_variance(performance_full_time):
    """ Calculate the variance* of the full time period"""
    logging.debug("model, performance_key_values: calc_variance")

    # Look att mean values over <mean_size> values # TODO check that this is the right approach
    mean_size = 10
    mean = np.sum(performance_full_time[:mean_size])/mean_size
    sum_total_dif = 0
    elements_to_sum = (len(performance_full_time) - mean_size - 1)
    for i in range(elements_to_sum):
        sum_total_dif += ((performance_full_time[i+mean_size] - mean)/mean)**2  # NOTE: normalized variance

        # Update mean of last of the new group
        mean -= performance_full_time[i]/mean_size  # Remove impact from first value
        mean += performance_full_time[i + mean_size]/mean_size  # Add impact from last value
    if elements_to_sum > 0:
        variance = sum_total_dif/elements_to_sum
    else:
        variance = 1000  # set random large value
    return variance

def calc_risk(performance_intervals):
    """Calculates risk of losing money"""
    
    loses = 0

    for investment_return in performance_intervals:
        if investment_return < 1:
            loses = loses + 1

        risk = loses/len(performance_intervals)

    return risk
