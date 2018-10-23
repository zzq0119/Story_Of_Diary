"""diary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
import app1.views as app1_views

urlpatterns = [
    path('',app1_views.login,name='login'),
    path('join/',app1_views.join,name='join'),
    path('<int:u_id>/<int:d_id>/',app1_views.private_diary,name='private_diary'),
    path('<int:u_id>/',app1_views.private,name='private'),
    path('<int:u_id>/public/<int:d_id>/',app1_views.public,name='public'),
]
