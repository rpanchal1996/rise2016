from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import pandas as pd
import json
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model

from .models import Usermodel
import os
os.chdir("/home/rudresh/Desktop/Rise Hackathon/webtechShitToPush/python-getting-started/hello/")
# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')




def register(request):
	if(request.method == 'POST'):
		username = request.POST.get('username')
		password = request.POST.get('password')
		customerID = request.POST.get('customerID')
		user = User.objects.create_user(username=username,password=password)
		user.set_password(password)
		user.save()
		new_user= Usermodel.objects.create(user=user,customerID=customerID)
		new_user.save()
		return render(request,'register.html',{})
	
	return render(request,'register.html')

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username,password=password)
		if user:
			login(request,user)
			return HttpResponseRedirect('/home')
		else:
			return HttpResponseRedirect('/invalidlogin')
			

	else:
		return render(request,'login.html',{})	

def post_login(request):
	if(request.user.is_authenticated()):
		user = request.user
		customerID = Usermodel.objects.get(user=user).customerID
		username = Usermodel.objects.get(user=user).user.username
		return render(request,'home.html',{'username':username})
	else:
		return HttpResponseRedirect('/login')

def invalidLogin(request):
	return render(request,'invalidLogin.html')

def pred_bal(month,day,acc):
	url = 'data/account'+str(acc)+'.json'
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
		
	print(new_df)
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
	return int(pred_bal(month,day,acc))-int(ballim)

def best_account(acc1_bal,acc1_lim,acc2_bal,acc2_lim,acc3_bal,acc3_lim,acc4_bal,acc4_lim):
	all_acs = {}
	all_acs[1] = acc1_bal - acc1_lim
	all_acs[2] = acc2_bal - acc2_lim
	all_acs[3] = acc3_bal - acc3_lim
	all_acs[4] = acc4_bal - acc4_lim
	return max(all_acs, key=all_acs.get)

def balance_options(request):

	to_transfer = 0
	best_account_val = 0
	dest_acc = 0
	if request.method == 'POST':
		month = 'Feb'
		day = 12
		acc1_bal = int(request.POST.get('acc1_bal'))
		acc1_lim = int(request.POST.get('acc1_lim'))
		acc2_bal = int(request.POST.get('acc2_bal'))
		acc2_lim = int(request.POST.get('acc2_lim'))
		acc3_bal = int(request.POST.get('acc3_bal'))
		acc3_lim = int(request.POST.get('acc3_lim'))
		acc4_bal = int(request.POST.get('acc4_bal'))
		acc4_lim = int(request.POST.get('acc4_lim'))
		
		acc2_bal = acc2_bal*1.3
		acc2_lim = acc2_lim*1.3
		acc3_bal = acc3_bal*1.12
		acc3_lim = acc3_lim*1.12
		acc4_bal = acc4_bal*1.07
		acc4_lim = acc4_lim*1.07
		
		flag1 = 0
		flag2 = 0 
		flag3 = 0
		flag4 = 0
		
		if(is_safe(month,day,1,acc1_lim)<0):
			flag1 = 1
		if(is_safe(month,day,2,acc2_lim)<0):
			flag2 = 1
		if(is_safe(month,day,3,acc3_lim)<0):
			flag3 = 1
		if(is_safe(month,day,4,acc4_lim)<0):
			flag4 = 1
		best_account_val = best_account(acc1_bal,acc1_lim,acc2_bal,acc2_lim,acc3_bal,acc3_lim,acc4_bal,acc4_lim)

		if(flag1):
			to_transfer = is_safe(month,day,1,acc1_lim)*-1
			dest_acc = 1
		
		if(flag2):
			to_transfer = is_safe(month,day,2,acc2_lim)*-1
			dest_acc = 2
		
		if(flag3):
			to_transfer = is_safe(month,day,3,acc3_lim)*-1
			dest_acc = 3
		
		if(flag4):
			to_transfer = is_safe(month,day,4,acc4_lim)*-1
			dest_acc = 4

		return render(request,'test.html',{'money':to_transfer,'from':best_account_val,'to':dest_acc})

	return render(request,'test.html',{'money':to_transfer,'from':best_account_val,'to':dest_acc})