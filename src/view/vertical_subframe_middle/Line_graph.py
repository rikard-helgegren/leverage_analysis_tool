#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.
import logging
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from kivy.metrics import dp
from kivy.uix.widget import Widget
from src.view.Matplot_figure import MatplotFigure
from src.view.styling.set_empty_ticks import set_empty_ticks
from src.view.styling.light_mode.color_palet import *


#optimized draw on Agg backend
mpl.rcParams['path.simplify'] = True
mpl.rcParams['path.simplify_threshold'] = 1.0
mpl.rcParams['agg.path.chunksize'] = 1000

#define some matplotlib figure parameters
#mpl.rcParams['font.family'] = 'Verdana'
mpl.rcParams['axes.spines.top'] = False
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.linewidth'] = 1.0

font_size_axis_title=dp(13)
font_size_axis_tick=dp(12)        


class Line_graph(Widget):
    """class that generate Matplotlib graph."""
    def __init__(self, view, frame): 
        logging.debug("View: Line_graph: __init__") 
        super().__init__()
        self.values_list = [] 
        self.time_span_list = [[]]
        self.buy_sell_log = {}
        self.time_union = []

        self.view = view

        self.fig, self.axs = plt.subplots(
            nrows=1, 
            ncols=1,
            sharey=True,
            tight_layout=True,
            facecolor=light_gray
        )
    
        set_empty_ticks(self.axs)
        self.matplot = MatplotFigure()
        self.matplot.figure = self.fig
        frame.add_widget(self.matplot)

        self.canvas = self.matplot.figcanvas


    def draw(self, time_union, values_list, time_span_list, buy_sell_log_list):
        logging.debug("View: Line_graph, draw")

        
        # buy_sell_mapped_to_downsampled_time_list = self.map_buy_sell_to_downsampeled_time(time_span_list, buy_sell_log_list)
        self.values_list = self.downsample_long_lists_in_list(values_list)
        self.time_span_list = self.downsample_long_lists_in_list(time_span_list)
        self.buy_sell_log_list = buy_sell_log_list #TODO implement downsampling of buy_sell_log_list. Currently braking when used.
        self.time_union = self.downsample_long_lists_in_list(time_union)

        self._draw()

    def update(self):
        logging.debug("View: Line_graph, update")
        self._draw()

    def _draw(self):
        logging.debug("View: Line_graph, _draw")
        plt.figure(self.fig.number)
        clear_canvas = True

        color_graph = portfolio_data_color

        #if clear_before_drawing: #TODO implement with this input
        self.axs.clear()
        self.set_time_on_x_axis(self.axs)

        for index in range(len(self.values_list)):
            if self.values_list[index] != []:
                
                if self.view.show_trades and self.buy_sell_log_list[index] != {}:
                    self.set_buy_and_sell_markers(self.axs, self.time_span_list[index], self.values_list[index], self.buy_sell_log_list[index])
                
                self.line1, = self.axs.plot(
                        self.time_span_list[index],
                        self.values_list[index], 
                        color = color_graph[index], 
                        alpha = 0.5)

                if self.view.log_plot:
                    self.axs.set_yscale("log")
                
                plt.tight_layout()
                clear_canvas = False
        
        if clear_canvas:
            set_empty_ticks(self.axs)
        
        self.canvas.draw()

    def downsample_long_lists_in_list(self, values_list, max_len=1_000):
        logging.debug("View: Line_graph, downsample_long_lists_in_list:" + str(max_len))
        """
        Downsample each sublist in values_list to at most max_len elements
        by removing items evenly across the list.

        Args:
            values_list (list[list]): List of value lists
            max_len (int): Maximum allowed length per sublist

        Returns:
            list[list]: Downsampled values_list
        """
        downsampled = []

        if not values_list:
            logging.debug("Empty input")
            return downsampled

        # Case 1: Single flat list → return unchanged
        if not isinstance(values_list, list):
            logging.debug("No list input")
            return values_list
        
        if not isinstance(values_list[0], list):
            logging.debug("No list in list input")
            return values_list


        for values in values_list:
            n = len(values)

            if n <= max_len:
                downsampled.append(values)
                continue

            step = n / max_len
            indices = [int(i * step) for i in range(max_len)]
            downsampled.append([values[i] for i in indices])

        return downsampled
    
    def map_buy_sell_to_downsampeled_time(self, time_span_list, buy_sell_log_list):
        """
        Remap buy/sell logs (keyed by original indices) to downsampled indices.

        Args:
            time_span_list (list[list]):
                Downsampled time lists (same downsampling as values)
            buy_sell_log_list (list[dict]):
                Trade logs keyed by ORIGINAL index positions

        Returns:
            list[dict]:
                Trade logs keyed by DOWNSAMPLED index positions
        """

        if not time_span_list or not buy_sell_log_list:
            return buy_sell_log_list

        mapped_logs = []

        for times, trade_log in zip(time_span_list, buy_sell_log_list):
            if not trade_log or not times:
                mapped_logs.append({})
                continue

            # Infer original length from trade log indices
            original_len = max(trade_log.keys()) + 1
            down_len = len(times)

            # Recreate original indices that survived downsampling
            step = original_len / down_len
            sampled_original_indices = [int(i * step) for i in range(down_len)]

            # Map original index → downsampled index
            orig_to_down = {
                orig_idx: down_idx
                for down_idx, orig_idx in enumerate(sampled_original_indices)
            }

            new_trade_log = {}

            for orig_trade_idx, trades in trade_log.items():
                # Find closest kept original index
                closest_orig = min(
                    sampled_original_indices,
                    key=lambda x: abs(x - orig_trade_idx)
                )

                down_idx = orig_to_down[closest_orig]

                new_trade_log.setdefault(down_idx, []).extend(trades)

            mapped_logs.append(new_trade_log)

        return mapped_logs



    def set_buy_and_sell_markers(self, axs, times, values, buy_sell_log):
        logging.debug("View: Line_graph, set_buy_and_sell_markers")
        circle_size =100

        x_values = []
        y_values = []
        colors = []
        did_buy=False
        did_sell=False

        for value in buy_sell_log:
            if value < times[0] and value > times[-1]: # bug from samples size of data to determine behaviour
                logging.warn("index out off bounds scatter plott" + str(value) + "MIN " + str(times[0]) + ", MAX " + times[-1])
            else:  
                x_values.append(value)
                #TODO uggly implementation, redo this log in c++ and do it propper with information in data type.
                ego_index = value - times[0] # not the common date indeces but the one specific to this graph
                y_values.append(values[ego_index])
                events = buy_sell_log[value]
                
                # Reset
                did_buy=False
                did_sell=False

                for event in events:
                    if event['Action'].value == 1:
                        did_buy=True
                    elif event['Action'].value == 2:
                        did_sell=True
                    else:
                        logging.warn("View.Linegraph: set_buy_and_sell_markers, invallid logg action: " + str(event['Activity']))
                
                if did_buy and did_sell:
                    colors.append(graph_buy_and_sell)
                elif did_buy:
                    colors.append(graph_buy_green)
                elif did_sell:
                    colors.append(graph_sell_red)

        axs.scatter(x_values, y_values, s=circle_size, c=colors)

    def set_time_on_x_axis(self, ax):
        logging.debug("View: Line_graph, set_time_on_x_axis")
        pos = []
        labels = []

        reference_year = ""
        for i, time in enumerate(self.time_union):
            #get first 4 digits, i.e. the year
            year = str(time)[:4]
            if year != reference_year:
                reference_year = year
                pos.append(i)
                labels.append(year)

        ax.set_xticks(pos, labels, rotation='vertical')
