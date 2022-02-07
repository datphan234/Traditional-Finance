import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import datetime as datetime
import numpy as np
from mpl_finance import candlestick_ohlc

yf.pdr_override()

smaUsed=[10,30,50]

start=dt.datetime(2020,1,1)- dt.timedelta(days=max(smaUsed))
now=dt.datetime.now()
stock=input('Enter the stock symbol: ')

while stock != 'quit':
	prices=pdr.get_data_yahoo(stock,start,now)

	fig, ax1=plt.subplots() #Create Plots

	for x in smaUsed: #calculates the SMAs for the stated periods and appends to dataframe
		sma=x
		prices['SMA_'+str(sma)]=prices.iloc[:,4].rolling(window=sma).mean()


	#calculate Bollinger Bands	
	BBperiod=15
	stdev=2
	prices['SMA'+str(BBperiod)]=prices.iloc[:,4].rolling(window=BBperiod).mean()
	prices['STDEV']=prices.iloc[:,4].rolling(window=BBperiod).std()
	prices['LowerBand']=prices['SMA'+str(BBperiod)]-(prices['STDEV']*2)
	prices['HigherBand']=prices['SMA'+str(BBperiod)]+(prices['STDEV']*2)
	prices['Date']=mdates.date2num(prices.index)

	#calculate 10.4.4 stochastic
	Period=10 #stochastic period
	K=4
	D=4
	prices['RolHigh']=prices['High'].rolling(window=Period).max()
	prices['RolLow']=prices['High'].rolling(window=Period).min()
	prices['stok']=((prices['Adj Close']-prices['RolLow'])/(prices['RolHigh']-prices['RolLow']))*100
	prices['K']=prices['stok'].rolling(window=K).mean()
	prices['D']=prices['K'].rolling(window=D).mean()
	prices['GD']=prices['High']
	ohlc=[]


	#delete extra dates
	prices=prices.iloc[max(smaUsed):] 

	greenDotDate=[]
	greenDot=[]
	lastK=0
	lastD=0
	lastLow=0
	lastClose=0
	lastLowBB=0


	#Go through price history to create candlestics and GD+Blue dots
	for i in prices.index:
		append_me=prices['Date'][i],prices['Open'][i],prices['High'][i],prices['Low'][i],prices['Adj Close'][i],prices['Volume'][i]
		ohlc.append(append_me)

		#check for green dots
		if prices['K'][i]>prices['D'][i] and lastK<lastD and lastK<60:
			plt.plot(prices['Date'][i],prices['High'][i]+1, marker='o',ms=4,ls='',color='g')

			greenDotDate.append(i)
			greenDot.append(prices['High'][i])

		#check for lower BB bounce
		if ((lastLow<lastLowBB) or (prices['Low'][i]<prices['LowerBand'][i])) and (prices['Adj Close'][i]>lastClose and prices['Adj Close'][i]>prices['LowerBand'][i]) and lastK<60:
			plt.plot(prices['Date'][i],prices['Low'][i]-1,marker='o',ms=4,ls='',color='b')

		#store values:
		lasK=prices['K'][i]
		lasD=prices['D'][i]
		lastLow=prices['Low'][i]
		lastClose=prices['Adj Close'][i]
		lastLowBB=prices['LowerBand'][i]

	#plot ma and BB
	for x in smaUsed:
		sma=x
		prices['SMA_'+str(sma)].plot(label='close')
	prices['HigherBand'].plot(label='close',color='lightgray')
	prices['LowerBand'].plot(label='close',color='lightgray')


	#plot candlesticks
	candlestick_ohlc(ax1, ohlc, width=.5, colorup='k', colordown='r', alpha=.75)

	ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
	ax1.xaxis.set_major_locator(mticker.MaxNLocator(8))
	plt.tick_params(axis='x', rotation=45)

	plt.show()