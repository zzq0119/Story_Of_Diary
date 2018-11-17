from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from login.form import LoginForm
from django.template import loader
from .models import User
from django.template import RequestContext
import datetime

# Create your views here.
class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=50)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
    
def mainpage(request):
    if 'username' in request.COOKIES and 'last_connection' in request.COOKIES:
        username = request.COOKIES['username']
      
        last_connection = request.COOKIES['last_connection']
        last_connection_time = datetime.datetime.strptime(last_connection[:-7], "%Y-%m-%d %H:%M:%S")
      
        if (datetime.datetime.now() - last_connection_time).seconds < 10:
            return render(request, 'mainpage.html', {})
        else:
            return HttpResponseRedirect('index',request)
			
    else:
        return HttpResponseRedirect('index',request)

    
def index(request,error_message=''):
    return render(request,'index.html',{'error_message':error_message})

def signIn(request):
    if request.method=='POST':
        username=request.POST.get('username')
        if len(User.objects.filter(user_nickname=username))!=0:
            return render(request,'signIn.html',{'error_message':'the username is used!'})
        password=request.POST.get('password')
        password1=request.POST.get('check_password')
        if password==password1:
            user=User(user_nickname=username,user_password=password)
            user.save()
            return HttpResponseRedirect('index',request)
        else:
            return render(request,'signIn.html',{'error_message':'Inconsistent password'})
    else:
        return render(request,'signIn.html')
'''
def loginpage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=User.objects.get(user_nickname=username)
            if user.user_password==password:
                return HttpResponseRedirect('mainpage',request)
            else:
                return render(request,'index.html',{'error_message':'Password Invalid.'})
        except(User.DoesNotExist):
            return render(request,'index.html',{'error_message':'User does not exist.'})
'''
def loginpage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=User.objects.get(user_nickname=username)
            if user.user_password==password:
                response = HttpResponseRedirect('mainpage',request)
                response.set_cookie('last_connection', datetime.datetime.now())
                response.set_cookie('username', datetime.datetime.now())
                return response
            else:
                return render(request,'index.html',{'error_message':'Invalid Password.'})
        except(User.DoesNotExist):
            return render(request,'index.html',{'error_message':'User does not exist.'})
            
#空表单会报错；
#