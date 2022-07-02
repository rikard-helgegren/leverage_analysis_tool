#!/usr/bin/env bash

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${PWD}/code/model
python3 leverage_analysis_tool.py
