# LAT - Leverage Analysis Tool

LAT is an analyzing tool for gaining understanding if and how leveraged instruments
can be used to build an investment portfolio that matches ones preferences. The tool is still under construction.

![Screenshot sample of the application](/images/sample-Kivy.png)

### Background

Development of this application was started after a series increasingly more realistic models. Experiment with the previous model resulted in a whitepaper, concluding that leveraged instruments could increase the expected returns of a portfolio. This application will enable non-programmes to experiment with leveraged certificates, and allow for different strategies of buying and selling the certificates in order to minimize risk or to increase returns.

<kbd>
<img src="/images/Leveraged_Certificates.png" alt="Whitepaper first page" width="50%"/>
</kbd>

### How to run

Run the application by executing the Makefile

```
make
```

This compiles the C++ files, and then runs the program.

*NOTE*: The program does not work with Windows currently. Please use Linux or Mac.

### Required libraries

Beyond Python3 standard libraries this program also requires:

* numpy
* matplotlib
* kivy
* kivymd
* simplejson
* seaborn

and c++ compilator

* g++

run `sudo make install` all needed requirements,
or `pip3 install -r requirements.txt` to install all pip requirements without sudo. 

### Project structure
For getting an undestanding of this code you are recomended to start with leverage_analysis_tool.py, and then Model.py and View.py.

### Walkthrough

To get started select a market by clicking on a row with a market in the bottom left table. The leverage is selected by the column number of your click.

To the top left are widgits to change input parameters and strategy. And in the middle is a histogram which displays the distribution of outcomes of the portfolio when investing for a selected amount of years (default is one year). There is also a graph showing the performance from the start date to the end date, which can be specefied benath the graph.

Metrics of the portfolios performance is displayed on the righten side of the application.

### Intro to the application

![Image of the applicatioin with numbers for refrence of specific parts](/images/GUI-numbers.png)

1. 
    Leverage slider: A slider, to set what procentage of the whole portfolio that is made out of leveraged products. E.g. a value of 10 means, 90% is pure index (leverage 1) and 10% is leveraged products (leverage 2 and above).

    Include fees: A toggle, to turn on and off if fees like spread, the daily fee and brokarage should be included in the model.

    Time investing: A text field, to enter investment horizon (years). It is on this intervall all performance metrics (9) will be calculated. It will also be the length of each run in the histogram (4). E.g. a value of 2 will calculate mean and median yeilds based of a 2 year investment period

    Loan: A text field for specifying how much to loan. To leveraging your investment in that way. This is a one time loan that is done at the first day of your investment period, and it is returned the last day of investment, with interest.

2. Strategy menue:

    Hold: No rebalances nor purcheses are made to the portfolio

    Rebalance time: The portfolio is rebalanced regurarly, by default each 6 month. A rebalance means to set leverage 1 instrument and instrument with leverage greater than 1 to their initial proportions.

    Harvest/Refill: A leverage instrument is rebalanced if it reaches a higher or lower limit. Default levels for rebalance are 150% or 50% of the instruments initial value

    Do not invest: A investmentstrategy which is not exposed to the market

    Variance: Lerveraged instruments are sold, if the variance of the underlying market have a too big of a variance, and then bought again when the volatility is lower. While the instruments are whitdrawn their worth is not reinvested in the mean time.

3. List of leveraged instruments: the underlying market changes by row and the leverage of the instrument increase by the column. Green check marks indicates which instruments are used for the portfolio.

4. Trades: If the strategy selected does purches or sells of leveraged products, or rebalancing of the portfolio. Then activating trades show a marker in the graph for that trade. A green marker is used when buying more leveraged products and read markers for selling. A yellow marker is used if one instrument is bought and an other is sold. 

    Clear: Deselect all instruments of the current portfolio.

    Pause: Pause calculations and updates. This could be used if one wants to create a complex portfolio without the program running for each incremental update. (This is a temporary button, and wil be removed when the program runns smother)

5. Histogram: Each colum shows a specific outcome. E.g. the column at 1.1 is the outcome of 10% positive return, and the colum of 0.9 is the outcome of 10% negative return. The hight of the column shows how common this outcome has been in the selected time interval, the higher the more common. The purpose of the histogram is to show the distribution of the outcomes.

6. Graph: The graph shows how the portfolio would have performed in a given historical time period, day by day. This can be used to see how volatile, rewarding, and resilliant the portfolio is.

7. Time window: Set the start date and end date for what time interval you want to use for the analysis. If a field is left empty, the day used for that fields are selected to the very first day and the very last day, respectively

8. Pie charts: A few key performance indicators shown in a quick visual way. All these values are based of the data in the histogram

    Mean: This value is under strong influence of a few good time periods.

    Median: The mean return is based of all outcomes shown in the histogram.

    Risk: The probability of negative outcomes multiplied by the severity of the loss.

9. Table of performace indicators:
Various metrics that could be used to make a informed evaluation of the investment strategy.

### Data

The data included are not the historical data of actual markets indeces, but rather fabricated to behave similar to the market index they try to represent.

For correct historical data, go to the following websites to download data

* kaggle.com
* finance.yahoo.com

The data should be stored as csv files and need to have a specific format, see below. This format is checked in the beginning of the programs execution.

Filename: *Index* *Country*.csv \
First row: Date,Value \
Following rows: *Date value*,*Market value*

e.g.

SP500 USA.csv

```
Date,Value
20220103,3
20220102,2
20220101,1
```

The file path to the data folder is set in the file *src/model/constants_model.py*

### Disclaimer

Historical returns are no guarantee of future returns. An investment in securities or funds can both increase and decrease in value, and you may not get the invested capital back.

### Goal & Journey

The project started out buy geting the logic in place and making a proof of consept, by using Tkinter as the GUI toolkit. But the goal was all along to change graphical toolkit to something more pleasing, if I managed to get that far without dropping the project.

![Image of the applicatioin when using Tkinter](/images/sample-Tkinter.png)

This phase is now past and the program is now built by using Kivy (https://kivy.org/). At the start of the project I wanted to achieve something in the following style. And it is still my northern star, though Kivy adds a few struggels in dark mode.

![Image of design goal](/images/Goal.jpeg)


The aim is to make a tool for both beginner and experts where there are two display options. One simplistic with only the most important features and values viewable. And one with all controls and all statistical performance meters.
