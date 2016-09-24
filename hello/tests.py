#from django.test import TestCase
# Create your tests here.
import pandas as pd
import json
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model

def pred_bal(month,day,acc):
	url = 'data/account'+str(acc)+'.json'
	print(url)
	df = pd.read_json(path_or_buf=url)
	df_jan = df.loc[df['month']==month]
	till_now = 500000
	columns = ['Bal']
	count = 1
	new_df = pd.DataFrame(columns=columns)
	for index, row in df_jan.iterrows():
		if(row['transaction']==0):
			till_now = till_now+row['amount']
		else:
			till_now = till_now-row['amount']
		
		temp_df = pd.DataFrame({'Bal':[till_now],'number':row['date']})
		
		new_df = new_df.append(temp_df)
		count = count+1
		
	#print(new_df)
	x = new_df.number.values
	X = x.reshape(count-1,1)
	y = new_df.Bal.values
	Y = y.reshape(count-1,1)

	regr = linear_model.LinearRegression()
	regr.fit(X,Y)
	#plt.scatter(x, y,  color='black')
	#plt.plot(X, regr.predict(X), color='blue', linewidth=3)
	#plt.xticks(())
	#plt.yticks(())
	#plt.show()
	#print(regr.predict(day))

	return (regr.predict(day)) 

def is_safe(month,day,acc,ballim):
	return pred_bal(month,day,acc)-ballim

def best_account(acc1_bal,acc1_lim,acc2_bal,acc2_lim,acc3_bal,acc3_lim,acc4_bal,acc4_lim):
	all_acs = {}
	all_acs[1] = acc1_bal - acc1_lim
	all_acs[2] = acc2_bal - acc2_lim
	all_acs[3] = acc3_bal - acc3_lim
	all_acs[4] = acc4_bal - acc4_lim
	return max(all_acs, key=all_acs.get)

def balance_options(request):
	
	acc1_bal
	acc1_lim
	acc2_bal = acc2_bal*1.3
	acc2_lim = acc2_lim*1.3
	acc3_bal = acc3_bal*1.12
	acc3_lim = acc3_lim*1.12
	acc4_bal = acc4_bal*0.015
	acc4_lim = acc4_lim*0.015
	flag1 = 0
	flag2 = 0 
	flag3 = 0
	flag4 = 0
	
	if(is_safe(month,day,1)<0):
		flag1 = 1
	if(is_safe(month,day,2)<0):
		flag2 = 1
	if(is_safe(month,day,3)<0):
		flag3 = 1
	if(is_safe(month,day,4)<0):
		flag4 = 1
	best_account = best_account(acc1_bal,acc1_lim,acc2_bal,acc2_lim,acc3_bal,acc3_lim,acc4_bal,acc4_lim)

	if(flag1):
		to_transfer = is_safe(month,day,1)
		source_acc = 1
	
	if(flag2):
		to_transfer = is_safe(month,day,1)
		source_acc = 1
	
	if(flag3):
		to_transfer = is_safe(month,day,1)
		source_acc = 1
	
	if(flag4):
		to_transfer = is_safe(month,day,1)
		source_acc = 1

print(is_safe('Feb',12,2,500000))
