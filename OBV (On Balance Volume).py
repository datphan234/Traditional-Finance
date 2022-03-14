#Description: Use On Balance Volume (OBV) to give buy/sell signals

#Libraries
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt


#Get the data
df=yf.Ticker('SPY').history(period='12mo').reset_index()
#Set the date to be the index
df=df.set_index(pd.DatetimeIndex(df['Date'].values))
#print(df)

#Visualize the SPY
#plt.plot(df['Close'], label='Close')
#plt.title('SPY')
#plt.xlabel('Date')
#plt.ylabel('Price in USD')
#plt.show()

#OBV Calculation
OBV=[]
OBV.append(0)

for i in range(1,len(df.Close)):
	if df.Close[i]>df.Close[i-1]:
		OBV.append(OBV[-1]+df.Volume[i])
	elif df.Close[i]<df.Close[i-1]:
		OBV.append(OBV[-1]-df.Volume[i])
	else:
		OBV.append(OBV[-1])

#Add the OBV and OBV ema to df
df['OBV']=OBV
df['OBV_ema']=df['OBV'].ewm(span=20).mean()
print(df)

#Visualize the OBV
#plt.plot(df['OBV'], label='OBV')
#plt.plot(df['OBV_ema'], label='OBV_ema')
#plt.title('SPY OBV and OBV_ema')
#plt.xlabel('Date')
#plt.ylabel('USD')
#plt.show()

#Create a function to signal buy/sell
#If OBV > OBV_EMA Then Buy
#If OBV < OBV_EMA Then Sell
#Else Do Nothing

#signal=df,col1=OBV,col2=OBV_ema
def buy_sell(signal,col1,col2):
	sigBuy=[]
	sigSell=[]
	flag=-1
	for i in range(0,len(signal)):
		#If OBV>OBV_ema then buy
		if signal[col1][i]>signal[col2][i] and flag!=1:
			sigBuy.append(signal['Close'][i])
			sigSell.append(np.nan)
			flag=1
		#If OBV<OBV_ema then sell	
		elif signal[col1][i]<signal[col2][i] and flag!=0:
			sigSell.append(signal['Close'][i])
			sigBuy.append(np.nan)
			flag=0
		else:
			sigBuy.append(np.nan)
			sigSell.append(np.nan)
	return(sigBuy,sigSell)

#Create Buy and Sell columns
x=buy_sell(df,'OBV','OBV_ema')
df['Buy_Signal_Price']=x[0]
df['Sell_Signal_Price']=x[1]

#Visualize the Signals
plt.plot(df['Close'], label='Close',alpha=0.35)
plt.scatter(df.index,df['Buy_Signal_Price'],label='Buy Signal', marker='^',alpha=1,color='green')
plt.scatter(df.index,df['Sell_Signal_Price'],label='Sell Signal', marker='v',alpha=1,color='red')
plt.title('Buy and Sell Signals')
plt.xlabel('Date')
plt.ylabel('USD')
plt.legend(loc='upper left')
plt.show()
