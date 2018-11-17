from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('loginpage', views.loginpage, name='loginpage'),
    path('mainpage',views.mainpage,name='mainpage'),
    path('signin', views.signin, name='signin'),
]