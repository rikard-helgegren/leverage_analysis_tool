#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

from src.model.common.is_data_empty import is_data_empty

def test_is_data_empty():
    """If either of the entries are empty """

    arbitrary_data = [1,2]

    # Returning True
    assert is_data_empty([], [])
    assert is_data_empty(arbitrary_data, [])
    assert is_data_empty([], arbitrary_data)
    assert is_data_empty(None, [arbitrary_data])
    assert is_data_empty([arbitrary_data], None)

    # Retunring False
    assert not is_data_empty(arbitrary_data, arbitrary_data)

        