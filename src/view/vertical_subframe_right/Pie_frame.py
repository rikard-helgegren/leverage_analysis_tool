#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.
import logging


from kivy.uix.boxlayout import BoxLayout

from matplotlib import pyplot as plt
import numpy as np


from src.view.Matplot_figure import MatplotFigure

class Pie_frame():
    def __init__(self, view, frame, title=""):

        self.title = title

        orange = [232/255, 184/255, 84/255]
        pink = [193/255,234/255,66/255]

        self.default_color = orange
        self.refrence_color = pink
        self.max_value = 20


        light_gray_value = .98
        light_gray = [light_gray_value, light_gray_value, light_gray_value]
        self.fig, self.axs = plt.subplots(
            1,
            1,
            sharey=True,
            tight_layout=True, 
            facecolor=light_gray,
            edgecolor=light_gray)
        
        with_size = 0.2

        data1 = np.array([1,2,2.8])
        data2 = np.array([0.7,2.3,2.8])

        outer_colors = [light_gray,self.refrence_color,light_gray]
        inner_colors = [light_gray,self.default_color,light_gray]

        self.axs.pie(data1, radius=1, colors=(outer_colors),
            wedgeprops=dict(width=with_size, edgecolor='w'))
        self.axs.set_title(self.title, pad=0, y=0.95, 
                    fontdict={'fontsize': 15,
                            'fontweight': 'bold',
                            'color': 'k'})

        self.axs.pie(data2, radius=1-with_size, colors=inner_colors,
            wedgeprops=dict(width=with_size, edgecolor='w'))
  
        self.matplot = MatplotFigure()
        self.matplot.figure = self.fig
        frame.add_widget(self.matplot)


        self.canvas = self.matplot.figcanvas

        #REMOVE AFTER CLEAN UP
        self.draw(0)


    def draw(self, data):
        logging.debug("View: Pie_frame: draw")
        plt.figure(self.fig.number)

        if isinstance(data, str):
            data = float(data.replace('%',''))
            if data != 0:
                data = data/100 + 1


        light_gray_value = .98
        light_gray = [light_gray_value, light_gray_value, light_gray_value]

        with_size = 0.2

        #if clear_before_drawing: #TODO implement with this input button
        self.axs.clear()

        if data != 0:
            display_text = ""
            if data>=1:
                outer_colors = [light_gray,self.default_color,light_gray]
                val2 = max(0, (data - 1) * 100) #Cant draw a negative amount in pie chart
                val1 = max(0, self.max_value - val2)
                val3 = val1 + val2
                
            else:
                outer_colors = [light_gray,[1,0.4,0.4],light_gray]
                val2 = max(0,(1 - data ) * 100) #Cant draw a negative amount in pie chart
                val3 = max(0, self.max_value - val2)
                val1 = val2 + val3 
            
            data1 = [val1,val2,val3]
            text_color = outer_colors[1]
            val2 = int(val2) #round to whole integer
            display_text = display_text + str(val2) + "%"
            
            self.axs.set_title(self.title, pad=0, y=0.95, 
                    fontdict={'fontsize': 15,
                            'fontweight': 'bold',
                            'color': 'k'})
            self.axs.pie(data1, radius=1, colors=(outer_colors),
                wedgeprops=dict(width=with_size*2, edgecolor='w'))
            self.axs.text(0.5, 0.5, display_text,
                    color= text_color,
                    horizontalalignment='center',
                    verticalalignment='center',
                    transform=self.axs.transAxes,
                    fontsize=20,
                    fontweight='bold')

            #data1 = np.array([1,2,2.8])
            #data2 = np.array([0.7,2.3,2.8])

            #inner_colors = [light_gray,'r',light_gray]

            #self.axs.pie(data2, radius=1-with_size, colors=inner_colors,
                #wedgeprops=dict(width=with_size, edgecolor='w'))

            plt.tight_layout()
        
        else:
            thin=0.05
            fade_black_val = 0.45
            fade_black = [fade_black_val, fade_black_val, fade_black_val]

            self.axs.set_title(self.title, pad=0, y=0.95, 
                    fontdict={'fontsize': 15,
                            'fontweight': 'bold',
                            'color': 'k'})
            self.axs.pie([1], radius=1, colors=([fade_black]),
                wedgeprops=dict(width=thin, edgecolor='w'))
            self.axs.pie([1], radius=1-thin, colors=([light_gray]),
                wedgeprops=dict(width=with_size*2, edgecolor='w'))
            #self.axs.pie([1], radius=1-thin-(with_size*2), colors=(['k']),
            #    wedgeprops=dict(width=thin, edgecolor='w'))
            self.axs.text(0.5, 0.5, '0%',
                    horizontalalignment='center',
                    verticalalignment='center',
                    transform=self.axs.transAxes,
                    fontsize=30,
                    fontweight='bold',
                    color=fade_black)

        self.canvas.draw()


    def set_default_color(self, color):
        self.default_color = color

    def set_refrence_color(self, color):
        self.refrence_color = color

    def set_max_value(self, max_value):
        self.max_value = max_value
