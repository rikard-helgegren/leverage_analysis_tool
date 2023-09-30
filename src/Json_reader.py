#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import os
import sys
import simplejson as json
class Json_reader:
    def read_config():
        #program_folder = os.path.dirname(os.path.realpath(sys.argv[0]))  # TODO: not working for tests runing from /tmp 
        program_folder = os.getcwd()  # TODO: not working when running from other folder then project folder
        config_path = program_folder + '/config.json'

        json_data = {}
        with open(config_path, "r") as file:

            json_data = json.load(file)
        
        return json_data