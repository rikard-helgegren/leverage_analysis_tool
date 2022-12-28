#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import numpy as np
from src.model.common.variance_and_volatility import calc_variance
from src.model.common.variance_and_volatility import calc_least_square_fit

def test_calc_variance():
    # Test with a small sample size and no variance
    performance_full_time = [1, 1, 1, 1, 1]
    sample_size = 2
    expected_variance = 0
    variance = calc_variance(performance_full_time, sample_size)
    assert variance == expected_variance, f'Error: expected {expected_variance}, got {variance}'

    # Test with a larger sample size and no variance
    performance_full_time = [1, 1, 1, 1, 1, 1, 1, 1]
    sample_size = 4
    expected_variance = 0
    variance = calc_variance(performance_full_time, sample_size)
    assert variance == expected_variance, f'Error: expected {expected_variance}, got {variance}'
    
    # Test with a small sample size and no variance with regards to linear fit
    performance_full_time = [1, 2, 3, 4, 5]
    sample_size = 2
    expected_variance = 0
    variance = calc_variance(performance_full_time, sample_size)
    assert variance == expected_variance, f'Error: expected {expected_variance}, got {variance}'

    # Test with a larger sample size and no variance with regards to linear fit
    performance_full_time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    sample_size = 4
    expected_variance = 0
    variance = calc_variance(performance_full_time, sample_size)
    assert variance == expected_variance, f'Error: expected {expected_variance}, got {variance}'

    # Test with a small sample size with variance
    performance_full_time = [1, 0, 1, 0, 1, 0, 1]
    sample_size = 3
    expected_variance = 1.875
    variance = calc_variance(performance_full_time, sample_size)
    assert np.round(variance,4) == expected_variance, f'Error: expected {expected_variance}, got {variance}'

    # Test with a larger sample size and high variance
    performance_full_time = [100, 0, 100, 0, 100, 0, 100, 0, 100, 0,]
    sample_size = 4
    expected_variance = 1.4375
    variance = calc_variance(performance_full_time, sample_size)
    assert np.round(variance,4) == expected_variance, f'Error: expected {expected_variance}, got {variance}'

    # Test with a small sample size and only 1 value
    performance_full_time = [1]
    sample_size = 1
    expected_variance = 1000
    variance = calc_variance(performance_full_time, sample_size)
    assert variance == expected_variance, f'Error: expected {expected_variance}, got {variance}'


def test_calc_least_square_fit():
    
    # Test const data
    value_data = [1 ,1 ,1 ,1]
    expected_fit = [1 ,1 ,1 ,1]
    fit_line_for_data = calc_least_square_fit(value_data)
    assert fit_line_for_data == expected_fit,  f'Error: expected {expected_fit}, got {fit_line_for_data}'

    # Test linear data
    value_data = [1 ,2 ,3 ,4]
    expected_fit = [1 ,2 ,3 ,4]
    fit_line_for_data = calc_least_square_fit(value_data)
    assert fit_line_for_data == expected_fit,  f'Error: expected {expected_fit}, got {fit_line_for_data}'

    # Test best fit to non linear data
    value_data = [1 ,0 ,0 ,1]
    expected_fit = [0.5 ,0.5 ,0.5 ,0.5]
    fit_line_for_data = calc_least_square_fit(value_data)
    assert fit_line_for_data == expected_fit,  f'Error: expected {expected_fit}, got {fit_line_for_data}'
