#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import subprocess

import model.common.constants_model as constants_model

# Compile c++ algorithms
command = ['g++','-O2', '-std=c++11','-pthread','-fPIC','-shared','-o',
          constants_model.program_folder + '/compiled_code/calculateHistogramOutput.so',
          constants_model.program_folder + '/model/histogram/calculateHistogramOutput.cpp']
subprocess.run(command)
