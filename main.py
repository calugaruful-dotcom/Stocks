import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

#define the ticker symbol
SnP500 = 'SPY'
SPY = yf.Ticker('SPY')

class Stock:

    class StockPeriod:
        def __init__(self, stock, startdate, enddate):
            self.ticker = stock
            self.start = startdate
            self.end = enddate
            self.download = 0
            self.datecounter = 0
            self.minprice = 100000
            self.mindate = 0
            self.maxprice = 0
            self.maxdate = 0
            self.dates = []
            self.close = []

        def downloadPeriodData(self):
            self.download = yf.download(str(self.ticker), start=str(self.start), end=str(self.end))
            return self.download

        def toString(self):
            self.datecounter = 0
            for index, row in self.download.iterrows():
                date_str = str(index)
                self.dates.append(date_str)
                self.close.append(round(float(row['Close']), 2))

            for item in self.close:
                self.datecounter += 1
                if item < self.minprice:
                    self.minprice = item
                    self.mindate = self.datecounter - 1
                if item > self.maxprice:
                    self.maxprice = item
                    self.maxdate = self.datecounter - 1

            print(self.start[0:7] + ' Low Date: ' + self.dates[self.mindate])
            print(self.start[0:7] + ' Low Price: ' + str(self.minprice))
            print(self.start[0:7] + ' High Date: ' + self.dates[self.maxdate])
            print(self.start[0:7] + ' High Price: ' + str(self.maxprice))
            run = self.maxdate - self.mindate
            rise = self.maxprice - self.minprice
            slope = rise / run
            print(self.start[0:7] + ' slope: ' + str(slope))
            print('')

    class StockToDate:
        def __init__(self, stock, period, timeint):
            self.ticker = stock
            self.period = period
            self.timeint = timeint
            self.close = []
            self.dates = []
            self.datecounter = 0
            self.minprice = 100000
            self.mindate = 0
            self.maxprice = 0
            self.maxdate = 0
            self.download = 0
            self.rmins = []
            self.rmax = []
            self.maxima =[]
            self.minima = []
            self.sma30 = pd.DataFrame()

        def downloadToDateData(self):
            self.download = yf.download(str(self.ticker), period=str(self.period), interval=str(self.timeint))
            return self.download

        def calcCloseAndDates(self):
            self.datecounter = 0
            for index, row in self.download.iterrows():
                date_str = str(index)
                self.dates.append(date_str)
                self.close.append(round(float(row['Close']), 4))

        def FindMaxima(self):
            length = len(self.close)
            if length >= 2:
                if self.close[0] > self.close[1]:
                    self.maxima.append(self.close[0])

                if length > 3:
                    for i in range(1, length - 1):
                        if self.close[i] > self.close[i - 1] and self.close[i] > self.close[i + 1]:
                            self.maxima.append(self.close[i])

                if self.close[length - 1] > self.close[length - 2]:
                    self.maxima.append(self.close[length - 1])
            return self.maxima

        def FindMinima(self):
            length = len(self.close)
            if length >= 2:
                if self.close[0] > self.close[1]:
                    self.minima.append(self.close[0])

                if length > 3:
                    for i in range(1, length - 1):
                        if self.close[i] < self.close[i - 1] and self.close[i] < self.close[i + 1]:
                            self.minima.append(self.close[i])

                if self.close[length - 1] < self.close[length - 2]:
                    self.minima.append(self.close[length - 1])
            return self.minima

        def PlotData(self,input,type):
            today = date.today()
            self.input = input
            self.type = type
            plt.figure(figsize=(12.5, 4.5))
            plt.plot(self.input, label={self.ticker})
            plt.title(self.ticker + ' ' + self.type + ' stock history to date in ' + self.timeint)
            plt.xlabel(self.period + ' ' + str(today))
            plt.ylabel(self.type + 'Price $')
            plt.show()

        def SimpleMovingAverage(self, list, window=30):
            list = self.GetClosePrice()
            sma = pd.DataFrame(list)
            sma30 = sma.rolling(window).mean()
            return sma30

        def GetClosePrice(self):
            return self.close

snpJan20 = Stock.StockPeriod('SPY', '2020-01-01', '2020-01-31')
snpJan20.downloadPeriodData()
snpJan20.toString()

testtodate = Stock.StockToDate('SPY', '365d', '1d')
testtodate.downloadToDateData()
testtodate.calcCloseAndDates()
max = testtodate.FindMaxima()
min = testtodate.FindMinima()


plt.figure(figsize=(12.5, 4.5))
closeprice = testtodate.GetClosePrice()

# sma = pd.DataFrame(closeprice)
# sma2 = sma.rolling(window=30).mean()
# sma3 = sma.rolling(window=100).mean()
#
# plt.plot(sma2, 'r')
# plt.plot(sma3, 'b')
# plt.plot(sma, 'g')
# plt.show()
SMA30 = testtodate.SimpleMovingAverage(closeprice)
plt.plot(SMA30, 'g')
plt.plot(closeprice, 'r' )
plt.show()