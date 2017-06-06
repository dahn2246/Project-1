Dow30 Project - Last updated 5 June 2017

************************************Reading********************************
This Python project performs analysis on stocks in the Dow Jones Industrial Index. The
program includes earnings data (collected from www.stockrow.com) and stores this in a
sqlite3 database. With this earnings data, this program gives users data on financial ratios
such as Price/Earnings, Price/Book, Return on Invested Capital, etc. 

Furthermore, the program performs multiple linear analysis between average price for three
months and earnings data such as revenue, earnings per share, dividends, etc. This analysis
gives a regressed stock price which can be seen as a target price for the three month period
between earnings quarter. The multiple linear analysis is performed as follows:

|1, Revenue_Q1, EPS_Q1, Dividends_Q1|    |coefficient1|    |Price_Q1|
|1, Revenue_Q2, EPS_Q2, Dividends_Q2| *  |coefficient2| =  |Price_Q2|
|1, Revenue_Q3, EPS_Q3, Dividends_Q3|    |coefficient3|    |Price_Q3|
.....

As seen, the multiple linear regression takes form in X * Coff = Y. As of yet, residual analysis
or confidence interval analysis has not been done. 

**********************************User Guide*********************************
Run main.py as is to get analysis of all stocks from Dow Jones Industrial Index. 

To update stock information, uncomment these two lines: 
#             Download.updateHistoricalPrice(i)
#             update(i)
and run. 

**********************************Warning***********************************
Use dow 30 stock analysis at your own risk. The creator is not resonsible for any loss
of profit or any other types of loses. 




