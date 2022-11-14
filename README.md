# LAT - Leverage Analysis Tool

LAT is an analyzing tool for gaining understanding if and how leveraged instruments
can be used to build an investment portfolio that matches ones preferences. The tool is
still under construction.

![Image of screenshot of application](/images/Sample.png)

### Background

Development of this application was started after a series increasingly more realistic models. Experiment with the previous model resulted in a whitepaper, concluding that leveraged instruments could increase the expected returns of a portfolio. This application will enable non-programmes to experiment with leveraged certificates, and allow different strategies for buying and selling the certificates in order to minimize risk or to increase returns.

<kbd>
<img src="/images/Leveraged_Certificates.png" alt="Whitepaper first page" width="50%"/>
</kbd>

### How to run

Run the application by executing Makefile

```
make
```

This compiles the C++ files, and then runs the program.

*NOTE*: The program does not work with Windows currently.

### Required libraries

Beyond Python3 standard libraries this program also requires:

* numpy
* matplotlib
* tkinter

and c++ compilator

* g++

### Walktrhough

To get started select a market by clicking on a market in the top right table. Unfold the levereaged products by klicking the arrow to the left of the market, and then select desiered leverage.

To the left are widgits to change input parameters and strategy. And in the middle is a histogram which displays the distribution of outcomes of the portfolio when investing for *Years Investing*, and a graph showing the performance from *Start date* to *End date*. 

### Data

Data files are not included due to copyright uncertainties but can be downloaded at

* https://www.investing.com/
* https://www.kaggle.com/

The data should be stored as csv files and need to have a specific format, this is checked in the beginning of the program.

Filename: *Index* *Country*.csv \
First row: Date, Close, Open \
Following rows: *Date value*, *Close value*, *Open value*

e.g.

SP500 USA.csv

```
Date, Close, Open
20220103, 3, 2
20220102, 2, 1
20220101, 1, 0
```

The file path is set in *src/model/constants*

### Disclaimer

Historical returns are no guarantee of future returns. An investment in securities or funds can both increase and decrease in value,
and you may not get the invested capital back.

### Goal

In the end the graphical user interface will be built by using Kivy (https://kivy.org/) to achieve something in this style:

![Image of design goal](/images/Goal.jpeg)


But during development of the model tkinter will be used to swiftly test and experiment with the model.

The aim is to make a tool for both beginner and experts where there are two display options. One simplistic with only the most important features and values viewable. And one with all controls and all statistical performance meters.

### Help out

If you would like to contribute, tasks for further development can be found in the project boards linked to this repository.

(https://github.com/rikard-helgegren/leverage_analysis_tool/projects)
