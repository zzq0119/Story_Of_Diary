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
                u_id=user.id

                request.session['username'] = login_user
                request.session['u_id'] = u_id
                request.session.set_expiry(300)
                return HttpResponseRedirect(reverse('public',args=(1,)))
                
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
        
def public(request,page):
    if 'u_id' in request.session and 'username' in request.session:
        user_name=request.session['username']
        u_id=request.session['u_id']
        diary_list=Diary.objects.filter(public=True)
        user=User.objects.get(id=u_id)
        length=len(diary_list)#日记总条数
        max_page=(length-1)/6+1
        diary_list=diary_list[page*6-6:page*6]
        dist={}
        if page>1 and page<max_page:
            dist['last']=reverse('public',args=(page-1,))
            dist['next']=reverse('public',args=(page+1,))
        if page==max_page and max_page>1:
            dist['last']=reverse('public',args=(page-1,))
        if page==1 and max_page>1:
            dist['next']=reverse('public',args=(page+1,))
        for i in range(len(diary_list)):
            dist['diary'+str(i+1)]=diary_list[i]
            dist['url'+str(i+1)]=reverse('public_detail',args=(diary_list[i].id,))
        dist['user']=user_name
        dist['age']=datetime.datetime.today().year-User.objects.get(id=u_id).birthday.year
        dist['public']=reverse('public',args=(1,))
        dist['private']=reverse('private',args=(1,))
        dist['setting']=reverse('private_setting')
        dist['picture']=user
        return render(request,'public.html',dist)
    else:
        return render(request,'login.html',{'error_message':'Login First.'})
       # 'url':reverse('public',args=(u_id,1)),,'list':diary_list
def private(request,page):
    if 'u_id' in request.session and 'username' in request.session:
        user_name=request.session['username']
        u_id=request.session['u_id']
        user=get_object_or_404(User,id=u_id)
        diary_list=user.diary_set.all()
        length=len(diary_list)
        max_page=(length-1)/6+1
        diary_list=diary_list[page*6-6:page*6]
        dist={}
        if page>1 and page<max_page:
            dist['last']=reverse('private',args=(page-1,))
            dist['next']=reverse('private',args=(page+1,))
        if page==max_page and max_page>1:
            dist['last']=reverse('private',args=(page-1,))
        if page==1 and max_page>1:
            dist['next']=reverse('private',args=(page+1,))
        for i in range(len(diary_list)):
            dist['diary'+str(i+1)]=diary_list[i]
            dist['url'+str(i+1)]=reverse('private_detail',args=(diary_list[i].id,))
        dist['user']=user_name
        dist['age']=datetime.datetime.today().year-User.objects.get(id=u_id).birthday.year
        dist['public']=reverse('public',args=(1,))
        dist['private']=reverse('private',args=(1,))
        dist['setting']=reverse('private_setting')
        dist['picture']=user
        dist['new']=reverse('private_edit_new')
        return render(request,'private.html',dist)
    else:
        return render(request,'login.html',{'error_message':'Login First.'})       
def private_setting(request):
    if 'u_id' in request.session and 'username' in request.session:
        u_id=request.session['u_id']
        user=User.objects.get(id=u_id)
        content={'back':reverse('private',args=(1,)),'img':user,'name':user.realname,'sex':'女','date':user.birthday,'phone':user.telephone}
        if user.sex:
            content={'back':reverse('private',args=(1,)),'img':user,'name':user.realname,'sex':'男','date':user.birthday,'phone':user.telephone}
        if request.method=="POST":
            if request.FILES.get("img"):
                user.img=request.FILES.get("img")
            user.realname=request.POST.get("realname")
            content = {'back':reverse('private',args=(1,)),'img':user,'name':user.realname,'sex':request.POST.get("sex"),'date':user.birthday,'phone':user.telephone}
            if request.POST.get("year") and request.POST.get("month") and request.POST.get("day"):
                user.birthday=date(int(request.POST.get("year")),int(request.POST.get("month")),int(request.POST.get("day")))
            user.telephone=request.POST.get("telephone")
            user.save()
        return render(request, 'private_setting.html', content)
    else:
        return render(request,'login.html',{'error_message':'Login First.'})
def public_detail(request,d_id):
    diary=Diary.objects.get(id=d_id)
    dist={'back':reverse('public',args=(1,)),'title':diary.title,'text':diary.diary_text,'author':diary.user.username}
    return render(request,'public_detail.html',dist)
def private_detail(request,d_id):
    diary=Diary.objects.get(id=d_id)
    dist={'back':reverse('private',args=(1,)),'title':diary.title,'text':diary.diary_text,'url':reverse('private_edit',args=(d_id,))}
    return render(request,'private_detail.html',dist)
def private_edit(request,d_id):
    diary=get_object_or_404(Diary,id=d_id)
    mess='私有'
    if diary.public:
        mess='公开'
    if request.method=='POST':
        if 'delete' in request.POST:
            diary.delete()
            return HttpResponseRedirect(reverse('private',args=(1,)))
        if request.POST.get('check_box')=="1":
            diary.public=True
        else:
            diary.public=False
        diary.title=request.POST.get('file1')
        diary.diary_text=request.POST.get('file')
        diary.simp_text=diary.diary_text[:100]+'...'
        diary.pub_date=datetime.datetime.today()
        diary.save()
        dist={'back':reverse('private',args=(1,)),'title':diary.title,'text':diary.diary_text,'url':reverse('private_edit',args=(d_id,))}
        return render(request,'private_detail.html',dist)
    return render(request,'private_edit.html',{'d_id':d_id,'diary_title':diary.title,'content':diary.diary_text,'mess':mess,'url':reverse('private_detail',args=(d_id,))})
def private_edit_new(request):
    if 'u_id' in request.session and 'username' in request.session:
        user_name=request.session['username']
        u_id=request.session['u_id']
        user=User.objects.get(id=u_id)
        if request.method=='POST' :
            diary=Diary(user=user,title=request.POST.get('file1'),diary_text=request.POST.get('file'),simp_text=request.POST.get('file')[:100]+'...',public=False)
            mess='private'
            diary.pub_date=datetime.datetime.today()
            if request.POST.get('check_box')=="1":
                diary.public=True
                mess='public'
            diary.save()
            dist={'back':reverse('private',args=(1,)),'title':diary.title,'text':diary.diary_text,'url':reverse('private_edit',args=(diary.id,))}
            return render(request,'private_detail.html',dist)
        return render(request,'private_edit_new.html',{'url':reverse('private',args=(1,))})
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








