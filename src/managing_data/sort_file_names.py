#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

def sort_file_names(clean_file_names, sort_ranking):
    new_list = []

    for name_rank in sort_ranking:
        for name_file in clean_file_names:
            if name_rank in name_file:
                new_list.append(name_file)

    for name_file in clean_file_names:
        if name_file not in new_list:
            new_list.append(name_file) 

    return new_list
