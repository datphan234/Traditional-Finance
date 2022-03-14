import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#List
Year=[]
Yearly_Income=[]
Yearly_Expenses=[]
Yearly_investment=[]
Annual_Returns=[]

#Assumption
income=input('Enter your income:')
expense=float(income)/2
interest_rate = input('Enter your interest rate:')
investment=float(income)/3
annual_return = float(investment)*float(interest_rate)
year=2021

#Append to the list
Year.append(year)
Yearly_Income.append(income)
Yearly_Expenses.append(expense)
Yearly_investment.append(investment)
Annual_Returns.append(annual_return)

#Loop for 'n' years
invested_year=input('Enter the number of year:')
for i in range(0,int(invested_year)-1):
	investment=investment+annual_return+float(income)/3
	annual_return=investment*float(interest_rate)
	Year.append(year+i+1)
	Yearly_Income.append(income)
	Yearly_Expenses.append(expense)
	Yearly_investment.append(investment)
	Annual_Returns.append(annual_return)

#Create a DataFrame
df=pd.DataFrame()
df['Year']=Year
df['Yearly_Income']=Yearly_Income
df['Yearly_Expenses']=Yearly_Expenses
df['Yearly_investment']=Yearly_investment
df['Annual_Returns']=Annual_Returns
print(df.round(1))
plt.plot(df['Year'],df['Yearly_Expenses'],label='Yearly Expenses')
plt.plot(df['Year'],df['Annual_Returns'],label='Annual Returns')
plt.title('Retire in '+str(invested_year)+ 'year')
plt.xlabel('Year')
plt.ylabel('USD')
plt.legend(loc='upper right')
plt.show()