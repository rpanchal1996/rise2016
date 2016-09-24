from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


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






