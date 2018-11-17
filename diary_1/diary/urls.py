"""diary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from django.conf.urls import url

import django.contrib.auth.views

urlpatterns = [
    #path(r'login/', include('login.urls')),
    path('admin/', admin.site.urls),
    path('diary_main/',include('diary_main.urls')),
]
    
'''
    #
    path('edit/',views.index),
    ##
    path('', views.index, name='index'),
    ###
    path('',app1_views.login,name='login'),
    path('join/',app1_views.join,name='join'),
    path('<int:u_id>/<int:d_id>/',app1_views.private_diary,name='private_diary'),
    path('<int:u_id>/',app1_views.private,name='private'),
    path('<int:u_id>/setting/',app1_views.private_setting,name='private_setting'),
    path('<int:u_id>/public/<int:d_id>/',app1_views.public,name='public'),
    '''