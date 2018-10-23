from django.test import TestCase
from .models import User,Diary
from django.urls import resolve,reverse
from .views import *
from django.http import HttpRequest,QueryDict
#注册
class joinTest(TestCase):
    def test_join_view_status_code(self):
        url = reverse('join')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
    def test_join_url_resolves_to_join_view(self):
        found=resolve('/join/')
        self.assertEquals(found.func,join)
    def test_join(self):#注册
        request=HttpRequest()
        request.method='POST'
        request.POST['user']='001'
        request.POST['password0']='123456'
        request.POST['password1']='123456'
        response=join(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response['location'],'/')
    def test_join_username_used(self):#用户名已存在
        User.objects.create(username='001',password='123456')
        request=HttpRequest()
        request.method='POST'
        request.POST['user']='001'
        request.POST['password0']='123456'
        request.POST['password1']='123456'
        response=join(request)
        self.assertIn('the username is used!',response.content.decode())
    def test_join_passwords_different(self):#两次密码不同
        request=HttpRequest()
        request.method='POST'
        request.POST['user']='001'
        request.POST['password0']='123456'
        request.POST['password1']='12345'
        response=join(request)
        self.assertIn('two passwords are not equal!',response.content.decode())
#登录        
class loginTest(TestCase):
    def test_login_view_status_code(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
    def test_root_url_resolves_to_login_view(self):
        found=resolve('/')
        self.assertEquals(found.func,login)
    def test_login(self):#登录
        User.objects.create(username='001',password='123456')
        request=HttpRequest()
        request.method='POST'
        request.POST['user']='001'
        request.POST['password']='123456'
        response=login(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response['location'],'/1/')
    def test_login_user_not_exist(self):#用户名不存在
        request=HttpRequest()
        request.method='POST'
        request.POST['user']='001'
        request.POST['password']='123456'
        response=login(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response['location'],'/join/')
    def test_login_wrong_password(self):#密码错误
        User.objects.create(username='001',password='123456')
        request=HttpRequest()
        request.method='POST'
        request.POST['user']='001'
        request.POST['password']='12345'
        response=login(request)
        self.assertIn('the password is wrong!',response.content.decode())
#私人部分        
class privateTest(TestCase):
    def add_user(self):
        User.objects.create(username='001',password='123456')
    def test_private_view_status_code(self):
        self.add_user()
        url = reverse('private',args=(1,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
    def test_private_url_resolves_to_private_view(self):
        found=resolve('/1/')
        self.assertEquals(found.func,private)
    def test_private_update(self):#改密码
        self.add_user()
        request=HttpRequest()
        request.method='POST'
        request.POST['password0']='123456'
        request.POST['password1']='654321'
        request.POST['password2']='654321'
        response=private(request,1)
        self.assertEquals(response.status_code, 200)
        self.assertIn('修改成功',response.content.decode())
        self.assertEquals(User.objects.get(username='001').password,'654321')
    def test_private_wrong_password(self):#改密码错误
        self.add_user()
        request=HttpRequest()
        request.method='POST'
        request.POST['password0']='12345'
        request.POST['password1']='654321'
        request.POST['password2']='654321'
        response=private(request,1)
        self.assertEquals(response.status_code, 200)
        self.assertIn('密码错误',response.content.decode())
    def test_private_wrong_password(self):#两次密码不同
        self.add_user()
        request=HttpRequest()
        request.method='POST'
        request.POST['password0']='123456'
        request.POST['password1']='654321'
        request.POST['password2']='65432'
        response=private(request,1)
        self.assertEquals(response.status_code, 200)
        self.assertIn('密码错误',response.content.decode())
