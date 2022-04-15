import random
import timeit

#######################################################
###                  Algorithms                     ###
#######################################################

def percentage_change(values):
    changes = []
    for i in range(len(values)-1):
        changes.append((values[i+1]-values[i])/values[i])
    return changes

def naive_calc(list_of_values, leverage, cutoff, values_to_check):
    changes = percentage_change(list_of_values)
    gains = []
    has_appended = False
    for i in range(0, len(list_of_values) - values_to_check):
        value_thus_far = 1
        has_appended = False

        for change in changes[i:i + values_to_check]:
            value_thus_far *= 1 + change*leverage

            if value_thus_far < cutoff:
                gains.append(cutoff)
                has_appended = True
                break

        
        if not has_appended:
            gains.append(value_thus_far)
    
    return gains

def improved_calc(list_of_values, leverage, cutoff, values_to_check):
    changes = percentage_change(list_of_values)
    gains = []
    has_appended = False

    # calc once:
    value_thus_far = 1
    lowest_value = 1
    lowest_value_index = 0
    has_appended = False

    for i, change in enumerate(changes[0:values_to_check]):
        value_thus_far *= 1 + change*leverage
        
        if value_thus_far < lowest_value:
            lowest_value = value_thus_far
            lowest_value_index = i

        if value_thus_far < cutoff:
            gains.append(cutoff)
            has_appended = True
            break
        
    if not has_appended:
        gains.append(value_thus_far)

    for prev_i in range(0, len(list_of_values) - values_to_check - 1):
        has_appended = False

        # move interval to check
        lowest_value /= (1 + changes[prev_i]*leverage)
        value_thus_far /= (1 + changes[prev_i]*leverage)
        value_thus_far *= (1 + changes[prev_i+values_to_check]*leverage)

        if value_thus_far < lowest_value:
            lowest_value = value_thus_far
            lowest_value_index = prev_i + values_to_check

        if lowest_value < cutoff:
            if lowest_value_index <= prev_i:
                # The lowest recorded value is in the past! Need to recalculate a new lowest value.
                lowest_value = value_thus_far
                lowest_value_index = i
                value_thus_far = 1

                for j, change in enumerate(changes[i:i+values_to_check]):
                    value_thus_far *= 1 + change*leverage
                    
                    if value_thus_far < lowest_value:
                        lowest_value = value_thus_far
                        lowest_value_index = i + j
            
            if lowest_value < cutoff:
                gains.append(cutoff)
                has_appended = True

        if not has_appended:
            gains.append(value_thus_far)
        
    return gains

# Tests suggest improved_calc and naive_improved_calc have approximately the same preformance.
# But improved_calc should be theoreticaly faster for the same data set in most cases.
def naive_improved_calc(list_of_values, leverage, cutoff, values_to_check):
    changes = percentage_change(list_of_values)
    gains = []
    has_appended = False

    # calc once:
    value_thus_far = 1
    lowest_value = 1
    has_appended = False

    for i, change in enumerate(changes[0:values_to_check]):
        value_thus_far *= 1 + change*leverage
        
        if value_thus_far < lowest_value:
            lowest_value = value_thus_far

        if value_thus_far < cutoff:
            gains.append(cutoff)
            has_appended = True
            break
        
    if not has_appended:
        gains.append(value_thus_far)

    for prev_i in range(0, len(list_of_values) - values_to_check - 1):
        has_appended = False

        # move interval to check
        lowest_value /= (1 + changes[prev_i]*leverage)
        value_thus_far /= (1 + changes[prev_i]*leverage)
        value_thus_far *= (1 + changes[prev_i+values_to_check]*leverage)

        if value_thus_far < lowest_value:
            lowest_value = value_thus_far

        if lowest_value == 1:
            lowest_value = value_thus_far
            value_thus_far = 1

            for change in changes[i:i+values_to_check]:
                value_thus_far *= 1 + change*leverage
                
                if value_thus_far < lowest_value:
                    lowest_value = value_thus_far
            
        if lowest_value < cutoff:
            gains.append(cutoff)
            has_appended = True

        if not has_appended:
            gains.append(value_thus_far)
        
    return gains

def naive_calc_money(list_of_values, leverage, cutoff, values_to_check, money_to_invest):
    changes = percentage_change(list_of_values)
    gains = []
    has_appended = False
    for i in range(0, len(list_of_values) - values_to_check):
        value_thus_far = 1
        has_appended = False

        for change in changes[i:i + values_to_check]:
            value_thus_far *= 1 + change*leverage

            if value_thus_far < cutoff:
                gains.append(cutoff*money_to_invest)
                has_appended = True
                break

        
        if not has_appended:
            gains.append(value_thus_far*money_to_invest)
    
    return gains

#######################################################
###                     Tests                       ###
#######################################################

