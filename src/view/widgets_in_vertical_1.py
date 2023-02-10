#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import tkinter as tk

from src.Config import Config # TODO: Called to manny times 
from src.view.menu_of_strategies import Menu_Of_Strategies



def setup_vertical_frame_1(view):

    super_frame = tk.Frame(view, padx=5, pady=5)
    super_frame.pack(side=tk.LEFT)

    insert_slide_for_leverage(view, super_frame)
    insert_fee_checkbox(view, super_frame)
    insert_years_and_loan(view, super_frame)
    insert_strategy_menue(view, super_frame)
    insert_harvest_refill(view, super_frame)
    insert_rebalance_time(view, super_frame)
    insert_varinace_togles(view, super_frame)


def insert_slide_for_leverage(view, super_frame):
    view.frame_leverage = tk.Frame(super_frame, padx=5, pady=5)
    view.frame_leverage.pack()

    view.label_leverage = tk.Label(view.frame_leverage, text='Percent Leverage')
    view.label_leverage.pack()

    view.scale = tk.Scale(view.frame_leverage, from_=0, to=100, orient='horizontal', command=view.update_amount_leverage)
    view.scale.set(Config().DEFAUT_PROPORTION_LEVERAGE*100)
    view.scale.pack()


def insert_fee_checkbox(view, super_frame):
    view.frame_Checkbox = tk.Frame(super_frame, padx=5, pady=5)
    view.frame_Checkbox.pack()
    view.checkbutton_fee_state = tk.BooleanVar() 
    view.checkbutton_fee_state.set(True)
    view.checkbutton_fee = tk.Checkbutton(view.frame_Checkbox,
                                          text="Include Fees",
                                          variable=view.checkbutton_fee_state,
                                          command=view.update_fee_status)
    view.checkbutton_fee.pack()


def insert_years_and_loan(view, super_frame):
    # make spinbox pair horisontal
    view.frame_group1 = tk.Frame(super_frame, padx=5, pady=5)
    view.frame_group1.pack()


    view.frame_years = tk.Frame(view.frame_group1, padx=5, pady=5)
    view.frame_years.pack(side=tk.LEFT)
    view.label_years = tk.Label(view.frame_years, text='Years\nInvesting')
    view.label_years.pack()
    view.spin_years = tk.Spinbox(view.frame_years, from_=0, to=100, width=5, command=view.update_years_histogram_interval)
    view.spin_years.delete(0)
    view.spin_years.insert(0, Config().DEFAUT_YEARS_HISTOGRAM_INTERVAL)
    view.spin_years.pack()

    view.frame_loan = tk.Frame(view.frame_group1, padx=5, pady=5)
    view.frame_loan.pack(side=tk.LEFT)
    view.label_loan = tk.Label(view.frame_loan, text='\nLoan')
    view.label_loan.pack()
    view.spin_loan = tk.Spinbox(view.frame_loan, from_=0, to=100, width=5, command=view.update_loan)
    view.spin_loan.delete(0)
    view.spin_loan.insert(0, Config().DEFAUT_LOAN)
    view.spin_loan.pack()


def insert_strategy_menue(view, super_frame):
    view.menu_of_strategies = Menu_Of_Strategies(super_frame, view)


def insert_harvest_refill(view, super_frame):
    # make spinbox pair horisontal
    view.frame_group2 = tk.Frame(super_frame, padx=5, pady=5)
    view.frame_group2.pack()

    view.frame_harvest_point = tk.Frame(view.frame_group2, padx=5, pady=5)
    view.frame_harvest_point.pack(side=tk.LEFT)
    view.label_harvest_point = tk.Label(view.frame_harvest_point, text='Harvest\nPoint %')
    view.label_harvest_point.pack()
    view.spin_harvest_point = tk.Spinbox(view.frame_harvest_point, from_=101, to=2000, width=5, command=view.update_harvest_point)
    view.spin_harvest_point.delete(0,"end")
    view.spin_harvest_point.insert(0, Config().DEFAUT_HARVEST_POINT)
    view.spin_harvest_point.pack()

    view.frame_refill_point = tk.Frame(view.frame_group2, padx=5, pady=5)
    view.frame_refill_point.pack(side=tk.LEFT)
    view.label_refill_point = tk.Label(view.frame_refill_point, text='Refill\nPoint %')
    view.label_refill_point.pack()
    view.spin_refill_point = tk.Spinbox(view.frame_refill_point, from_=0, to=99, width=5, command=view.update_refill_point)
    view.spin_refill_point.delete(0)
    view.spin_refill_point.insert(0, Config().DEFAUT_REFILL_POINT)
    view.spin_refill_point.pack()

