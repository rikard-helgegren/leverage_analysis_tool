import os
import sys

################ Files ################

data_files_path = "data/raw_data/all"
program_folder = os.path.dirname(os.path.realpath(sys.argv[0]))
hist_harvest_refill_algo_file = '/src/compiled_code/calculateHistogramOutput.so'

############### MODEL VALUES #################

DEFULT_LOAN                                 = 0
DEFULT_YEARS_HISTOGRAM_INTERVAL             = 1
DEFULT_HARVEST_POINT                        = 150  # percentage
DEFULT_REFILL_POINT                         = 50  # percentage
DEFULT_REBALANCE_PERIOD_MONTHS              = 6 # months
DEFULT_UPDATE_HARVEST_REFILL                = 0
DEFULT_PROPORTION_CASH                      = 0
DEFULT_PROPORTION_FUNDS                     = 0.9
DEFULT_PROPORTION_LEVERAGE                  = 1 - DEFULT_PROPORTION_FUNDS
DEFULT_INCLUDE_FEES_STATUS                  = True
DEFULT_REBALANCE_STATUS                     = False
DEFULT_REBALANCE_BETWEEN_INSTRUMENTS_STATUS = False
DEFULT_CORRECTION_OF_INFLATION_STATUS       = True
DEFULT_CORRECTION_OF_CURRENCY_STATUS        = True
DEFULT_DELAY_OF_CORRECTION                  = 0

# TODO fine tune, what are usable values
DEFULT_VARIANCE_SAMPLE_SIZE = 10
DEFULT_VOLATILITY_STRATEGIE_SAMPLE_SIZE = 50 
DEFULT_VOLATILITY_STRATEGIE_LEVEL = 0.01 # Need to try what is resonable


PORTFOLIO_STRATEGIES = ["Hold", "Harvest/Refill", "Rebalance Time", "Do not invest", "Variance Dependent"]  # Should match view
HIGHEST_LEVERAGE_AVAILABLE = 5

############## VARIOUS CONSTANTS ##############

MARKET_DAYS_IN_YEAR = 270  # 270 is not true for all markets but close if the union is considered
MONTHS_IN_YEAR = 12

FEE_BULL_1 = 0.002/MARKET_DAYS_IN_YEAR  # 0.2% each year
FEE_BULL_2_TO_4 = 0.00001  # 0.01% each day
FEE_BULL_5_AND_MORE = 0.00002  # 0.02% each day

CONVERT_PERCENT = 100


