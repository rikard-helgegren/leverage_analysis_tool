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
from kivy.uix.textinput import TextInput

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
        # the strategy menue have acorrect size before selecting a strategy.
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
        
        strategy_frames['Hold'] = BoxLayout(size_hint=(0.0, 0.1))
        strategy_frames['Harvest/Refill'] = self.harvest_refill_frame()
        strategy_frames['Rebalance Time'] = self.rebalance_frame()
        strategy_frames['Do not invest'] = BoxLayout(size_hint=(0.0, 0.1))
        strategy_frames['Variance Dependent'] = BoxLayout(size_hint=(0.0, 0.1))

        return strategy_frames
        

    def rebalance_frame(self):
        rebalance_time_frame = BoxLayout(
                orientation='vertical',
                size_hint=(0.4, 0.2),
                pos_hint={'center_x': .5, 'center_y': .5})
        rebalance_time_frame.add_widget(Widget(size_hint=(1, .2))) #Space
        label = Label(text='[color=000000]Rebalance period (Months)[/color]',
                markup = True, size_hint=(1, .8))
        rebalance_time_frame.add_widget(label)
        text_box_rebalance = TextInput(
                text='6',
                multiline=False,
                size_hint =(.3, 1),
                pos_hint={'center_x': .5, 'center_y': .5})
        text_box_rebalance.bind(on_text_validate=self.update_rebalance_point)
        rebalance_time_frame.add_widget(text_box_rebalance)

        return rebalance_time_frame
        
    def harvest_refill_frame(self):

            harvest_refill_frame = BoxLayout(size_hint=(.5, 0.2), pos_hint={'center_x': .5, 'center_y': .5})

            inner_frame_left = BoxLayout(orientation='vertical', size_hint=(1, 1))
            inner_frame_left.add_widget(Widget(size_hint=(1, .2))) #Space
            label = Label(text='[color=000000]Harvest[/color]',
            markup = True, size_hint=(1, .8))
            inner_frame_left.add_widget(label)
            text_box_harvest_point = TextInput(text='150', multiline=False, size_hint =(1, 1))
            text_box_harvest_point.bind(on_text_validate=self.update_harvest_point)
            inner_frame_left.add_widget(text_box_harvest_point)
            harvest_refill_frame.add_widget(inner_frame_left)

            harvest_refill_frame.add_widget(Widget(size_hint=(.3, 1)))  #Space

            inner_frame_right = BoxLayout(orientation='vertical', size_hint=(1, 1))
            inner_frame_right.add_widget(Widget(size_hint=(1, .2))) #Space
            label = Label(text='[color=000000]Refill[/color]',
            markup = True, size_hint=(1, .8))
            inner_frame_right.add_widget(label)
            text_box_refill_point = TextInput(text='50', multiline=False, size_hint =(1, 1))
            text_box_refill_point.bind(on_text_validate=self.update_refill_point)
            inner_frame_right.add_widget(text_box_refill_point)
            harvest_refill_frame.add_widget(inner_frame_right)

            return harvest_refill_frame
    
    def extract_data(self, text_box):
        logging.warning("Not implemented. This is placeholder")

    def update_harvest_point(self, text_box):
        harvest_point = text_box._get_text()
        if harvest_point.isdigit():
            self.view.update_harvest_point(int(harvest_point))
        else:
            logging.error('"%r" is not a number', harvest_point)

    def update_refill_point(self, text_box):
        refill_point = text_box._get_text()
        if refill_point.isdigit():
            self.view.update_refill_point(int(refill_point))
        else:
            logging.error('"%r" is not a number', refill_point)
    
    def update_rebalance_point(self, text_box):
        rebalnce_intervall = text_box._get_text()
        if rebalnce_intervall.isdigit():
            self.view.update_rebalnce_intervall(int(rebalnce_intervall))
        else:
            logging.error('"%r" is not a number', rebalnce_intervall)
