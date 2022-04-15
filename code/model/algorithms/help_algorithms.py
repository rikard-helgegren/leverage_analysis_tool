import timeit

class List_node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def get_next(self):
        return self.next

    def set_next(self, next):
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None

    def get_head(self):
        return self.head

    def add_first(self, node):
        temp_node = self.head
        self.head = node
        self.head.set_next(temp_node)

    def add_first_data(self, data):
        self.add_first(List_node(data))

    def drop_first(self):
        self.head = self.head.next

def linked_list_to_string(linked_list):
    node = linked_list.head
    string = ''
    while node != None:
        string += str(node.data)
        string += '-'
        node = node.next
    string += 'None'
    return string

def print_linked_list(linked_list):
    print(linked_list_to_string(linked_list))

def gen_linked_list_of_ints(n):
    linked_list = LinkedList()
    start_node = List_node(0)
    node = start_node
    index = 0
    while n > index + 1:
        node.next = List_node(index+1)
        node = node.next
        index += 1
    linked_list.head = start_node
    return linked_list

def list_to_linked_list(list_to_convert):
    if len(list_to_convert) == 0:
        return LinkedList()
    start_node = List_node(list_to_convert[0])
    node = start_node
    for i in range(1, len(list_to_convert)):
        node.next = List_node(list_to_convert[i])
        node = node.next
    linked_list = LinkedList()
    linked_list.head = start_node
    return linked_list

def length_linked_list(linked_list):
    node = linked_list.head
    n = 0
    while node != None:
        n += 1
        node = node.next
    return n

def naive_linked_list_to_list(linked_list):
    temp_list = [None] * length_linked_list(linked_list)
    node = linked_list.head
    index = 0
    while node != None:
        temp_list[index] = node.data
        node = node.next
        index += 1
    return temp_list

# This one is faster
def linked_list_to_list(linked_list):
    temp_list = []
    node = linked_list.head
    while node != None:
        temp_list.append(node.data)
        node = node.next
    return temp_list

#######################################################
###                  Algorithms                     ###
#######################################################

def find_latest_first(lists_of_indexes):
    return max([min(x) for x in lists_of_indexes])

def find_Earliest_last(lists_of_indexes):
    return min([max(x) for x in lists_of_indexes])

def fix_gaps(lists_of_indexes):
    return fix_gaps2(lists_of_indexes, find_latest_first(lists_of_indexes), find_Earliest_last(lists_of_indexes))

def fix_gaps2(lists_of_indexes, latest_first, earliest_last):
    master_node = List_node() # Dummy node
    previous_node = master_node
    current_node = None

    # Create master_index_list
    for list_of_indexes in lists_of_indexes:
        i = 0
        while i < len(list_of_indexes):
            index = list_of_indexes[i]

            if list_of_indexes[i] < latest_first or list_of_indexes[i] > earliest_last:
                i += 1

            # first node, or out of data
            elif current_node == None:
                current_node = List_node(index)
                previous_node.next = current_node
                previous_node = current_node
                current_node = previous_node.next
                i += 1

            # insert index
            elif current_node.data > index:
                previous_node.next = List_node(index)
                previous_node = previous_node.next
                previous_node.next = current_node
                i += 1

            # index is later than current_node
            elif current_node.data < index:
                previous_node = current_node
                current_node = previous_node.next

            # index already exist in the linked_list
            else:
                previous_node = current_node
                current_node = previous_node.next
                i += 1

        previous_node = master_node
        current_node = master_node.next

    master_index_list = LinkedList()
    master_index_list.head = master_node.next
    return master_index_list

def find_first_index_less_than(search_list, less_than):
    i = 0
    while i < len(search_list) and search_list[i] < less_than:
        i += 1
    return i - 1

def naive_fix_gaps(lists_of_indexes):
    master_list = []
    for list_of_indexes in lists_of_indexes:
        for index in list_of_indexes:
            if index not in master_list:
                master_list.insert(find_first_index_less_than(master_list, index)+1, index)
    return master_list

