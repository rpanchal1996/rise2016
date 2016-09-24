from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import pandas as pd
import json
from pandas.tools.plotting import scatter_matrix
from sklearn import datasets, linear_model
from twilio.rest import TwilioRestClient 
from .models import Usermodel
import requests
import json
import numpy as np
import matplotlib.pyplot as plt
import os
os.chdir("/home/ssm/Desktop/avais/rise2016/hello")
import random
# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

def after_login(request):
	f = open("data/account.json","r")
	for line in f:
		final_obj = line
	return render(request, "home.html", {"obj" : final_obj})

def analyse(fromAccount, toAccount, amount, balanceFrom, balanceTo):
	balanceFrom -= amount
	balanceTo += amount
	return HttpResponse("Chal gaya")
	return render(request, "dummy2.html", {"fromAccount" : fromAccount, "toAccount" : toAccount,
			"balanceFrom" : balanceFrom, "balanceTo" : balanceTo})

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
		analyse(best_account_val,dest_acc,to_transfer,678998,382176)
	return render(request,'test.html',{'money':to_transfer,'from':best_account_val,'to':dest_acc})

def sms(request):
	data = "Hello from Barclays."
	#+"We have set up an automated transfer to save funds, subject to your approval. Kindly verify the transaction."
 
	# put your own credentials here 
	ACCOUNT_SID = "AC1acb94e313c3487dddd3882107e2ca06" 
	AUTH_TOKEN = "33d8f22b974a208a17c392682c4b0b23" 
	 
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
	 
	client.messages.create(
		to="+919833175929", 
		from_="+18134387557", 
		body=data,
	)

	return render(request,'home.html',{'username':''})

def rudresh_change(request):
	stocks = [
		"Novavax, Inc.:$ 2.26",
		"Apple Inc.:$ 112.71",
		"Sirius XM Holdings Inc.:$ 4.205",
		"Yahoo! Inc.:$ 42.80",
		"Facebook, Inc.:$ 127.96",
		"Endo International plc:$ 23.39",
		"PowerShares QQQ Trust, Series 1:$ 118.33",
		"GoPro, Inc.:$ 17.15",
		"Microsoft Corporation:$ 57.43",
		"Frontier Communications Corporation:$ 4.33",
		"Cisco Systems, Inc.:$ 31.34",
		"VelocityShares Daily Inverse VIX Short Term ETN:$ 38.12",
		"Micron Technology, Inc.:$ 17.48",
		"Intel Corporation:$ 37.19",
		"Applied Materials, Inc.:$ 29.66"
	]
	index1 = random.randint(0,14)
	while True:
		index2 = random.randint(0,14)
		if index1 != index2:
			break
	while True:
		index3 = random.randint(0,14)
		if index3 != index2 and index3 != index1:
			break
	stocks_dict = {}
	stocks_dict["stock1"] = stocks[index1].split(":")[0]
	stocks_dict["stock2"] = stocks[index2].split(":")[0]
	stocks_dict["stock3"] = stocks[index3].split(":")[0]
	stocks_dict["cost1"] = stocks[index1].split(":")[1]
	stocks_dict["cost2"] = stocks[index2].split(":")[1]
	stocks_dict["cost3"] = stocks[index3].split(":")[1]
	return render("dummy3.html",{"stocks_dict" : stocks_dict})

def currency_prediction:
	gbparr = []
	usdarr = []
	chfarr = []
	nzdarr = []
	count =[]
	for date in xrange(1,31):
		if(date>9):
			url = 'http://api.fixer.io/2016-08-'+str(date)
		else:
			url = 'http://api.fixer.io/2016-08-0'+str(date)
		
		r = requests.get(url)
		r = r.json()
		
		gbparr.append(r['rates']['GBP'])
		usdarr.append(r['rates']['USD'])
		chfarr.append(r['rates']['CHF'])
		nzdarr.append(r['rates']['NZD']/1.5)
		count.append(date)

	for date in xrange(1,20):
		if(date>9):
			url = 'http://api.fixer.io/2016-09-'+str(date)
		else:
			url = 'http://api.fixer.io/2016-09-0'+str(date)
		
		r = requests.get(url)
		r = r.json()
		gbparr.append(r['rates']['GBP'])
		usdarr.append(r['rates']['USD'])
		chfarr.append(r['rates']['CHF'])
		nzdarr.append(r['rates']['NZD']/1.5)
		count.append(date+30)


	#m_sqr_usd =np.sum(((y-np.average(y))**2))
	#print(m_sqr_usd)
	usdy = np.array(usdarr)
	usdx = np.array(count)
	nzdy = np.array(nzdarr)
	nzdx = np.array(count)
	gbpy = np.array(gbparr)
	gbpx = np.array(count)
	chfy = np.array(chfarr)
	chfx = np.array(count)
	print(np.sum(((nzdy-np.average(nzdy))**2)))
	print(np.sum(((usdy-np.average(usdy))**2)))
	print(np.sum(((gbpy-np.average(gbpy))**2)))
	print(np.sum(((chfy-np.average(chfy))**2)))

	usdz = np.polyfit(usdx,usdy,4)
	nzdz = np.polyfit(nzdx,nzdy,4)
	gbpz = np.polyfit(gbpx,gbpy,4)
	chfz = np.polyfit(chfx,chfy,4)

	usdp = np.poly1d(usdz)
	nzdp = np.poly1d(nzdz)
	gbpp = np.poly1d(gbpz)
	chfp = np.poly1d(chfz)

	plt.plot(usdx,usdy,usdp(usdx),'-')
	plt.show()
	usddat = {}
	usdpred = {}
	nzddat = {}
	nzdpred = {}
	gbpdat = {}
	gbppred = {}
	chfdat = {}
	chfpred = {}

	for i in xrange(1,50):
		usddat[str(i)] = usdarr[i-1]
		nzddat[str(i)] = nzdarr[i-1]
		gbpdat[str(i)] = gbparr[i-1]
		chfdat[str(i)] = chfarr[i-1]
		usdpred[str(i)] = usdp(i)
		gbppred[str(i)] = gbpp(i)
		nzdpred[str(i)] = nzdp(i)
		chfpred[str(i)] = chfp(i)
