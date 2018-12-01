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
from django.conf import settings
from django.conf.urls import url
from django.views.static import serve
import django.contrib.auth.views

from django.conf.urls.static import static

urlpatterns = [
    path('',include('diary_main.urls')),
    path('admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root":settings.MEDIA_ROOT})
]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    
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