import ctypes
import os
import subprocess

from code.model.determine_longest_common_timespan   import determine_longest_common_timespan
import code.model.constants as constants


def harvest_refill_hist_ctypes(self):

    ## C++ interactions ##
    pwd = os.environ['PWD']
    cpp_so_file = pwd + '/code/model/hist_harvest_refill_algo.so'
    lib_object_cpp = ctypes.CDLL(cpp_so_file)

    ## get variables and pass to function ##
    cpp_algorithm = lib_object_cpp.cpp_harvest_refill_algo  # Set upp function call

    # input types and values
    [all_argtypes_list, all_values_list] = get_indata(self)
    cpp_algorithm.argtypes = all_argtypes_list

    # make actual call
    cpp_algorithm(*all_values_list)

    [return_data, size_days_in] = [all_values_list[-1], all_values_list[6]]

    size_return_data = size_days_in - self.years_investigating * constants.MARKET_DAYS_IN_YEAR

    return_data_python_format = [return_data[i] for i in range(size_return_data)]

    return return_data_python_format


# Set up which types are to be sent to cpp
def get_indata(self):
    all_argtypes = []
    all_values = []

    ### loan ###
    all_argtypes.append(ctypes.c_float)
    all_values.append(self.get_loan())


    ### instrument selected ###
    instruments_selected = self.get_instruments_selected()
    names_instruments_selected, leverage_instruments_selected = zip(*instruments_selected)

    # leverage list
    all_argtypes.append(ctypes.c_int * len(instruments_selected))
    all_values.append((ctypes.c_int * len(leverage_instruments_selected))(*leverage_instruments_selected))

    # length of instruments_selected
    all_argtypes.append(ctypes.c_int)
    all_values.append(len(leverage_instruments_selected))

    # names
    all_argtypes.append(ctypes.c_char_p)  # instrument names type
    all_values.append((','.join(names_instruments_selected) + '.').encode())


    ### proportion_funds ###
    all_argtypes.append(ctypes.c_float)
    all_values.append(self.get_proportion_funds())


    ### proportion_leverage ###
    all_argtypes.append(ctypes.c_float)
    all_values.append(self.get_proportion_leverage())


    ### markets_selected ###
    markets_selected = self.get_markets_selected()
    a_instrument = instruments_selected[0]
    market = markets_selected[a_instrument[0]]
    nr_days_in_data = len(market.get_time_span())

    # end pos
    all_argtypes.append(ctypes.c_int)
    all_values.append(nr_days_in_data)

    # number of markets selected
    all_argtypes.append(ctypes.c_int)
    all_values.append(len(markets_selected.keys()))

    # prep variables
    countries = []  # countries
    daily_change = []  # daily change
    for key in markets_selected.keys():
        countries.append(markets_selected[key].get_country())
        current_daily_change = markets_selected[key].get_daily_change()
        daily_change.append((ctypes.c_float * len(current_daily_change))(*current_daily_change))

    # country names
    all_argtypes.append(ctypes.c_char_p)
    all_values.append((','.join(countries)+'.').encode())   # make list to string and encode

    # daily change
    all_argtypes.append(ctypes.POINTER(ctypes.c_float) * len(markets_selected.keys()))
    all_values.append(((ctypes.POINTER(ctypes.c_float) * len(daily_change))(*daily_change)))  # passing list of float pointers

    # index names
    all_argtypes.append(ctypes.c_char_p)
    index_names = markets_selected.keys()
    all_values.append((','.join(index_names)+'.').encode())  # make list to string and encode

    # time horizon days investing
    all_argtypes.append(ctypes.c_int)  # days investing
    all_values.append(self.years_investigating*constants.MARKET_DAYS_IN_YEAR)

    ### Harvest refill limits ###
    all_argtypes.append(ctypes.c_float)
    all_values.append(self.get_harvest_point()/100)  # harvest point not in percent
    all_argtypes.append(ctypes.c_float)
    all_values.append(self.get_refill_point()/100)  # refill point not in percent

    ### Out data ###
    all_argtypes.append(ctypes.c_float * nr_days_in_data)  # out data
    return_data = [0] * nr_days_in_data  # initiate with zeros   # TODO whait should not this be too many? should be - days in intervall. but no?!?
    all_values.append((ctypes.c_float * len(return_data))(*return_data))

    return [all_argtypes, all_values]