def fill_gaps_data(lists_to_fill, lists_of_values):
    latest_first = find_latest_first(lists_to_fill)
    earliest_last = find_Earliest_last(lists_to_fill)
    master_linked_list = fix_gaps2(lists_to_fill, latest_first, earliest_last)
    node = master_linked_list.head
    master_lists_of_values = []

    for (list_to_fill, list_of_values) in zip(lists_to_fill, lists_of_values):
        i = 0
        value_list = []
        while node != None:

            if i == len(list_to_fill):
                value_list.append(list_of_values[i-1])
                node = node.next

            # if list_to_fill[i] > earliest_last then node != None by the construction of master_linked_list
            elif list_to_fill[i] < latest_first:
                i += 1

            elif list_to_fill[i] == node.data:
                value_list.append(list_of_values[i])
                node = node.next
                i += 1

            # Here we know node.data < list_to_fill[i] and we don't want to increase i
            # Here i != 0 since then latest_first < node.data < list_to_fill[0], which is impossible
            else:
                value_list.append(list_of_values[i-1])
                node = node.next
        master_lists_of_values.append(value_list)
        node = master_linked_list.head
    
    master_list = linked_list_to_list(master_linked_list)
    return ([master_list]*len(lists_to_fill), master_lists_of_values)

def fix_gaps_cmp(lists_of_indexes, cmp):
    return fix_gaps2_cmp(lists_of_indexes, find_latest_first(lists_of_indexes), find_Earliest_last(lists_of_indexes), cmp)

def fix_gaps2_cmp(lists_of_indexes, latest_first, earliest_last, cmp):
    master_node = List_node() # Dummy node
    previous_node = master_node
    current_node = None

    # Create master_index_list
    for list_of_indexes in lists_of_indexes:
        i = 0
        while i < len(list_of_indexes):
            index = list_of_indexes[i]

            if cmp(index, latest_first) < 0 or cmp(index, earliest_last) > 0:
                i += 1

            # first node, or out of data
            elif current_node == None:
                current_node = List_node(index)
                previous_node.next = current_node
                previous_node = current_node
                current_node = previous_node.next
                i += 1

            # insert index
            elif cmp(current_node.data, index) > 0:
                previous_node.next = List_node(index)
                previous_node = previous_node.next
                previous_node.next = current_node
                i += 1

            # index is later than current_node
            elif cmp(current_node.data, index) < 0:
                previous_node = current_node
                current_node = previous_node.next

            # index already exist in the linked_list
            else:
                previous_node = current_node
                current_node = previous_node.next
                i += 1

        previous_node = master_node
        current_node = master_node.next

    master_index_list = LinkedList()
    master_index_list.head = master_node.next
    return master_index_list

def fill_gaps_data_cmp(lists_to_fill, lists_of_values, cmp):
    latest_first = find_latest_first(lists_to_fill)
    earliest_last = find_Earliest_last(lists_to_fill)
    master_linked_list = fix_gaps2_cmp(lists_to_fill, latest_first, earliest_last, cmp)
    node = master_linked_list.head
    master_lists_of_values = []

    for (list_to_fill, list_of_values) in zip(lists_to_fill, lists_of_values):
        i = 0
        value_list = []
        while node != None:

            if i == len(list_to_fill):
                value_list.append(list_of_values[i-1])
                node = node.next

            # if list_to_fill[i] > earliest_last then node != None by the construction of master_linked_list
            elif cmp(list_to_fill[i], latest_first) < 0:
                i += 1

            elif cmp(list_to_fill[i], node.data) == 0:
                value_list.append(list_of_values[i])
                node = node.next
                i += 1

            # Here we know node.data < list_to_fill[i] and we don't want to increase i
            # Here i != 0 since then latest_first < node.data < list_to_fill[0], which is impossible
            else:
                value_list.append(list_of_values[i-1])
                node = node.next
        master_lists_of_values.append(value_list)
        node = master_linked_list.head
    
    master_list = linked_list_to_list(master_linked_list)
    return ([master_list]*len(lists_to_fill), master_lists_of_values)



#######################################################
###                     Tests                       ###
#######################################################


def node_test():
    # Test constructor and get_data
    node = List_node()
    assert(node.data == None)
    assert(node.get_data() == None)

    node = List_node('Test')
    assert(node.data == 'Test')
    assert(node.get_data() == 'Test')

    # Test set_data
    node.set_data('Other Test')
    assert(node.get_data() == 'Other Test')

    # Test next and set_next
    node2 = List_node(1)
    node.set_next(node2)
    assert(node.get_data() == 'Other Test')
    assert(node.get_next().get_data() == 1)
    assert(node.get_next().get_next() == None)

