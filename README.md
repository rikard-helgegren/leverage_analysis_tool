# LAT - Leverage Analysis Tool

This is an analyzing tool for gaining understanding if and how leveraged instruments
can be used to build an investment portfolio that matches ones preferences. The tool is
still under construction.


### How to run

Run the application by executing leverage_analysis_tool.py

```
python3 leverage_analysis_tool.py
```

*NOTE*: Does not work at windows currently. 

### Required libraries

Beyond Python3 standard libraries this program also requires:

* numpy
* matplotlib
* tkinter

### Data

Data files are not included due to copy write uncertainties but can be downloaded at

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

### Disclaimer

Historical returns are no guarantee of future returns. An investment in securities or funds can both increase and decrease in value,
and you may not get the invested capital back.
