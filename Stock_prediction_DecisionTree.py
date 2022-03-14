# This program applies Machine Learning Decision Tree to predict the stock price

#Libraries
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

#Get the data
Stock_ticker='SPY'
df=yf.Ticker(Stock_ticker).history(period='max').reset_index()
df=df.set_index(pd.DatetimeIndex(df['Date'].values))
df.index.name='Date'
#print(df)

#Manipulate the data
df['Price_Up']=np.where(df['Close'].shift(-1)>df['Close'],1,0)
df=df.drop(columns=['Date','Open','High','Low'])
#print(df)

#Split the data set in feature and target data set
X=df.iloc[:,0:df.shape[1]-1].values
Y=df.iloc[:,df.shape[1]-1].values

#Split the data into 80% training, 20% testing
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2)

#Create and train the model (Decision Tree)
tree=DecisionTreeClassifier().fit(X_train,Y_train)

#Show how well the model did
print(tree.score(X_test,Y_test))

#Show the model predictions
tree_predictions=tree.predict(X_test)
print(tree_predictions)

#Show the actual values
print(Y_test)
