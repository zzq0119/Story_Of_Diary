from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signUp', views.signUp, name='signUp'),
    path('private/signOut', views.signOut, name='signOut'),
    path('public/page/<int:page>/', views.public, name='public'),
    path('private/setting/', views.private_setting,name='private_setting'),
    path('private/page/<int:page>/', views.private, name='private'),
    path('public/detail/<int:d_id>/', views.public_detail, name='public_detail'),
    path('private/detail/<int:d_id>/',views.private_detail,name='private_detail'),
    path('private/edit/<int:d_id>/',views.private_edit,name='private_edit'),
    path('private/edit/new/',views.private_edit_new,name='private_edit_new'),
]
