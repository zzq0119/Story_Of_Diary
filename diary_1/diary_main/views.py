from django.shortcuts import get_object_or_404,render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Diary,User
from datetime import date
from django.template import loader,RequestContext
import datetime

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
                return HttpResponseRedirect(reverse('private'))
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
            return HttpResponseRedirect('signUp',request)
        else:
            return render(request,'index.html',{'error_message':'Inconsistent password.'})
    else:
        print(request.POST)
        return render(request,'index.html')
        
def signUp(request):
    return render(request,'signUpSuccess.html')
    
def private(request):
    if 'u_id' in request.session and 'username' in request.session:
        user_name=request.session['username']
        u_id=request.session['u_id']
        
        return render(request,'private.html',{'urlset':reverse('private_setting'),'username':user_name})
    else:
        return render(request,'index.html',{'error_message':'Login First.'})
       
def private_mydiary(request,d_id):
    if 'u_id' in request.session and 'username' in request.session:
        u_id=request.session['u_id']
        user_=get_object_or_404(User,id=u_id)
        diary_list=user_.diary_set.all()
        if d_id != 0:
            diary=get_object_or_404(Diary,id=d_id)
        return render(request,'private_mydiary.html',{'mess':'','d_id':d_id,'content':''})
    else:
        return render(request,'index.html',{'error_message':'Login First.'})



    
def private_diary(request,d_id):
    if 'u_id' in request.session and 'username' in request.session:
        u_id=request.session['u_id']
        user_=get_object_or_404(User,id=u_id)
        diary_list=user_.diary_set.all()
        if d_id != 0:   #查看修改删除
            diary=get_object_or_404(Diary,id=d_id)
            mess='private'
            if diary.public:
                mess='public'
            if request.method=='POST':
                if 'delete' in request.POST:
                    diary.delete()
                    return HttpResponseRedirect(reverse('private'))
                mess='private'
                if request.POST.get('check_box')=="1":
                    diary.public=True
                    mess='public'
                diary.diary_text=request.POST.get('file')
                diary.simp_text=diary.diary_text[:17]+'...'
                diary.save()
                return render(request,'private_diary.html',{'mess':mess,'d_id':d_id,'content':diary.diary_text})
            return render(request,'private_diary.html',{'mess':mess,'d_id':d_id,'content':diary.diary_text})
        else:   #新建
            if request.method=='POST' :
                diary=Diary(user=user_,diary_text=request.POST.get('file'),simp_text=request.POST.get('file')[:17]+'...',public=False)
                mess='private'
                if request.POST.get('check_box')=="1":
                    diary.public=True
                    mess='public'
                diary.pub_date=datetime.datetime.today()
                diary.save()
                return HttpResponseRedirect(reverse('private'))
            return render(request,'private_diary.html',{'mess':'','d_id':d_id,'content':''})
    else:
        return render(request,'index.html',{'error_message':'Login First.'})        
def private_setting(request):
    if 'u_id' in request.session and 'username' in request.session:
        u_id=request.session['u_id']
        user=User.objects.get(id=u_id)
        content={'back':reverse('private'),'img':user,'name':user.realname,'sex':'女','date':user.birthday,'phone':user.telephone}
        if user.sex:
            content={'back':reverse('private'),'img':user,'name':user.realname,'sex':'男','date':user.birthday,'phone':user.telephone}
        if request.method=="POST":
            if request.FILES.get("img"):
                user.img=request.FILES.get("img")
            user.realname=request.POST.get("realname")
            content = {'back':reverse('private'),'img':user,'name':user.realname,'sex':request.POST.get("sex"),'date':user.birthday,'phone':user.telephone}
            if request.POST.get("year") and request.POST.get("month") and request.POST.get("day"):
                user.birthday=date(int(request.POST.get("year")),int(request.POST.get("month")),int(request.POST.get("day")))
            user.telephone=request.POST.get("telephone")
            user.save()
        return render(request, 'private_setting.html', content)
    else:
        return render(request,'index.html',{'error_message':'Login First.'})
def public(request,d_id):
    if 'u_id' in request.session and 'username' in request.session:
        diary_list=Diary.objects.filter(public=True)
        if len(diary_list)!=0:
            diary=diary_list[d_id-1]
            return render(request,'public.html',{'author':diary.user.username,'u_id':u_id,'list':diary_list,'content':diary.diary_text})
        else:
            return render(request,'public.html',{'author':"无",'u_id':u_id,'list':diary_list,'content':"无"})
    else:
        return render(request,'index.html',{'error_message':'Login First.'})
        
def signOut(request):
    request.session.flush()
    return render(request,'index.html')
        

