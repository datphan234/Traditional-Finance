#Description: This programs uses the Money Flow Index to identify buy sell signals

#Libraries
import pandas as pd
import numpy as np
import yfinance as yf
import warnings
import matplotlib.pyplot as plt

stock_ticker='SPY'
#Get the data
df=yf.Ticker(stock_ticker).history(period='48mo').reset_index()
#Set the date to be the index
df=df.set_index(pd.DatetimeIndex(df['Date'].values))
#print(df)

#Visualize the data
#plt.plot(df['Close'],label='Close')
#plt.xlabel('Date')
#plt.ylabel('Close Price USD')
#plt.legend(loc='upper left')
#plt.show()

#Calculate the typical price
typical_price=(df['Close']+df['High']+df['Low'])/3

#Get the period
period=14

#Calculate the money flow
money_flow=typical_price*df['Volume']

#Get the positive and negative money flows
positive_flow=[]
negative_flow=[]

#Loop through the typical price
for i in range(1,len(typical_price)):
	if typical_price[i]>typical_price[i-1]:
		positive_flow.append(money_flow[i-1])
		negative_flow.append(0)
	elif typical_price[i]<typical_price[i-1]:
		negative_flow.append(money_flow[i-1])
		positive_flow.append(0)
	else:
		negative_flow.append(0)
		positive_flow.append(0)

#Get all the positive and negative money flows
positive_mf=[]
negative_mf=[]

for i in range(period-1,len(positive_flow)):
	positive_mf.append(sum(positive_flow[i+1-period:i+1]))
for i in range(period-1,len(negative_flow)):
	negative_mf.append(sum(negative_flow[i+1-period:i+1]))

#Calculate the money flow index
mfi=100-(100/((np.array(positive_mf)/np.array(negative_mf)+1)))

#Visualize MFI
df2=pd.DataFrame()
df2['MFI']=mfi

#plt.plot(df2['MFI'],label='MFI')
#plt.axhline(10,linestyle='--',color='lightgreen')
#plt.axhline(20,linestyle='--',color='lightgreen')
#plt.axhline(80,linestyle='--',color='tomato')
#plt.axhline(90,linestyle='--',color='tomato')
#plt.title('Money Flow Index')
#plt.ylabel('MFI Values')
#plt.legend(loc='upper left')
#plt.show()

#New Data Frame
new_df=pd.DataFrame()
new_df=df[period:]
new_df['MFI']=mfi
#print(new_df)

#Create a function for buy sell signals (you can create it straight to the data, I just want to practice my function skills)
def signal(data,high,low):
	buy_signal=[]
	sell_signal=[]

	for i in range(len(data['MFI'])):
		if data['MFI'][i]>high:
			sell_signal.append(data['Close'][i])
			buy_signal.append(np.nan)
		elif data['MFI'][i]<low:
			buy_signal.append(data['Close'][i])
			sell_signal.append(np.nan)	
		else:
			buy_signal.append(np.nan)
			sell_signal.append(np.nan)
	return(buy_signal,sell_signal)

#Add new columns(Buy&Sell)
new_df['Buy']=signal(new_df,80,20)[0]
new_df['Sell']=signal(new_df,80,20)[1]

#Visualize the data
plt.plot(df['Close'],label='Close Price',alpha=0.5)
plt.scatter(new_df.index,new_df['Buy'],color='green',label='Buy Signal',marker='^',alpha=1)
plt.scatter(new_df.index,new_df['Sell'],color='red',label='Sell Signal',marker='^',alpha=1)
plt.title(stock_ticker+' Buy and Sell Signals by Money Flow Index')
plt.xlabel('Date')
plt.ylabel('Close Price USD')
plt.legend(loc='upper left')
plt.show()










