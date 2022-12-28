#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

from src.model.common.check_data_is_empty import check_data_is_empty

def test_check_data_is_empty():
    """If ither of the entries are empty """

    arbitrary_data = [1,2]

    # Returning True
    assert check_data_is_empty([], [])
    assert check_data_is_empty(arbitrary_data, [])
    assert check_data_is_empty([], arbitrary_data)
    assert check_data_is_empty(None, [arbitrary_data])
    assert check_data_is_empty([arbitrary_data], None)

    # Retunring False
    assert not check_data_is_empty(arbitrary_data, arbitrary_data)

        