def list_test():
    list1 = LinkedList()
    assert(list1.head == None)
    assert(list1.get_head() == None)

    list1.add_first_data('Test')
    assert(list1.get_head().data == 'Test')
    assert(list1.get_head().next == None)

    list1.add_first(List_node('Other Text'))
    assert(list1.get_head().data == 'Other Text')
    assert(list1.get_head().next.data == 'Test')
    assert(list1.get_head().next.next == None)
    assert(length_linked_list(list1) == 2)

    list1.drop_first()
    assert(list1.get_head().data == 'Test')
    assert(list1.get_head().next == None)
    assert(length_linked_list(list1) == 1)



def print_linked_list_test():
    linked_list = LinkedList()
    linked_list.add_first_data(3)
    linked_list.add_first_data(2)
    linked_list.add_first_data(1)
    assert(linked_list_to_string(linked_list) == '1-2-3-None')

    assert(linked_list_to_string(gen_linked_list_of_ints(10)) == '0-1-2-3-4-5-6-7-8-9-None')
    assert(linked_list_to_string(list_to_linked_list([1, 2, 3, 4])) == '1-2-3-4-None')
    assert(linked_list_to_string(list_to_linked_list([1, 2, 4])) == '1-2-4-None')
    assert(linked_list_to_string(list_to_linked_list([1, 2, 5, 7, 11, 12])) == '1-2-5-7-11-12-None')

    assert(length_linked_list(gen_linked_list_of_ints(10)) == 10)
    assert(length_linked_list(list_to_linked_list([1, 2, 3, 4])) == 4)
    assert(length_linked_list(list_to_linked_list([1, 2, 4]) ) == 3)
    assert(length_linked_list(list_to_linked_list([1, 2, 5, 7, 11, 12])) == 6)

    Lists_for_test = [[1, 2, 3], [1, 2, 4, 6, 8], [1, 7, 234, 345, 35, 5]]
    for l in Lists_for_test:
        assert(l == linked_list_to_list(list_to_linked_list(l)))
        assert(l == naive_linked_list_to_list(list_to_linked_list(l)))

def fix_gaps_test():
    list_of_lists_to_fill = [[[1, 2, 5, 6, 7, 10], [1, 2, 3, 4, 7, 8, 9]], [[1, 2, 5], [1, 2, 7, 8, 9], [1, 3, 4, 6, 7, 10]], [[1, 2], [1, 2, 7, 9], [1, 4, 6, 7, 10]]]

    assert(find_latest_first(list_of_lists_to_fill[0]) == 1)
    assert(find_latest_first(list_of_lists_to_fill[1]) == 1)
    assert(find_latest_first(list_of_lists_to_fill[2]) == 1)

    assert(find_Earliest_last(list_of_lists_to_fill[0]) == 9)
    assert(find_Earliest_last(list_of_lists_to_fill[1]) == 5)
    assert(find_Earliest_last(list_of_lists_to_fill[2]) == 2)

    assert(linked_list_to_string(fix_gaps(list_of_lists_to_fill[0])) == '1-2-3-4-5-6-7-8-9-None')
    assert(linked_list_to_string(fix_gaps(list_of_lists_to_fill[1])) == '1-2-3-4-5-None')
    assert(linked_list_to_string(fix_gaps(list_of_lists_to_fill[2])) == '1-2-None')

    for lists_to_fill in list_of_lists_to_fill:
        assert(linked_list_to_list(fix_gaps(lists_to_fill)) == 
               naive_fix_gaps([[i for i in list_to_fill
                    if find_latest_first(lists_to_fill) <= i <= find_Earliest_last(lists_to_fill)] for list_to_fill in lists_to_fill]))
        assert(linked_list_to_list(fix_gaps(lists_to_fill)) == 
               linked_list_to_list(fix_gaps_cmp(lists_to_fill, lambda x, y: x - y)))

    list_of_lists_to_fill2 = [[[1, 2, 3, 6], [1, 2, 4, 8]],
                              [[1, 3, 5, 6, 8], [1, 3, 6, 8, 9], [1, 7, 9]],
                              [[1, 2], [1, 2]],
                              [[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5]]]
    list_of_lists_of_data = [[[1, 2, 3, 6], [1, 2, 4, 8]],
                             [[1, 2, 3, 4, 5], [6, 7, 8, 9, 0], [1, 2, 3]],
                             [[1, 2], [3, 4]],
                             [[1, 4, 2, 5, 7, 2, 7, 9, 4], [1, 5, 7, 4, 2]]]
    list_of_expected_output = [([[1, 2, 3, 4, 6], [1, 2, 3, 4, 6]], [[1, 2, 3, 3, 6], [1, 2, 2, 4, 4]]),
                              ([[1, 3, 5, 6, 7, 8], [1, 3, 5, 6, 7, 8], [1, 3, 5, 6, 7, 8]], [[1, 2, 3, 4, 4, 5], [6, 7, 7, 8, 8, 9], [1, 1, 1, 1, 2, 2]]),
                              ([[1, 2], [1, 2]], [[1, 2], [3, 4]]),
                              ([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]], [[1, 4, 2, 5, 7], [1, 5, 7, 4, 2]])]

    for i in range(len(list_of_expected_output)):
        assert(fill_gaps_data(list_of_lists_to_fill2[i], list_of_lists_of_data[i]) == 
               list_of_expected_output[i])
        assert(fill_gaps_data(list_of_lists_to_fill2[i], list_of_lists_of_data[i]) == 
               fill_gaps_data_cmp(list_of_lists_to_fill2[i], list_of_lists_of_data[i], lambda x, y: x - y))


