import logging

class List_node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None


def linked_list_to_string(linked_list):
    node = linked_list.head
    string = ''
    while node != None:
        string += str(node.data)
        string += '-'
        node = node.next
    string += 'None'
    return string


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
def find_first_common_market_day(lists_of_indexes, chosen_time_interval_start_date):
    """ Returns the earliest day that all selected indexes have in common
        or
        The manually set day to use as first, if it is valid for all indexes.
    """
    first_common = max([x[0] for x in lists_of_indexes])
    if chosen_time_interval_start_date == 0:
        return first_common

    return max(first_common, chosen_time_interval_start_date)


def find_last_common_market_day(lists_of_indexes, chosen_time_interval_end_date):
    """ Returns the last day that all selected indexes have in common
        or
        The manually set day to use as last, if it is valid for all indexes.
    """
    last_common = min([x[-1] for x in lists_of_indexes])
    if chosen_time_interval_end_date == 0:
        return last_common

    return min(last_common, chosen_time_interval_end_date)


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


def fill_gaps_data(markets_selected, chosen_time_interval_start_date, chosen_time_interval_end_date):
    logging.debug("Model: fill_gaps_data")

    if markets_selected == {}:
        return {}

    #prefix adapter
    lists_to_fill = []
    lists_of_values = []
    for market in markets_selected.values():
       lists_to_fill.append(market.get_time_span())
       lists_of_values.append(market.get_values())
    #end prefix adapter

    latest_first = find_first_common_market_day(lists_to_fill, chosen_time_interval_start_date)
    earliest_last = find_last_common_market_day(lists_to_fill, chosen_time_interval_end_date)
    master_linked_list = fix_gaps2(lists_to_fill, latest_first, earliest_last)
    node = master_linked_list.head
    master_lists_of_values = []

    for (list_to_fill, list_of_values) in zip(lists_to_fill, lists_of_values):
        i = 0
        value_list = []
        while node is not None:

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

    #sufix adapter
    for i, market in enumerate(markets_selected.values()):
        market.set_time_span(master_list)
        market.set_values(master_lists_of_values[i])
    #end sufix adapter

    return markets_selected
