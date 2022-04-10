import timeit

class Tree_node:
    def __init__(self, data=None, cmp=lambda x, y: x - y):
        self.data = data
        self.left = None
        self.right = None
        self.depth = 1
        self.parent = None
        self.cmp = cmp

    def add_node(self, node):
        added_left = False
        # add node
        if self.cmp(node.data, self.data) < 0:
            if self.left != None:
                self.left.add_node(node)
            else:
                self.left = node
                node.parent = self
                self.balance_tree()
        else:
            if self.right != None:
                self.right.add_node(node)
            else:
                self.right = node
                node.parent = self
                self.balance_tree()

    def depth(node):
        if node == None:
            return 0
        else:
            return node.depth

    def fix_depth(self):
        self.depth = max([Tree_node.depth(self.left), Tree_node.depth(self.right)]) + 1

    def balance_tree(self):
        if Tree_node.depth(self.left) > Tree_node.depth(self.right) + 1:
            #switch nodes
            temp_node = self.left
            self.left = self.left.right
            temp_node.right = self

            temp_node.parent = self.parent
            self.parent = temp_node
            if self.left != None:
                self.left.parent = self

            self.fix_depth()
            temp_node.fix_depth()
        
            if temp_node.parent != None:
                # fix parent
                if temp_node.parent.left == self:
                    temp_node.parent.left = temp_node
                else:
                    temp_node.parent.right = temp_node

                temp_node.parent.balance_tree()
        elif Tree_node.depth(self.right) > Tree_node.depth(self.left) + 1:
            #switch nodes
            temp_node = self.right
            self.right = self.right.left
            temp_node.left = self

            temp_node.parent = self.parent
            self.parent = temp_node
            if self.right != None:
                self.right.parent = self

            self.fix_depth()
            temp_node.fix_depth()

            if temp_node.parent != None:
                # fix parent
                if temp_node.parent.left == self:
                    temp_node.parent.left = temp_node
                else:
                    temp_node.parent.right = temp_node

                temp_node.parent.balance_tree()
        else:
            self.fix_depth()
            if self.parent != None:
                self.parent.balance_tree()

class Ordered_tree:
    def __init__(self, cmp=lambda x, y: x - y):
        self.head = None
        self.cmp = cmp

    def add_node(self, node):
        if self.head == None:
            self.head = node
            node.parent = None
        else:
            self.head.add_node(node)
            if self.head.parent != None:
                self.head = self.head.parent

    def add(self, data):
        self.add_node(Tree_node(data, cmp=self.cmp))

class Min_heap:
    def __init__(self, cmp=lambda x, y: x - y):
        self.tree = Ordered_tree(cmp=cmp)

    def add(self, data):
        self.tree.add(data)

    def peek(self):
        if self.tree.head == None:
            return None
        # returns the smallest value in the tree
        node = self.tree.head
        while node.left != None:
            node = node.left
        return node.data

    def pop(self):
        if self.tree.head != None:
            if self.tree.head.left == None:
                if self.tree.head.right == None:
                    self.tree.head = None
                else:
                    self.tree.head = self.tree.head.right
                    self.tree.head.parent = None
            else:    
                # find the smallest value in the tree, and remove it
                node = self.tree.head
                while node.left != None:
                    node = node.left
                node.parent.left = node.right
                if node.right != None:
                    node.right.parent = node.parent
                node.parent.balance_tree()

                if self.tree.head.parent != None:
                    self.tree.head = self.tree.head.parent


#######################################################
###                  Algorithms                     ###
#######################################################

def naive_cutoff(list_of_values, cutoff, values_to_check):
    gains = []
    have_appended = False
    for i in range(0, len(list_of_values) - values_to_check):
        gain = 0
        start_value = list_of_values[i]
        have_appended = False

        for value in list_of_values[i:i + values_to_check + 1]:
            end_value = value

            if value < cutoff*start_value:
                gains.append(cutoff*start_value)
                have_appended = True
                break

        if not have_appended:
            gains.append(end_value - start_value)
    return gains

