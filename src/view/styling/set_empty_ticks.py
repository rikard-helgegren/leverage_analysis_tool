#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

def set_empty_ticks(graph_axis):
    graph_axis.set_xticks([0,2,4,6,8,10], ['','','','','',''])
    graph_axis.set_yticks([0,2,4,6,8,10], ['','','','','',''])
