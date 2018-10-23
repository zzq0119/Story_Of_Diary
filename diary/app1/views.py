from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Diary,User

# Create your views here.
def login(request):
    if request.method=='POST':
        login_user=request.POST.get('user')
        login_password=request.POST.get('password')
        try:
            user=User.objects.get(username=login_user)
            if user.password==login_password:
                u_id=user.id
                return HttpResponseRedirect(reverse('private',args=(u_id,)))
            else:
                return render(request,'login.html',{'error_mess':'the password is wrong!'})
        except(User.DoesNotExist):
            return HttpResponseRedirect(reverse('join'))
    else:
        return render(request,'login.html')
def join(request):
    if request.method=='POST':
        join_user=request.POST.get('user')
        if len(User.objects.filter(username=join_user))!=0:
            return render(request,'join.html',{'error_mess':'the username is used!'})
        join_password=request.POST.get('password0')
        join_password1=request.POST.get('password1')
        if join_password==join_password1:
            user=User(username=join_user,password=join_password)
            user.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            return render(request,'join.html',{'error_mess':'two passwords are not equal!'})
    else:
        return render(request,'join.html')
def private(request,u_id):
    user=get_object_or_404(User,id=u_id)
    diary_list=user.diary_set.all()
    if request.method=='POST':
        if request.POST.get('password0')==user.password and request.POST.get('password1')==request.POST.get('password2'):
            user.password=request.POST.get('password1')
            user.save()
            return render(request,'private.html',{'url':reverse('public',args=(u_id,1)),'mess':"修改成功",'u_id':u_id,'username':user.username,'list':diary_list})
        else:
            return render(request,'private.html',{'url':reverse('public',args=(u_id,1)),'mess':"密码错误",'u_id':u_id,'username':user.username,'list':diary_list})
    return render(request,'private.html',{'url':reverse('public',args=(u_id,1)),'u_id':u_id,'username':user.username,'list':diary_list})
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
def public(request,u_id,d_id):
    diary_list=Diary.objects.filter(public=True)
    if len(diary_list)!=0:
        diary=diary_list[d_id-1]
        return render(request,'public.html',{'author':diary.user.username,'u_id':u_id,'list':diary_list,'content':diary.diary_text})
    else:
        return render(request,'public.html',{'author':"无",'u_id':u_id,'list':diary_list,'content':"无"})
