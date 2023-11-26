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

class Strategy_menue:
    def __init__(self, view, frame):
        self.view = view

        self.main_frame_width = 1
        self.main_frame_hight = 0.32
        self.strategy_main_frame = BoxLayout(
                orientation='vertical', 
                size_hint=(
                        self.main_frame_width,
                        self.main_frame_hight))

        self.strategy_frames = self.init_strategy_frames()
        """Dict, key is startegy, value is corresponding frame"""

        self.current_strategy = ""

        self.menue_width = 0.3
        self.menue_hight = 0.1

            
        frame.add_widget(Widget(size_hint=(1, .2))) #Space

        self.drop_down_menue = Spinner(
            text='Strategies',
            values=constants.PORTFOLIO_STRATEGIES,
            size_hint=(self.menue_width, self.menue_hight),
            pos_hint={'center_x': .5, 'center_y': .5}
        )

        self.drop_down_menue.bind(text=self.update_strategy)
        self.strategy_main_frame.add_widget(self.drop_down_menue)

        # I don't understand the size settings so this is a ugly hack to make
        # the strategy menue have a correct size before selecting a strategy.
        self.no_strategy_box = BoxLayout(size_hint=(0.0, 0.1))
        self.strategy_main_frame.add_widget(self.no_strategy_box)
        
        frame.add_widget(self.strategy_main_frame)


    def update_strategy(self, spinner, new_strategy):
        logging.debug("Strategy_menue: update_strategy: new_strategy %r old strategy %r", new_strategy, self.current_strategy)
        
        old_strategy = self.current_strategy

        if old_strategy == "":
            self.strategy_main_frame.remove_widget(self.no_strategy_box)
        else:
            self.strategy_main_frame.remove_widget(self.strategy_frames[old_strategy])

        self.strategy_main_frame.add_widget(self.strategy_frames[new_strategy])

        self.current_strategy = new_strategy
        self.view.update_strategy_selected(new_strategy)


    def init_strategy_frames(self):

        strategy_frames = {}
        self.view.rebalance_strategy = Rebalance_strategy(self.view)
        self.view.harvest_refill_strategy = Harvest_refill_strategy(self.view)
        self.view.variance_strategy = Variance_strategy(self.view)
        
        strategy_frames['Hold'] = BoxLayout(size_hint=(0.0, 0.1))
        strategy_frames['Harvest/Refill'] = self.view.harvest_refill_strategy.get_frame()
        strategy_frames['Rebalance Time'] = self.view.rebalance_strategy.get_frame()
        strategy_frames['Do not invest'] = BoxLayout(size_hint=(0.0, 0.1))
        strategy_frames['Variance Dependent'] = self.view.variance_strategy.get_frame()

        return strategy_frames