def insert_rebalance_time(view, super_frame):

    view.frame_group3 = tk.Frame(super_frame, padx=5, pady=5)
    view.frame_group3.pack()

    view.frame_rebalance_point = tk.Frame(view.frame_group3, padx=5, pady=5)
    view.frame_rebalance_point.pack(side=tk.LEFT)
    view.label_rebalance_point = tk.Label(view.frame_rebalance_point, text='Rebalance\nMonth')
    view.label_rebalance_point.pack()
    view.spin_rebalance_point = tk.Spinbox(view.frame_rebalance_point, from_=0, to=100, width=5, command=view.update_rebalance_point)
    view.spin_rebalance_point.delete(0,"end")
    view.spin_rebalance_point.insert(0, Config().DEFAUT_REBALANCE_PERIOD_MONTHS)
    view.spin_rebalance_point.pack()

def insert_varinace_togles(view, super_frame):
    
    # make spinbox trio horisontal
    view.frame_group4 = tk.Frame(super_frame, padx=5, pady=5)
    view.frame_group4.pack()

    view.frame_variance_calc_sample_size = tk.Frame(view.frame_group4, padx=5, pady=5)
    view.frame_variance_calc_sample_size.pack(side=tk.LEFT)
    view.label_variance_calc_sample_size = tk.Label(view.frame_variance_calc_sample_size, text='Sample size\ncalc variance')
    view.label_variance_calc_sample_size.pack()
    view.spin_variance_calc_sample_size = tk.Spinbox(view.frame_variance_calc_sample_size, from_=2, to=2000, width=5, command=view.update_variance_calc_sample_size)
    view.spin_variance_calc_sample_size.delete(0,"end")
    view.spin_variance_calc_sample_size.insert(0, Config().DEFAUT_VARIANCE_SAMPLE_SIZE)
    view.spin_variance_calc_sample_size.pack()

    view.frame_volatility_strategie_sample_size = tk.Frame(view.frame_group4, padx=5, pady=5)
    view.frame_volatility_strategie_sample_size.pack(side=tk.LEFT)
    view.label_volatility_strategie_sample_size = tk.Label(view.frame_volatility_strategie_sample_size, text='Sample size\nstartegy decition')
    view.label_volatility_strategie_sample_size.pack()
    view.spin_volatility_strategie_sample_size = tk.Spinbox(view.frame_volatility_strategie_sample_size, from_=0, to=2000, width=5, command=view.update_volatility_strategie_sample_size)
    view.spin_volatility_strategie_sample_size.delete(0,"end")
    view.spin_volatility_strategie_sample_size.insert(0, Config().DEFAUT_VOLATILITY_STRATEGIE_SAMPLE_SIZE)
    view.spin_volatility_strategie_sample_size.pack()

    view.frame_volatility_strategie_level = tk.Frame(view.frame_group4, padx=5, pady=5)
    view.frame_volatility_strategie_level.pack(side=tk.LEFT)
    view.label_volatility_strategie_level = tk.Label(view.frame_volatility_strategie_level, text='Volatility\ntrigger level')
    view.label_volatility_strategie_level.pack()
    view.spin_volatility_strategie_level = tk.Spinbox(view.frame_volatility_strategie_level, from_=0, to=99, width=5, command=view.update_volatility_strategie_level, format="%.3f", increment=0.001)
    view.spin_volatility_strategie_level.delete(0,"end")
    view.spin_volatility_strategie_level.insert(0, str(Config().DEFAUT_VOLATILITY_STRATEGIE_LEVEL).replace(".", ",")+"0")
    view.spin_volatility_strategie_level.pack()
