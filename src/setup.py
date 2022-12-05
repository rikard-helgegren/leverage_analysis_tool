#!/usr/bin/env python3

import os
import sys
import subprocess

import model.constants as constants

# Compile c++ algorithms
program_folder = os.path.dirname(os.path.realpath(sys.argv[0]))
command = ['g++','-O2','-pthread','-fPIC','-shared','-o',
          constants.program_folder + '/compiled_code/calculateHistogramOutput.so',
          constants.program_folder + '/model/histogram/calculateHistogramOutput.cpp']
subprocess.run(command)
