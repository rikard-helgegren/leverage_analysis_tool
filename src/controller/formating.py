#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

def formatDate(date):
    """Change format from 20220101 to 2022-01-01"""

    date = str(date)
    date = list(date)
    date.insert(6, '-')
    date.insert(4, '-')
    date = ''.join(date)

    return date
