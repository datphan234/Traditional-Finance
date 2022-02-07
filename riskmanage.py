import pandas as pd
import yfinance as yf
import numpy as np
import datetime as dt
from pandas_datareader import data as pdr
import statistics
import time
import matplotlib.pyplot as plt

yf.pdr_override()
now = dt.datetime(2020,9,9)
start=dt.datetime(2019,1,1)

AvgGain=15 #Avg gain 15%
AvgLoss=5 #Avg loss 5%
smaUsed=[50,200]
emaUsed=[21]

stock=input('Enter the stock symbol: ')

while stock != 'quit':
	df=pdr.get_data_yahoo(stock,start,now)
	close=df['Adj Close'][-1]
	maxStop=close*((100-AvgLoss)/100)
	Target1R=round(close*((100+AvgGain)/100),2)
	Target2R=round(close*((100+(2*AvgGain))/100),2)
	Target3R=round(close*((100+(3*AvgGain))/100),2)

	for x in smaUsed:
		sma=x
		df['SMA_'+str(sma)]=round(df.iloc[:,4].rolling(window=sma).mean(),2)
	for x in emaUsed:
		ema=x
		df['EMA_'+str(ema)]=round(df.iloc[:,4].ewm(span=ema,adjust=False).mean(),2)

	sma50=round(df['SMA_50'][-1],2)
	sma200=round(df['SMA_200'][-1],2)
	ema21=round(df['EMA_21'][-1],2)
	low5=round(min(df['Low'].tail(5)),2)

	pf50=round(((close/sma50)-1)*100,2)
	check50=df['SMA_50'][-1]>maxStop
	pf200=round(((close/sma200)-1)*100,2)
	check200=((close/df['SMA_200'][-1])-1)*100>100

	pf21=round(((close/ema21)-1)*100,2)
	check21=df['EMA_21'][-1]>maxStop

	pf1=roun(((close/low5)-1)*100,2)
	check1=pf1>maxStop


	stock=input('Enter the stock symbol: ')
