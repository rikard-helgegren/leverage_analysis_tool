#!/usr/bin/env python3
#
# Copyright (C) 2024 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging

from src.view.styling.light_mode.color_palet import *

from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.widget import Widget

class Portfolio_tab():
    def __init__(self, table_of_instruments, frame):
        logging.debug("Portfolio_tab: __init__")

        self.nbr_of_portfolios = 1

        self.table_of_instruments = table_of_instruments
        self.frame = frame

        self.first_frame = BoxLayout(
                orientation='vertical', 
                size_hint=(0.1, 0.1))
        self.second_frame = BoxLayout(
                orientation='vertical', 
                size_hint=(0.1, 0.1))
        
        self.space_frame = BoxLayout(orientation='vertical',size_hint=(0.1, 0.1))
        
        
        def btn_left_press(value): #TODO find out have to have it outside __init__, it's "struggeling"
            logging.debug("Portfolio_tab: btn_left_press")
            self.select_first()

        def btn_right_press(value): #TODO find out have to have it outside __init__, it's "struggeling"
            logging.debug("Portfolio_tab: btn_right_press")
            self.select_second()
        
        self.portfolio1_btn = MDRaisedButton(
            text ="portfolio 1",
            size_hint=(1, 0.3),
            md_bg_color = blue)
        self.portfolio1_btn.bind(on_press=btn_left_press)
        self.first_frame.add_widget(self.portfolio1_btn)


        self.portfolio2_btn = MDRaisedButton(
            text ="portfolio 2",
            size_hint=(1, 0.1),
            md_bg_color = green)
        self.portfolio2_btn.bind(on_press=btn_right_press)

        self.add_portfolio_btn = MDRaisedButton(
            text ="+",
            size_hint=(.5, 0.1),
            md_bg_color = 'gray')
        self.add_portfolio_btn.bind(on_press=self.add_portfolio)
        self.second_frame.add_widget(self.add_portfolio_btn)

        self.frame.add_widget(Widget(size_hint=(.015, 0.1))) #Space
        self.frame.add_widget(self.first_frame)
        self.frame.add_widget(self.second_frame)
        self.frame.add_widget(self.space_frame)

    def select_first(self):
        logging.debug("Portfolio_tab: select_first")
        model_nbr = 0
        self.table_of_instruments.view.set_selected_model(model_nbr)
        self.portfolio1_btn.md_bg_color = blue
        self.portfolio2_btn.md_bg_color = gray_green
    
    def select_second(self):
        logging.debug("Portfolio_tab: select_second")
        model_nbr = 1
        self.table_of_instruments.view.set_selected_model(model_nbr)
        self.portfolio1_btn.md_bg_color = gray_blue
        self.portfolio2_btn.md_bg_color = green

    def add_portfolio(self, value):
        logging.debug("Portfolio_tab: add_portfolio")
        self.table_of_instruments.view.add_model()

        match self.nbr_of_portfolios:
            case 0:
                self.first_frame.remove_widget(self.add_portfolio_btn)
                self.first_frame.add_widget(self.portfolio1_btn)
                self.space_frame.size_hint(1.5, 0.1)
                self.nbr_of_portfolios += 1
                self.select_first()
            case 1:
                self.second_frame.remove_widget(self.add_portfolio_btn)
                self.second_frame.add_widget(self.portfolio2_btn)
                self.nbr_of_portfolios += 1
                self.select_second()
            case _:
                logging.warn("Cant handle this number of portfolios: " + str(self.nbr_of_portfolios)) 
                return
            
        
    def remove_portfolio(self, portfolio_number):
        logging.debug("Portfolio_tab: remove_portfolio")
        match portfolio_number:
            case 0:
                logging.warn("TODO")
            case 1:
                logging.warn("TODO")
            case _:
                logging.warn("Cant handle this portfolio number: " + str(portfolio_number)) 
                return
