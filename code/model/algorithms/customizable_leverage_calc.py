import enum
import random
import timeit

class Investment_state:
    def __init__(self, leverage, money_to_invest):
        self.leverage = leverage

        self.starting_money = money_to_invest
        self.current_money = money_to_invest
        self.peak_money = money_to_invest
        self.lowest_money = money_to_invest
        self.total_money_invested = money_to_invest
        self.total_money_withdrawn = 0

        self.latest_change = 0

    def update(self, new_change):
        self.latest_change = new_change
        self.current_money *= 1 + new_change*self.leverage
        self.update_money_parameters()

    def update_money_parameters(self):
        if self.current_money < self.lowest_money:
            self.lowest_money = self.current_money
        elif self.current_money > self.peak_money:
            self.peak_money = self.current_money

    def invest(self, amount):
        self.current_money += amount
        self.total_money_invested += amount
        self.update_money_parameters()

    def withdraw(self, amount):
        self.current_money -= amount
        self.total_money_withdrawn += amount
        self.update_money_parameters()

class Investment_decissions(enum.Enum):
    Do_nothing = 0
    Invest = 1
    Withdraw = 2
    Withdraw_all_and_stop_traiding = 3

class Investment_Strategy:
    def make_decission(self, Investment_state):
        return (Investment_decissions.Do_nothing, 0)

    def copy(self):
        return Investment_Strategy()

class Cutoff_strategy(Investment_Strategy):
    def __init__(self, cutoff):
        self.cutoff = cutoff

    def make_decission(self, Investment_state):
        if Investment_state.current_money < self.cutoff * Investment_state.starting_money:
            return (Investment_decissions.Withdraw_all_and_stop_traiding, 0)        
        return (Investment_decissions.Do_nothing, 0)

    def copy(self):
        return Cutoff_strategy(self.cutoff)

class Balance_strategy(Investment_Strategy):
    def make_decission(self, Investment_state):
        if Investment_state.current_money < Investment_state.starting_money/2:
            return (Investment_decissions.Invest, Investment_state.starting_money/2)
        elif Investment_state.current_money > Investment_state.starting_money*3/2:
            return (Investment_decissions.Withdraw, Investment_state.starting_money/2)
        return (Investment_decissions.Do_nothing, 0)

    def copy(self):
        return Balance_strategy()

class Scared_strategy(Investment_Strategy):
    def make_decission(self, Investment_state):
        if Investment_state.latest_change < -0.50:
            return (Investment_decissions.Withdraw_all_and_stop_traiding, 0)
        return (Investment_decissions.Do_nothing, 0)

    def copy(self):
        return Scared_strategy()

class Cashout_strategy(Investment_Strategy):
    def make_decission(self, Investment_state):
        if Investment_state.latest_change > 0.50:
            return (Investment_decissions.Withdraw_all_and_stop_traiding, 0)
        return (Investment_decissions.Do_nothing, 0)

    def copy(self):
        return Cashout_strategy()

class Diamond_hands_strategy(Investment_Strategy):
    def make_decission(self, Investment_state):
        return (Investment_decissions.Do_nothing, 0)

    def copy(self):
        return Diamond_hands_strategy()


#######################################################
###                  Algorithms                     ###
#######################################################

# Copied from leverage_calc.py
def percentage_change(values):
    changes = []
    for i in range(len(values)-1):
        changes.append((values[i+1]-values[i])/values[i])
    return changes


def naive_calc_money_with_strategy(list_of_values, leverage, cutoff, values_to_check, money_to_invest, strategy_to_test):
    changes = percentage_change(list_of_values)
    gains = []
    has_appended = False
    for i in range(0, len(list_of_values) - values_to_check):
        state = Investment_state(leverage, money_to_invest)
        strategy = strategy_to_test.copy()
        value_thus_far = 1
        has_appended = False

        for change in changes[i:i + values_to_check]:
            state.update(change)
            value_thus_far *= 1 + change*leverage

            (decission, amount) = strategy.make_decission(state)
            if decission == Investment_decissions.Invest:
                state.invest(amount)
            elif decission == Investment_decissions.Withdraw:
                state.withdraw(amount)
            elif decission == Investment_decissions.Withdraw_all_and_stop_traiding:
                gains.append(state.current_money)
                has_appended = True
                break

        if not has_appended:
            gains.append(state.current_money)
    
    return gains

#######################################################
###                     Tests                       ###
#######################################################

############### Copied from leverage_calc for testing porposes.

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

############### Copy from leverage_calc for testing porposes over.

def customizable_leverage_calc_tests():
    
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
    
    money_to_invest = [1, 10, 100, 1000]

    eps = 0.00001

    for i in range(len(test_values)):
        with_strategy = naive_calc_money_with_strategy(test_values[i], leverages[i], cutoffs[i], 
                                                       values_to_check[i], money_to_invest[i], Cutoff_strategy(0))
        naive_cutoff = naive_calc_money(test_values[i], leverages[i], cutoffs[i], 
                                    values_to_check[i], money_to_invest[i])
        assert(len(with_strategy) ==
               len(naive_cutoff))
        if min(with_strategy) > 0:
            assert(eq_list_float(
                with_strategy,
                naive_cutoff,
                eps
            ))

    m = 1000 # Days in each "index"
    for i in range(10):
        l = list(map(lambda a: 1+a/(10*m),
                     random.sample(range(1, m*10), m+1)))
        assert(eq_list_float(
            naive_calc_money_with_strategy(l, 2, 0, 365, 10000, Cutoff_strategy(0)),
            naive_calc_money(l, 2, 0, 365, 10000),
            eps
        ))


def calc_preformence_tests():
    print('cutoffs preformance test:')

    SETUP_CODE ='''
import random
from __main__ import naive_calc_money_with_strategy
from __main__ import naive_calc_money
from __main__ import Cutoff_strategy
n = 10000 # Days in each "index"
days = 3650 # Days to check
l = list(map(lambda a: 1+a/(1000*n),
                random.sample(range(1, n*10), n+1)))
'''

    TEST_CODE1 = 'naive_calc_money_with_strategy(l, 2, 0, days, 10000, Cutoff_strategy(0))'
    TEST_CODE2 = 'naive_calc_money(l, 2, 0, days, 10000)'

    print('Strategy cutoff:')
    naive_time = min(timeit.repeat(setup = SETUP_CODE,
                        stmt = TEST_CODE1,
                        repeat = 100,
                        number = 1))

    print(naive_time)

    print('Hard coded naive cutoff:')
    improved_time = min(timeit.repeat(setup = SETUP_CODE,
                        stmt = TEST_CODE2,
                        repeat = 100,
                        number = 1))

    print(improved_time)

    print("Fractions")
    print(naive_time/improved_time)


def tests():
    customizable_leverage_calc_tests()

    calc_preformence_tests()

if __name__ == '__main__':
    tests()