def improved_cutoff(list_of_values, cutoff, values_to_check):
    start_value = list_of_values[0]
    end_value = list_of_values[values_to_check]
    lowest_value = min(list_of_values[:values_to_check + 1])

    gains = []
    if lowest_value < cutoff*start_value:
        gains.append(cutoff*start_value)
    else:
        gains.append(end_value - start_value)

    for i in range(1, len(list_of_values) - values_to_check):
        
        # Recalculate lowest
        if start_value == lowest_value:
            lowest_value = min(list_of_values[i:i + values_to_check + 1])
        elif list_of_values[i + values_to_check] < lowest_value:
            lowest_value = list_of_values[i + values_to_check]
        
        start_value = list_of_values[i]
        end_value = list_of_values[i + values_to_check]

        if lowest_value < cutoff*start_value:
            gains.append(cutoff*start_value)
        else:
            gains.append(end_value - start_value)
    
    return gains


def improved_cutoff_heap(list_of_values, cutoff, values_to_check):
    start_value = list_of_values[0]
    end_value = list_of_values[values_to_check]

    heap = Min_heap(cmp=lambda a, b: a[1] - b[1])
    for pair in enumerate(list_of_values[:values_to_check + 1]):
        heap.add(pair)

    gains = []
    if heap.peek()[1] < cutoff*start_value:
        gains.append(cutoff*start_value)
    else:
        gains.append(end_value - start_value)

    for i in range(1, len(list_of_values) - values_to_check):
        
        heap.add((i + values_to_check, list_of_values[i + values_to_check]))

        # Recalculate lowest
        index_lowest_value, lowest_value = heap.peek()
        if start_value == lowest_value: 
            #Note: if index_lowest_value > i then then lowest_value is still within the range we are looking at
            while index_lowest_value <= i:
                heap.pop()
                index_lowest_value, lowest_value = heap.peek()
        
        start_value = list_of_values[i]
        end_value = list_of_values[i + values_to_check]

        if lowest_value < cutoff*start_value:
            gains.append(cutoff*start_value)
        else:
            gains.append(end_value - start_value)
    
    return gains

#######################################################
###                     Tests                       ###
#######################################################

def check_depth_of_tree(node):
    if node != None:
        largest_lower_depth = max([Tree_node.depth(node.left), Tree_node.depth(node.right)])
        assert(Tree_node.depth(node) == largest_lower_depth + 1)
        assert(-1 <= Tree_node.depth(node.left) - Tree_node.depth(node.right) <= 1)
        check_depth_of_tree(node.left)
        check_depth_of_tree(node.right)

def check_parent(node, parent):
    if node != None:
        assert(node.parent == parent)
        check_parent(node.left, node)
        check_parent(node.right, node)

def tree_tests():
    tree = Ordered_tree()
    assert(tree.head == None)

    tree.add(1)
    assert(tree.head != None)
    assert(tree.head.data == 1)
    assert(tree.head.left == None)
    assert(tree.head.right == None)
    
    tree.add(2)
    assert(tree.head != None)
    assert(tree.head.data == 1)
    assert(tree.head.left == None)
    assert(tree.head.right != None)
    assert(tree.head.right.data == 2)
    assert(tree.head.right.left == None)
    assert(tree.head.right.right == None)

    tree.add(3)
    assert(tree.head != None)
    assert(tree.head.data == 2)
    assert(tree.head.left != None)
    assert(tree.head.left.data == 1)
    assert(tree.head.left.left == None)
    assert(tree.head.left.right == None)
    assert(tree.head.right != None)
    assert(tree.head.right.data == 3)
    assert(tree.head.right.left == None)
    assert(tree.head.right.right == None)

    tree.add(-1)
    assert(tree.head.left.left.data == -1)

    tree.add(1.5)
    assert(tree.head.left.right.data == 1.5)

    tree.add(2.5)
    assert(tree.head.right.left.data == 2.5)

    tree = Ordered_tree()
    for i in range(1, 1000):
        tree.add(i)
        check_depth_of_tree(tree.head)
        check_parent(tree.head, None)

