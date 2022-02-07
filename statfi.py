import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import statistics
import numpy as np
import matplotlib.ticker as mticker
import yfinance as yf

yf.pdr_override()
year=1980
start =dt.datetime(year,1,1)
now=dt.datetime.now()

stock=input('Enter the stock symbol: ')

while stock != 'quit':
	fix, ax1=plt.subplots()

	df=pdr.get_data_yahoo(stock,start,now)

	sma=int(input('Enter a sma: '))
	limit=int(input('Enter warning limit: '))

	df['SMA'+str(sma)]=df.iloc[:,4].rolling(window=sma).mean()
	df['PC']=((df['Adj Close']/df['SMA'+str(sma)])-1)*100

	mean=df['PC'].mean()
	stdev=df['PC'].std()

	current=df['PC'][-1]
	yday=df['PC'][-2]

	print('mean:'+str(mean))
	print('stdev:'+str(stdev))

	bins=np.arange(-100,100,1)

	plt.xlim([df['PC'].min()-5,df['PC'].max()+5])

	plt.hist(df['PC'], bins=bins, alpha=0.5)

	plt.title(stock+'-- % From '+str(sma)+' SMA Histogram since '+str(year)) #set title
	plt.xlabel('Percent from '+str(sma)+ ' SMA (bin size=1)') #x axis title
	plt.ylabel('Count') #set y axis title

	plt.axvline(x=mean,ymin=0,ymax=1,color='k',linestyle='--')
	plt.axvline(x=mean+stdev,ymin=0,ymax=1,color='gray',linestyle='--')
	plt.axvline(x=mean+2*stdev,ymin=0,ymax=1,color='gray',linestyle='--')
	plt.axvline(x=mean+3*stdev,ymin=0,ymax=1,color='gray',linestyle='--')

	plt.axvline(x=mean-stdev,ymin=0,ymax=1,color='gray',linestyle='--')
	plt.axvline(x=mean-2*stdev,ymin=0,ymax=1,color='gray',linestyle='--')
	plt.axvline(x=mean-3*stdev,ymin=0,ymax=1,color='gray',linestyle='--')

	plt.axvline(x=current,ymin=0,ymax=1,color='r',label='price now')
	plt.axvline(x=yday,ymin=0,ymax=1,color='blue')

	ax1.xaxis.set_major_locator(mticker.MaxNLocator(14))

	fig2, ax2=plt.subplots()

	df=df[-150:]
	df['PC'].plot(label='close',color='k')
	

	plt.title(stock+'-- % From sma'+str(sma)+' Over the past 150 days ') #set title
	plt.xlabel('date') #x axis title
	plt.ylabel('Percent from' +str(sma)) #set y axis title

	ax2.xaxis.set_major_locator(mticker.MaxNLocator(8))
	plt.axhline(y=limit,xmin=0,xmax=1,color='r')
	
	plt.legend()
	plt.show()

