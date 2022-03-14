#Description: This program uses the Bollinger Band to signal buy sell

#Libraries
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

#Get the data
Stock_ticker='SPY'
df=yf.Ticker(Stock_ticker).history(period='24mo').reset_index()
#Set the date to be the index
#df=df.set_index(pd.DatetimeIndex(df['Date'].values))
#print(df)

#Calculate the SMA, STD, upper and lower band
period=50
df['SMA']=df['Close'].rolling(window=period).mean()
df['STD']=df['Close'].rolling(window=period).std()
df['Upper_Band']=df['SMA']+(2*df['STD'])
df['Lower_Band']=df['SMA']-(2*df['STD'])

#Create a new list
column_list=['Close','SMA','Upper_Band','Lower_Band']


#Create a function for buy and sell signal
def signal(data):
	buy_signal=[]
	sell_signal=[]
	for i in range(len(data['Close'])):
		if data['Close'][i]>data['Upper_Band'][i]:
			sell_signal.append(data['Close'][i])
			buy_signal.append(np.nan)
		elif data['Close'][i]<data['Lower_Band'][i]:
			buy_signal.append(data['Close'][i])
			sell_signal.append(np.nan)
		else:
			buy_signal.append(np.nan)
			sell_signal.append(np.nan)
	return(buy_signal,sell_signal)		


#Add 2 new colums
df['Buy']=signal(df)[0]
df['Sell']=signal(df)[1]

#Plot the data
plt.plot(df['Date'],df['Close'],color='orange',label='Close Price')
#plt.plot(df['Date'],df['SMA'],color='blue')
plt.plot(df['Date'],df['Upper_Band'],color='lightblue')
plt.plot(df['Date'],df['Lower_Band'],color='lightblue')
plt.fill_between(df['Date'],df['Upper_Band'],df['Lower_Band'],color='lightblue',alpha=0.1)
plt.scatter(df['Date'],df['Buy'],marker='^',color='green',label='Buy')
plt.scatter(df['Date'],df['Sell'],marker='^',color='red',label='Sell')
plt.title('Bollinger Band for ' +Stock_ticker)
plt.ylabel('USD Price')
plt.legend(loc='upper left')
plt.show()




