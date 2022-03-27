from tkinter import *
from  tkinter import ttk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from tkinter import messagebox

class View(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        print("TRACE: View: __init__")

        # create controller
        self.controller = None


        ######################
        # create widgets
        ######################

        self.frame1 = Frame(self, padx=5, pady=5)
        self.frame1.pack(side=LEFT)
        self.checkbutton_fee_state = IntVar()
        self.checkbutton = Checkbutton(self.frame1, text="Include Fees", variable=self.checkbutton_fee_state, command=self.update_fee_status)
        self.checkbutton.pack()

        self.label = Label(self.frame1, text='Years')
        self.label.pack()

        #Spinbox
        self.spin = Spinbox(self.frame1, from_=0, to=100, width=5,command=self.update_limit)
        self.spin.pack()

        #Slide
        self.scale = Scale(self.frame1, from_=0, to=100, orient='horizontal', command=self.update_amount)
        self.scale.pack()


        ##### Histogram #####

        self.frame2 = Frame(self, padx=5, pady=5)
        self.frame2.pack(side=LEFT)
        # specify the window as master
        self.histogram_fig = plt.figure(figsize=(4, 5))
        self.histogram_canvas = FigureCanvasTkAgg(self.histogram_fig, master=self.frame2)
        self.histogram_canvas.draw()
        self.histogram_canvas.get_tk_widget().pack()

        # navigation toolbar
        self.histogram_toolbarFrame = Frame(master=self.frame2)
        self.histogram_toolbarFrame.pack()
        self.histogram_toolbar = NavigationToolbar2Tk(self.histogram_canvas, self.histogram_toolbarFrame)
        self.histogram_toolbar.pack(side=BOTTOM)

        ##### Line Graph #####

        self.frame3 = Frame(self, padx=5, pady=5)
        self.frame3.pack(side=LEFT)
        # specify the window as master
        self.line_graph_fig = plt.figure(figsize=(4, 5))
        self.line_graph_canvas = FigureCanvasTkAgg(self.line_graph_fig, master=self.frame3)
        self.line_graph_canvas.draw()
        self.line_graph_canvas.get_tk_widget().pack()

        # navigation toolbar
        self.line_graph_toolbarFrame = Frame(master=self.frame3)
        self.line_graph_toolbarFrame.pack()
        self.line_graph_toolbar = NavigationToolbar2Tk(self.line_graph_canvas, self.line_graph_toolbarFrame)
        self.line_graph_toolbar.pack(side=BOTTOM)

       
        #Table of Stock Markets

        self.frame4 = Frame(self, padx=5, pady=5)
        self.frame4.pack(side=LEFT)
        #scrollbar
        game_scroll = Scrollbar(self.frame4)
        game_scroll.pack(side=RIGHT, fill=Y)

        game_scroll = Scrollbar(self.frame4,orient='horizontal')
        game_scroll.pack(side=BOTTOM,fill=X)

        columns = ('index', 'country', 'leverage')

        self.market_table = ttk.Treeview(self.frame4,yscrollcommand=game_scroll.set, xscrollcommand =game_scroll.set, columns=columns, show='headings')
        self.market_table.heading('index', text='Index')
        self.market_table.heading('country', text='Country')
        self.market_table.heading('leverage', text='Leverage')
        self.market_table.pack()
        self.market_table.bind('<<TreeviewSelect>>',self.table_item_selected)



    ###############
    # Commands
    ###############

    def set_controller(self, controller):
        print("TRACE: View: set_controller")
        self.controller = controller

    def update_fee_status(self):
        print("TRACE: View: update_fee_status")
        print("View, fee_status:", self.checkbutton_fee_state.get())
        self.controller.update_fee_status(self.checkbutton_fee_state.get())
        messagebox.showinfo('Error', 'Not fully implemented')
    
    def update_limit(self):
        print("TRACE: View: update_limit")
        messagebox.showinfo('Error', 'Not fully implemented')
        #TODO

    def update_amount(self, value):
        print("TRACE: View: update_amount")
        messagebox.showinfo('Error', 'Not fully implemented')
        #TODO


    def draw_histogram(self, data):
        print("TRACE: View: draw_histogram")
        plt.figure(self.histogram_fig.number)

        if data != []:
            plt.hist(data)

        self.histogram_canvas.draw()

    def draw_line_graph(self, data):
        print("TRACE: View: draw_line_graph")
        plt.figure(self.line_graph_fig.number)

        if data != []:
            plt.plot(data)

        self.line_graph_canvas.draw()

    def set_market_table(self, markets):
        print("TRACE: View: set_market_table")

        for market in markets:
            self.market_table.insert(parent='', index=END, values=(market, ))

    def table_item_selected(self, _ ):
        curItem = self.market_table.focus()
        print ("selected item in table",self.market_table.item(curItem))
