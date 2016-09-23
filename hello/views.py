from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout



from .models import Greeting
from .models import Coder
from .models import Helper

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

def registerCoder(request):
	if(request.method == 'POST'):
		username = request.POST.get('username')
		fname = request.POST.get('fname')
		lname = request.POST.get('lname')
		password = request.POST.get('password')
		semester = request.POST.get('semester')
		user = User.objects.create_user(username=username,password=password,first_name=fname,last_name=lname)
		user.set_password(password)
		user.save()
		new_user=Coder.objects.create(user=user,semester=semester)
		new_user.save()
		return render(request,'registerCoder.html',{})
	
	return render(request,'registerCoder.html')
def registerHelper(request):
	if(request.method == 'POST'):
		username = request.POST.get('username')
		fname = request.POST.get('fname')
		lname = request.POST.get('lname')
		password = request.POST.get('password')
		semester = request.POST.get('semester')
		user = User.objects.create_user(username=username,password=password,first_name=fname,last_name=lname)
		user.set_password(password)
		user.save()
		new_user=Helper.objects.create(user=user,experience=semester)
		new_user.save()
		return render(request,'registerHelper.html',{})
	return render(request,'registerHelper.html')

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
		semester = Coder.objects.get(user=user).semester
		user_fname = str(Coder.objects.get(user=user).user.first_name)
		user_lname = str(Coder.objects.get(user=user).user.last_name)
		return render(request,'home.html',{'semester':semester,'lname':user_lname,'fname':user_fname})
	else:
		return HttpResponseRedirect('/login')

def invalidLogin(request):
	return render(request,'invalidLogin.html')






