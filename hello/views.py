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

def pred_bal(month,day):
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