import random

def list_to_linked_list_preformence_test():
    print('Naive linked list to list test:')

    SETUP_CODE ='''
import numpy.random as nprnd
from __main__ import linked_list_to_list
from __main__ import list_to_linked_list
from __main__ import naive_linked_list_to_list
l = nprnd.randint(1000, size=100000)
l = list_to_linked_list(l)
'''

    TEST_CODE1 = 'linked_list_to_list(l)'
    TEST_CODE2 = 'naive_linked_list_to_list(l)'
    print('Ordinary linked_list_to_list:')
    print(min(timeit.repeat(setup = SETUP_CODE,
                        stmt = TEST_CODE1,
                        repeat = 100,
                        number = 100)))
    print('Naive linked_list_to_list:')
    print(min(timeit.repeat(setup = SETUP_CODE,
                        stmt = TEST_CODE2,
                        repeat = 100,
                        number = 100)))

def fix_gaps_preformence_test():
    print('fix gaps preformance test:')

    SETUP_CODE ='''
#import numpy.random as nprnd #Numpy does not work with pypy
import random
from __main__ import linked_list_to_list
from __main__ import fix_gaps
from __main__ import naive_fix_gaps
from __main__ import fill_gaps_data
s = 10 # Number of "index"
n = 10000 # Days in each "index"
#l = [nprnd.randint(n, size=n*10) for i in range(s)] #Numpy does not work with pypy
l = [random.sample(range(1, n*10), n) for i in range(s)]
'''

    TEST_CODE1 = 'fix_gaps(l)'
    TEST_CODE2 = 'linked_list_to_list(fix_gaps(l))'
    TEST_CODE3 = 'naive_fix_gaps(l)'
    TEST_CODE4 = 'fill_gaps_data(l, l)'
    print('Ordinary fix_gaps:')
    print(min(timeit.repeat(setup = SETUP_CODE,
                        stmt = TEST_CODE1,
                        repeat = 100,
                        number = 1)))

    print('Ordinary linked_list_to_list(fix_gaps):')
    print(min(timeit.repeat(setup = SETUP_CODE,
                        stmt = TEST_CODE2,
                        repeat = 100,
                        number = 1)))

    print('Naive fix_gaps:')
    print(min(timeit.repeat(setup = SETUP_CODE,
                        stmt = TEST_CODE4,
                        repeat = 100,
                        number = 1)))

    print('Full fill_gaps:')
    print(min(timeit.repeat(setup = SETUP_CODE,
                        stmt = TEST_CODE4,
                        repeat = 100,
                        number = 1)))

def preformence_tests():
    list_to_linked_list_preformence_test()
    fix_gaps_preformence_test()


def tests():
    node_test()
    list_test()
    print_linked_list_test()
    fix_gaps_test()

    #preformence_tests()
    #fix_gaps_preformence_test()

if __name__ == '__main__':
    tests()