def min_heap_tests():
    heap = Min_heap()

    # test add, peek
    for i in range(1, 1000):
        heap.add(i)
        assert(heap.peek() == 1)
        check_depth_of_tree(heap.tree.head)
        check_parent(heap.tree.head, None)

    # test peek, pop        
    for i in range(1, 1000):
        assert(heap.peek() == i)
        heap.pop()
        check_depth_of_tree(heap.tree.head)
        check_parent(heap.tree.head, None)

    assert(heap.peek() == None)

    # test max heap!
    heap = Min_heap(cmp=lambda x, y: y - x)

    # test add, peek
    for i in range(1, 1000):
        heap.add(i)
        assert(heap.peek() == i)
        check_depth_of_tree(heap.tree.head)
        check_parent(heap.tree.head, None)

    # test peek, pop        
    for i in range(1, 1000):
        assert(heap.peek() == 1000 - i)
        heap.pop()
        check_depth_of_tree(heap.tree.head)
        check_parent(heap.tree.head, None)

    assert(heap.peek() == None)

def cutoff_tests():
    list_to_test = [[1, 2, 3, 4, 5, 6],
                    [2, 4, 6, 8],
                    [1, 2],
                    [1, 7, 2, 8, 3, 7, 3, 9, 4],
                    [1, 4, 6, 7, 7, 9, 4, 8, 3, 8, 5, 6, 2]]
    cutoff_values = [0, 0, 1, 0.5, 0]
    values_to_check = [1, 3, 1, 4, 3]
    expected = [[1, 1, 1, 1, 1], 
                [6], 
                [1], 
                [2, 3.5, 1, 4.0, 1], 
                [6, 3, 3, -3, 1, -6, 4, -3, 3, -6]]
    for i in range(len(list_to_test)):
        assert(naive_cutoff(list_to_test[i], cutoff_values[i], values_to_check[i]) ==
               improved_cutoff(list_to_test[i], cutoff_values[i], values_to_check[i]))
        assert(naive_cutoff(list_to_test[i], cutoff_values[i], values_to_check[i]) ==
               improved_cutoff_heap(list_to_test[i], cutoff_values[i], values_to_check[i]))
        assert(improved_cutoff(list_to_test[i], cutoff_values[i], values_to_check[i]) ==
               expected[i])


def cutoff_preformence_tests():
    print('cutoffs preformance test:')

    SETUP_CODE ='''
import random
from __main__ import naive_cutoff
from __main__ import improved_cutoff
from __main__ import improved_cutoff_heap
n = 100000 # Days in each "index"
days = 36500 # Days to check
l = random.sample(range(1, n*10), n)
'''

    TEST_CODE1 = 'naive_cutoff(l, 0, days)'
    TEST_CODE2 = 'improved_cutoff(l, 0, days)'
    TEST_CODE3 = 'improved_cutoff_heap(l, 0, days)'
    print('Naive cutoff:')
    naive_time = min(timeit.repeat(setup = SETUP_CODE,
                        stmt = TEST_CODE1,
                        repeat = 10,
                        number = 1))

    print(naive_time)

    print('Improved cutoff:')
    improved_time = min(timeit.repeat(setup = SETUP_CODE,
                        stmt = TEST_CODE2,
                        repeat = 10,
                        number = 1))

    print(improved_time)

    print('Improved cutoff heap:')
    improved_heap_time = min(timeit.repeat(setup = SETUP_CODE,
                             stmt = TEST_CODE3,
                             repeat = 10,
                             number = 1))

    print(improved_heap_time)

    print("Fractions")
    print(naive_time/improved_time)
    print(naive_time/improved_heap_time)

def tests():
    tree_tests()
    min_heap_tests()
    cutoff_tests()

    cutoff_preformence_tests()

if __name__ == '__main__':
    tests()