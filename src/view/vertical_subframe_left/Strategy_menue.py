#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from src.view.strategies.Rebalance_strategy import Rebalance_strategy
from src.view.strategies.Harvest_refill_strategy import Harvest_refill_strategy
from src.view.strategies.Variance_strategy import Variance_strategy
import src.constants as constants
import src.view.constants as constants_view

class Strategy_menue:
    def __init__(self, view, frame):
        self.view = view

        # When True, ignore spinner callbacks caused by programmatic updates
        self._suppress_strategy_callback = False

        self.strategy_main_frame = BoxLayout(
                orientation='vertical', 
                size_hint=(1, 0.32))

        self.strategy_frames = self.init_strategy_frames()
        """Dict, key is startegy, value is corresponding frame"""

        self.current_strategy = ""

        self.menue_width = 0.3
        self.menue_hight = 0.1

            
        frame.add_widget(Widget(size_hint=(1, .1))) #Space

        self.drop_down_menue = Spinner(
            text='Strategies',
            values=constants.PORTFOLIO_STRATEGIES,
            size_hint=(self.menue_width, self.menue_hight),
            pos_hint=constants_view.center
        )
        self.drop_down_menue.bind(text=self.update_strategy_using_menue)
        self.strategy_main_frame.add_widget(self.drop_down_menue)

        # I don't understand the size settings so this is a ugly hack to make
        # the strategy menue have a correct size before selecting a strategy.
        self.no_strategy_box = BoxLayout(size_hint=(0.0, 0.1))
        self.strategy_main_frame.add_widget(self.no_strategy_box)
        
        frame.add_widget(self.strategy_main_frame)


    def update_strategy_using_menue(self, spinner, new_strategy):
        # Ignore programmatic changes (set by `set_strategy_by_model`) to avoid
        # triggering controller updates. Only propagate user interactions.
        if self._suppress_strategy_callback:
            return

        self.update_strategy(new_strategy)
        self.view.update_strategy_selected(new_strategy)

    def update_strategy(self, new_strategy):
        logging.debug("Strategy_menue: update_strategy: new_strategy %r old strategy %r", new_strategy, self.current_strategy)
        old_strategy = self.current_strategy
        
        if old_strategy == "":
            self.strategy_main_frame.remove_widget(self.no_strategy_box)
        else:
            self.strategy_main_frame.remove_widget(self.strategy_frames[old_strategy])

        self.strategy_main_frame.add_widget(self.strategy_frames[new_strategy])

        self.current_strategy = new_strategy


    def init_strategy_frames(self):
        logging.debug("Strategy_menue: init_strategy_frames" )

        strategy_frames = {}
        self.view.rebalance_strategy = Rebalance_strategy(self.view)
        self.view.harvest_refill_strategy = Harvest_refill_strategy(self.view)
        self.view.variance_strategy = Variance_strategy(self.view)
        
        strategy_frames[constants.PORTFOLIO_STRATEGIES[0]] = BoxLayout(size_hint=(0.0, 0.1))
        strategy_frames[constants.PORTFOLIO_STRATEGIES[1]] = self.view.harvest_refill_strategy.get_frame()
        strategy_frames[constants.PORTFOLIO_STRATEGIES[2]] = self.view.rebalance_strategy.get_frame()
        strategy_frames[constants.PORTFOLIO_STRATEGIES[3]] = BoxLayout(size_hint=(0.0, 0.1))
        strategy_frames[constants.PORTFOLIO_STRATEGIES[4]] = self.view.variance_strategy.get_frame()

        return strategy_frames
    
    def set_strategy_by_model(self, strategy, strategy_parameters):
        logging.debug("Strategy_menue: set_strategy_by_model " + str(strategy))

        # Update the spinner without firing the user-change callback.
        self._suppress_strategy_callback = True
        try:
            self.drop_down_menue.text = strategy
        finally:
            self._suppress_strategy_callback = False

        # Update UI to reflect strategy selection (no controller call)
        self.update_strategy(strategy)

        variable = constants.PORTFOLIO_STRATEGIES[0]

        if strategy == constants.PORTFOLIO_STRATEGIES[0]:
            logging.debug("No data need to be set for strategy: " + str(strategy))
        elif strategy == constants.PORTFOLIO_STRATEGIES[1]:
            self.view.harvest_refill_strategy.set_harvest_value(strategy_parameters['harvest_point'])
            self.view.harvest_refill_strategy.set_refill_value(strategy_parameters['refill_point'])
        elif strategy == constants.PORTFOLIO_STRATEGIES[2]:
            self.view.rebalance_strategy.set_value(strategy_parameters['rebalance_period_months'])
        elif strategy == constants.PORTFOLIO_STRATEGIES[3]:
            logging.debug("No data need to be set for strategy: " + str(strategy))
        elif strategy == constants.PORTFOLIO_STRATEGIES[4]:
            self.view.variance_strategy.set_sample_size_variance(strategy_parameters['variance_calc_sample_size'])
            self.view.variance_strategy.set_sample_size_decision(strategy_parameters['volatility_strategie_sample_size'])
            self.view.variance_strategy.set_volatillaty_trigger(strategy_parameters['volatility_strategie_level'])

        else:
            logging.warn("Not accounted for strategy: " + str(strategy))
