#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRectangleFlatIconButton

from src.view.styling.light_mode.button import get_style

class Options_frame:
    def __init__(self, view, super_frame):
        self.view = view
        self.pause_state = False

        options_frame = BoxLayout(size_hint=(1, .15))

        options_frame.add_widget(Widget(size_hint=(.8, 1))) # Space

        options_frame.add_widget(Widget(size_hint=(.2, 1))) # Space

        trades_button = MDRectangleFlatIconButton(
            icon= "plus-minus-variant",
            text= "Trades",
            on_release=self.trades_button_click,
            **get_style()
        )
        options_frame.add_widget(trades_button)

        options_frame.add_widget(Widget(size_hint=(.2, 1))) # Space

        clean_button = MDRectangleFlatIconButton(
            icon= "table-remove",
            text= "Clear",
            on_release=self.clean_button_click,
            **get_style()
        )
        options_frame.add_widget(clean_button)

        options_frame.add_widget(Widget(size_hint=(.2, 1))) # Space

        logPlot_button = MDRectangleFlatIconButton(
            icon= "chart-line-variant",
            text= "logPlot",
            on_release=self.logPlot_button_click,
            **get_style()
        )
        options_frame.add_widget(logPlot_button)


        options_frame.add_widget(Widget(size_hint=(.2, 1))) # Space

        self.pause_play_frame = BoxLayout(size_hint=(1, 1))
        self.pause_button = MDRectangleFlatIconButton(
            icon= "pause",
            text= "Pause",
            on_release=self.pause_button_click,
            **get_style()
        )
        self.pause_play_frame.add_widget(self.pause_button)
        options_frame.add_widget(self.pause_play_frame)

        self.play_button = MDRectangleFlatIconButton( # To be used when pause is clicked
                icon= "play",
                text= "Play",
                on_release=self.play_button_click,
                **get_style()
            )

        options_frame.add_widget(Widget(size_hint=(.8, 1))) # Space

        super_frame.add_widget(options_frame)

    def trades_button_click(self, instance):
        logging.debug("trades_button_click!")
        if self.view.show_trades:
            self.view.show_trades = False
        else:
            self.view.show_trades = True
        
        self.view.line_graph.update()

    def clean_button_click(self, instance):
        logging.debug("clean_button_click!")
        self.view.wipe_selected_instruments()

    def logPlot_button_click(self, instance):
        logging.debug("logPlot_button_click!")
        if self.view.log_plot:
            self.view.log_plot = False
        else:
            self.view.log_plot = True
        
        self.view.line_graph.update()

    def pause_button_click(self, instance):
        logging.debug("pause_button_click!")
        self.pause_state = True
        self.view.set_pause_state(self.pause_state)

        self.pause_play_frame.remove_widget(self.pause_button)
        self.pause_play_frame.add_widget(self.play_button)

    def play_button_click(self, instance):
        logging.debug("play_button_click!")
        self.pause_state = False
        self.view.set_pause_state(self.pause_state)

        self.pause_play_frame.remove_widget(self.play_button)
        self.pause_play_frame.add_widget(self.pause_button)