def float_eq(a, b, eps):
    return -eps < a - b < eps

def prod(A):
    product = 1
    for a in A:
        product *= a
    return product

def eq_list_float(A, B, eps):
    if len(A) != len(B):
        return False

    for i in range(len(A)):
        if not float_eq(A[i], B[i], eps):
            return False

    return True

def leverage_calc_test():
    test_values = [[1, 1.1, 1.21],
                   [1, 1.1, 0.99],
                   [1, 2, 1, 2, 1],
                   [1, 1.1, 1, 1.1, 1]]
    leverages = [2, 2, 4, 4]
    cutoffs = [0, 0, 0, 0]
    values_to_check = [1, 1, 2, 2]

    expected_value_leverage1 = [[1.1, 1.1], 
                                [1.1, 0.9], 
                                [1, 1, 1],
                                [1, 1, 1]]

    
    expected_value_leverages = [[1.2, 1.2], 
                                [1.2, 0.8], 
                                [0, 0, 0],
                                [(1-(4*0.1/1.1))*1.4, (1-(4*0.1/1.1))*1.4, (1-(4*0.1/1.1))*1.4]]
    
    eps = 0.00001

    # Check naive leverages 1
    for i in range(len(test_values)):
        assert(eq_list_float(
                naive_calc(test_values[i], 1, cutoffs[i], values_to_check[i]),
                expected_value_leverage1[i], eps))

        for value in naive_calc(test_values[i], 1, cutoffs[i], values_to_check[i]):
            assert(value >= cutoffs[i])

        for (j, value) in enumerate(naive_calc(test_values[i], 1, cutoffs[i], values_to_check[i])):
            assert(float_eq(value, cutoffs[i], eps) or 
                   float_eq(value, 
                            prod(list(map(lambda a: 1+a,
                                percentage_change(test_values[i][j:j+values_to_check[i] + 1])))), eps))

    for i in range(len(test_values)):
        assert(eq_list_float(
                naive_calc(test_values[i], leverages[i], cutoffs[i], values_to_check[i]),
                expected_value_leverages[i],
                eps))

    values_to_test = [1]
    n = 1000

    for i in range(n):
        values_to_test.append(1.1)
        values_to_test.append(1)
    
    assert(len(naive_calc(values_to_test, 2, 0, 2*n)) == 1)
    assert(float_eq(
            naive_calc(values_to_test, 2, 0, 2*n)[0], 0, eps))

    for i in range(len(test_values)):
        assert(eq_list_float(
                list(map(lambda a: 1000*a,
                    naive_calc(test_values[i], leverages[i], cutoffs[i], values_to_check[i]))),
                naive_calc_money(test_values[i], leverages[i], cutoffs[i], values_to_check[i], 1000),
                eps))

    for i in range(len(test_values)):
        assert(eq_list_float(
            naive_calc(test_values[i], leverages[i], cutoffs[i], values_to_check[i]),
            improved_calc(test_values[i], leverages[i], cutoffs[i], values_to_check[i]), eps))

    m = 10000 # Days in each "index"
    for i in range(10):
        l = list(map(lambda a: 1+a/(10*m),
                     random.sample(range(1, m*10), m+1)))
        assert(naive_calc(l, 2, 0, m) == improved_calc(l, 2, 0, m))

def calc_preformence_tests():
    print('cutoffs preformance test:')

    SETUP_CODE ='''
import random
from __main__ import naive_calc
from __main__ import improved_calc
from __main__ import naive_improved_calc
n = 10000 # Days in each "index"
days = 3650 # Days to check
l = list(map(lambda a: 1+a/(1000*n),
                random.sample(range(1, n*10), n+1)))
'''

    TEST_CODE1 = 'naive_calc(l, 2, 0, days)'
    TEST_CODE2 = 'improved_calc(l, 2, 0, days)'
    TEST_CODE3 = 'naive_improved_calc(l, 2, 0, days)'

    print('Naive cutoff:')
    naive_time = min(timeit.repeat(setup = SETUP_CODE,
                        stmt = TEST_CODE1,
                        repeat = 100,
                        number = 1))

    print(naive_time)

    print('Improved cutoff:')
    improved_time = min(timeit.repeat(setup = SETUP_CODE,
                        stmt = TEST_CODE2,
                        repeat = 100,
                        number = 1))

    print(improved_time)

    print('Naive Improved cutoff:')
    naive_improved_time = min(timeit.repeat(setup = SETUP_CODE,
                        stmt = TEST_CODE3,
                        repeat = 100,
                        number = 1))

    print("Fractions")
    print(naive_time/improved_time)
    print(naive_time/naive_improved_time)
    print(naive_improved_time/improved_time)

def tests():
    leverage_calc_test()

    #calc_preformence_tests()

if __name__ == '__main__':
    tests()