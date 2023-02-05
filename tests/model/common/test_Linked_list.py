#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

from src.model.common.Linked_list import Linked_list
from src.model.common.Linked_list import List_node
from src.model.common.Linked_list import linked_list_to_list
from src.model.common.Linked_list import list_to_linked_list

def test_linked_list_to_list():

    master_node = List_node(1)
    master_node.next = List_node(2)
    linked_list = Linked_list()
    linked_list.head = master_node

    assert linked_list_to_list(linked_list) == [1,2]

def test_list_to_linked_list():

    answer_linked_list = list_to_linked_list([1,2])

    master_node = List_node(1)
    master_node.next = List_node(2)

    linked_list = Linked_list()
    linked_list.head = master_node

    assert type(answer_linked_list) == type(linked_list)
    assert answer_linked_list.head.data == linked_list.head.data  # Check value of first node
    assert answer_linked_list.head.next.data == linked_list.head.next.data  # Check value of second node
