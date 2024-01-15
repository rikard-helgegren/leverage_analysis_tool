#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.


class List_node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class Linked_list:
    def __init__(self):
        self.head = None


def linked_list_to_list(linked_list):
    temp_list = []
    node = linked_list.head
    while node != None:
        temp_list.append(node.data)
        node = node.next
    return temp_list


def list_to_linked_list(list):
    master_node = List_node() # Dummy node
    previous_node = master_node
    current_node = None

    for item in list:
        previous_node.next = List_node(item)
        previous_node = previous_node.next
        previous_node.next = current_node

    master_index_list = Linked_list()
    master_index_list.head = master_node.next
    return master_index_list
