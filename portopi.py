import pandas as pd
from pandas_datareader import data as web
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

#FAANG
assets=['FB','NFLX','AAPL','AMZN','GOOGL','MSFT', 'TSLA']
assets2=['BTC-USD','ETH-USD']

#WEIGHTING
weights=np.array([0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.2])
weights2=np.array([0.5,0.5])

startdate='2013-01-01'
enddate=datetime.today().strftime('%Y-%m-%d')

#dataframe
df=pd.DataFrame()

for stock in assets:
	df[stock]=web.DataReader(stock,data_source='yahoo',start=startdate,end=enddate)['Adj Close']

'''for c in df.columns.values:
	plt.semilogy(df[c],label=c)
plt.title('Portfolio Price History')	
plt.xlabel('Date')
plt.ylabel('Price in USD')
plt.legend(df.columns.values, loc='upper left')	
plt.show()'''

#Daily return
dailyreturns=df.pct_change()

#Annualized covariance matrix
annual_cov_maxtrix=dailyreturns.cov()*252

#Portfolio variance
port_variance=np.dot(weights.T,np.dot(annual_cov_maxtrix,weights))

#Portfolio volatility or standard deviation
port_volatility = np.sqrt(port_variance)

#Annual portfolio return
annual_port_return=np.sum(dailyreturns.mean()*weights)*252

#Show the annual return, volatility (risk), variance
percent_var=str(round(port_variance,2)*100)+'%'
percent_vol=str(round(port_volatility,2)*100)+'%'
percent_return=str(round(annual_port_return,2)*100)+'%'
'''
print('Expected annual return:'+percent_return)
print('Annual volatility/risk:'+percent_vol)
print('Annual variance:'+percent_var)'''

#Portfolio Optimization!!!
#Expected returns and Covariance matrix
mu=expected_returns.mean_historical_return(df)
S=risk_models.sample_cov(df)

#Optimizing max sharpe ratio
ef=EfficientFrontier(mu,S)
weights=ef.max_sharpe()
clean_weights=ef.clean_weights()
print(clean_weights)
ef.portfolio_performance(verbose=True)



