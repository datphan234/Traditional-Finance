import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf

yf.pdr_override()
start=dt.datetime(1980,12,1)
now=dt.datetime(2020,3,18)
stock=''

stock=input('Enter the stock symbol: ')
while stock != 'quit':
	df=pdr.get_data_yahoo(stock,start,now)
	df.drop(df[df['Volume']<1000].index, inplace=True)

	dfmonth=df.groupby(pd.Grouper(freq='M'))['High'].max()

	glDate=0
	lastGLV=0
	currentDate=''
	currentGLV=0

	for index, value in dfmonth.items():
		if value>currentGLV:
			currentGLV=value
			currentDate=index
			counter=0
		if value<currentGLV:
			counter=counter+1

			if counter==3 and ((index.month != now.month and index.year != now.year)) :
				if currentGLV != lastGLV:
					print(currentGLV)
				glDate=currentDate
				lastGLV=currentGLV
				counter=0
	if lastGLV==0:
		message=stock+' has not formed a GL'
	else:
		message=('Last GL: '+str(lastGLV)+' on '+str(glDate))

	print(message)

	stock=input('Enter the stock symbol: ')

