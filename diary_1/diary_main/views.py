from django.shortcuts import get_object_or_404,render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Diary,User
from datetime import date
from django.template import loader,RequestContext
import datetime

##################################

'''
def read(i):
    f=open('./%s.txt'% i,'r')
    x=f.read()
    return x
  
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'read/index.html', context)

def detail(request, question_id):
    #return HttpResponse(read(question_id))
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'read/detail.html', {'question': question})
    #latest_question_list = Question.contain
    #context = {'latest_question_list': latest_question_list}
    #return render(request, 'read/index.html', context)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
'''

##################################


def login(request):
    if request.method=='POST':
        login_user=request.POST.get('username')
        login_password=request.POST.get('password')
        try:
            user=User.objects.get(username=login_user)
            if user.password==login_password:
                u_id=User.id
                response = HttpResponseRedirect(reverse('private',args=(u_id,)))
                response.set_cookie('last_connection', datetime.datetime.now())
                response.set_cookie('username', datetime.datetime.now())
                return response
                
            else:
                return render(request,'login.html',{'error_mess':'Invalid Password.'})
        except(User.DoesNotExist):
            return render(request,'login.html',{'error_message':'User does not exist.'})
    else:
        return render(request,'login.html')
        
def signIn(request):        #注册
    if request.method=='POST':
        user_name=request.POST.get('username')
        if User.objects.filter(username=user_name):
            return render(request,'signIn.html',{'error_message':'Username has been used.'})
        _password=request.POST.get('password')
        check_password=request.POST.get('check_password')
        if _password==check_password:
            user=User(username=user_name,password=_password)
            user.save()
            return HttpResponseRedirect('login',request)
        else:
            return render(request,'signIn.html',{'error_message':'Inconsistent password.'})
    else:
        return render(request,'signIn.html')

def private(request,u_id):
    #if 'username' in request.COOKIES and 'last_connection' in request.COOKIES:
    user_name=get_object_or_404(User,id=u_id)
    
    diary_list=user.diary_set.all()
    if request.method=='POST':
        if request.POST.get('password0')==user.password and request.POST.get('password1')==request.POST.get('password2'):
            user.password=request.POST.get('password1')
            user.save()
            return render(request,'private.html',{'url':reverse('public',args=(u_id,1)),'urlset':reverse('private_setting',args=(u_id,)),'mess':"修改成功",'u_id':u_id,'username':user.username,'list':diary_list})
        else:
            return render(request,'private.html',{'url':reverse('public',args=(u_id,1)),'urlset':reverse('private_setting',args=(u_id,)),'mess':"密码错误",'u_id':u_id,'username':user.username,'list':diary_list})
    return render(request,'private.html',{'url':reverse('public',args=(u_id,1)),'urlset':reverse('private_setting',args=(u_id,)),'u_id':u_id,'username':user.username,'list':diary_list})

def private_diary(request,u_id,d_id):
    user_=get_object_or_404(User,id=u_id)
    diary_list=user_.diary_set.all()
    if d_id!=0:#查看修改删除
        diary=get_object_or_404(Diary,id=d_id)
        mess='private'
        if diary.public:
            mess='public'
        if request.method=='POST':
            if 'delete' in request.POST:
                diary.delete()
                return HttpResponseRedirect(reverse('private',args=(u_id,)))
            mess='private'
            if request.POST.get('check_box')=="1":
                diary.public=True
                mess='public'
            diary.diary_text=request.POST.get('file')
            diary.simp_text=diary.diary_text[:17]+'...'
            diary.save()
            return render(request,'private_diary.html',{'mess':mess,'u_id':u_id,'d_id':d_id,'content':diary.diary_text})
        return render(request,'private_diary.html',{'mess':mess,'u_id':u_id,'d_id':d_id,'content':diary.diary_text})
    else:#新建
        if request.method=='POST' :
            diary=Diary(user=user_,diary_text=request.POST.get('file'),simp_text=request.POST.get('file')[:17]+'...',public=False)
            mess='private'
            if request.POST.get('check_box')=="1":
                diary.public=True
                mess='public'
            diary.save()
            return HttpResponseRedirect(reverse('private',args=(u_id,)))
        return render(request,'private_diary.html',{'mess':'','u_id':u_id,'d_id':d_id,'content':''})
def private_setting(request,u_id):
    user=User.objects.get(id=u_id)
    content={'back':reverse('private',args=(u_id,)),'img':user,'name':user.realname,'sex':'女','date':user.birthday,'phone':user.telephone}
    if user.sex:
        content={'back':reverse('private',args=(u_id,)),'img':user,'name':user.realname,'sex':'男','date':user.birthday,'phone':user.telephone}
    if request.method=="POST":
        if request.FILES.get("img"):
            user.img=request.FILES.get("img")
        user.realname=request.POST.get("realname")
        if request.POST.get("sex")=="1":
            user.sex=True
            content = {'back':reverse('private',args=(u_id,)),'img':user,'name':user.realname,'sex':'男','date':user.birthday,'phone':user.telephone}
        if request.POST.get("sex")=="0":
            user.sex=False
            content = {'back':reverse('private',args=(u_id,)),'img':user,'name':user.realname,'sex':'女','date':user.birthday,'phone':user.telephone}
        if request.POST.get("year") and request.POST.get("month") and request.POST.get("day"):
            user.birthday=date(int(request.POST.get("year")),int(request.POST.get("month")),int(request.POST.get("day")))
        user.telephone=request.POST.get("telephone")
        user.save()
    return render(request, 'private_setting.html', content)
def public(request,u_id,d_id):
    diary_list=Diary.objects.filter(public=True)
    if len(diary_list)!=0:
        diary=diary_list[d_id-1]
        return render(request,'public.html',{'author':diary.user.username,'u_id':u_id,'list':diary_list,'content':diary.diary_text})
    else:
        return render(request,'public.html',{'author':"无",'u_id':u_id,'list':diary_list,'content':"无"})
##################################
'''
from django.shortcuts import render
from edit import models


def index(request):
    if request.method == "POST":
        comment = request.POST.get("comment",None)
        detail = request.POST.get("detail",None)
        models.content.objects.create(comment=comment,detail=detail)

    edit_list = models.content.objects.all()

    return render(request,"edit.html",{"data":edit_list})
##################################
'''








