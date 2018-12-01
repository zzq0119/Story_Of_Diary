from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponseRedirect,HttpResponseForbidden
from django.urls import reverse
from .models import Diary,User
from datetime import date
from django.template import loader,RequestContext
import datetime,re

def index(request):
    if request.method=='POST' and 'check_password' not in request.POST:
        login_user=request.POST.get('username')
        login_password=request.POST.get('password')
        try:
            user=User.objects.get(username=login_user)
            if user.password==login_password:
                u_id=user.id
                request.session['username'] = login_user
                request.session['u_id'] = u_id
                request.session.set_expiry(300)
                return HttpResponseRedirect(reverse('private',args=(1,)))
            else:
                return render(request,'index.html',{'error_mess':'Invalid Password.'})
        except(User.DoesNotExist):
            return render(request,'index.html',{'error_message':'User does not exist.'})
    elif request.method=='POST' and 'check_password' in request.POST:
        user_name=request.POST.get('username')
        if User.objects.filter(username=user_name):
            return render(request,'index.html',{'error_message':'Username has been used.'})
        _password=request.POST.get('password')
        check_password=request.POST.get('check_password')
        if _password==check_password:
            user=User(username=user_name,password=_password)
            user.save()
            return redirect('signUp')
        else:
            return render(request,'index.html',{'error_message':'Inconsistent password.'})
    else:
        return render(request,'index.html')
        
def signUp(request):
    return render(request,'signUpSuccess.html')
    
def signOut(request):
    if request.session:
        request.session.flush()
    return redirect('/')
def public(request,page):
    if 'u_id' in request.session and 'username' in request.session:
        user_name=request.session['username']
        u_id=request.session['u_id']
        diary_list=Diary.objects.filter(public=True)
        user=User.objects.get(id=u_id)
        length=len(diary_list)#日记总条数
        max_page=int((length-1)/6)+1
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
        dist['user']=user.realname
        dist['age']=datetime.datetime.today().year-User.objects.get(id=u_id).birthday.year
        dist['public']=reverse('public',args=(1,))
        dist['private']=reverse('private',args=(1,))
        dist['setting']=reverse('private_setting')
        dist['picture']=user
        return render(request,'public.html',dist)
    else:
        return render(request,'index.html',{'error_message':'Login First.'})

def private(request,page):
    if 'u_id' in request.session and 'username' in request.session:
        user_name=request.session['username']
        u_id=request.session['u_id']
        user=get_object_or_404(User,id=u_id)
        diary_list=[]
        diary_list=user.diary_set.all()
        if request.method=="POST":
            tmp=[]
            diary_list=user.diary_set.all()
            for i in diary_list:
                if str(i.pub_date.date())==request.POST.get("date"):
                    tmp+=[i]
            diary_list=tmp
        length=len(diary_list)
        max_page=int((length-1)/5)+1
        diary_list=diary_list[page*5-5:page*5]
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
        dist['age']=datetime.datetime.today().year-User.objects.get(id=u_id).birthday.year
        dist['user']=user.realname
        dist['public']=reverse('public',args=(1,))
        dist['private']=reverse('private',args=(1,))
        dist['setting']=reverse('private_setting')
        dist['picture']=user
        dist['new']=reverse('private_edit_new')
        return render(request,'private.html',dist)
    else:
        return render(request,'index.html',{'error_message':'Login First.'})       
def private_setting(request):
    if 'u_id' in request.session and 'username' in request.session:
        u_id=request.session['u_id']
        user=User.objects.get(id=u_id)
        content={'back':reverse('private',args=(1,)),'img':user.img,'name':user.realname,'sex':'女','date':user.birthday,'phone':user.telephone}
        if user.sex:
            content={'back':reverse('private',args=(1,)),'img':user.img,'name':user.realname,'sex':'男','date':user.birthday,'phone':user.telephone}
        if request.method=="POST":
            if request.FILES.get("img"):
                user.img=request.FILES.get("img")
            if request.POST.get("realname"):
                user.realname=request.POST.get("realname")
            content = {'back':reverse('private',args=(1,)),'img':user}
            if request.POST.get("sex"):
                if request.POST.get("sex")=="0":
                    user.sex="女"
                else:
                    user.sex="男"
            if request.POST.get("YYYY") and request.POST.get("MM") and request.POST.get("DD"):
                user.birthday=date(int(request.POST.get("YYYY")),int(request.POST.get("MM")),int(request.POST.get("DD")))
            if request.POST.get("telephone"):
                user.telephone=request.POST.get("telephone")
            if request.POST.get("mailbox"):
                user.email=request.POST.get("mailbox")
            if request.POST.get('q1')==user.password and request.POST.get('q2'):
                user.password=request.POST.get('q2')
            user.save()
        return render(request, 'private_setting.html', content)
    else:
        return render(request,'index.html',{'error_message':'Login First.'})
def public_detail(request,d_id):
    if 'u_id' in request.session and 'username' in request.session:
        u_id=request.session['u_id']
        user=User.objects.get(id=u_id)
        diary=Diary.objects.get(id=d_id)
        diary_list=Diary.objects.filter(public=True)
        dist={'back':reverse('public',args=(1,)),'picture':user,'list':diary_list,'pub_date':diary.pub_date,'realname':user.realname,'age':datetime.datetime.today().year-user.birthday.year,
              'user_name':user.username,'title':diary.title,'text':diary.diary_text,'author':diary.user.username,'email':user.email}
        if user.sex=="男":
            dist['sex']="男"
        if user.sex=="女":
            dist['sex']="女"
        return render(request,'public_detail.html',dist)
    else:
        return redirect('/')
def private_detail(request,d_id):
    if 'u_id' in request.session and 'username' in request.session:
        u_id=request.session['u_id']
        user=User.objects.get(id=u_id)
        diary=Diary.objects.get(id=d_id)
        diary_list=user.diary_set.all()
        dist={'back':reverse('private',args=(1,)),'piture':user,'list':diary_list,'pub_date':diary.pub_date,'realname':user.realname,'age':datetime.datetime.today().year-user.birthday.year,
              'user_name':user.username,'title':diary.title,'text':diary.diary_text,'url':reverse('private_edit',args=(d_id,)),'email':user.email}
        if user.sex=="男":
            dist['sex']="男"
        if user.sex=="女":
            dist['sex']="女"
        return render(request,'private_detail.html',dist)
    else:
        return redirect('/')
def private_edit(request,d_id):
    if 'u_id' in request.session and 'username' in request.session:
        u_id=request.session['u_id']
        user=User.objects.get(id=u_id)
        diary=Diary.objects.get(id=d_id)
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
        dist={'picture':user,'realname':user.realname,'age':datetime.datetime.today().year-user.birthday.year,'email':user.email,
                                               'd_id':d_id,'diary_title':diary.title,'content':diary.diary_text,'mess':mess,'url':reverse('private_detail',args=(d_id,))}
        if user.sex=="男":
            dist['sex']="男"
        if user.sex=="女":
            dist['sex']="女"
        return render(request,'private_edit.html',dist)
    else:
        return redirect('/')
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
        dist={'url':reverse('private',args=(1,)),'picture':user,'realname':user.realname,'age':datetime.datetime.today().year-user.birthday.year,'email':user.email}
        if user.sex=="男":
            dist['sex']="男"
        if user.sex=="女":
            dist['sex']="女"
        return render(request,'private_edit_new.html',dist)
    else:
        return redirect('/')
