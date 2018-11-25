from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
#    path('login', views.login, name='login'),
#    path('signIn', views.signIn, name='signIn'),
    path('private/<int:d_id>/',views.private_diary,name='private_diary'),
    path('private', views.private, name='private'),
    path('private/setting/', views.private_setting,name='private_setting'),
    path('public/<int:d_id>', views.public, name='public'),
]