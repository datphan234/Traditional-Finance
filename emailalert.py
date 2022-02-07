import os
import smtplib
import imghdr
from email.message import EmailMessage
import time

import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr

EMAIL_ADDRESS= 'phanbuiquocdat@gmail.com'
EMAIL_PASSWORD= 'baqhmovfmvrnngvq'

msg=EmailMessage()

yf.pdr_override()
start=dt.datetime(2018,12,1)
now=dt.datetime.now()

stock='QQQ'
TargetPrice=396

msg['Subject']='Alert on'+stock
msg['From']= EMAIL_ADDRESS
msg['To']= 'saigonfilm69@gmail.com'

alerted=False

while 1:
	
	df=pdr.get_data_yahoo(stock,start,now)
	currentClose=df['Adj Close'][-1]

	condition=currentClose>TargetPrice
	if(condition and alerted==False):
		alerted=True

		message= stock+' has reached the price of '+str(TargetPrice)+\
		'\nCurrent Price: '+str(currentClose)
		
		msg.set_content(message)

		with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
			smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
			smtp.send_message(msg)

	else:
		print('no new alerts')
	time.sleep(5)

