from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('login', views.login, name='login'),
    path('signIn', views.signIn, name='signIn'),
 #   path('mainpage',views.mainpage,name='mainpage'),
    path('<int:u_id>/<int:d_id>/',views.private_diary,name='private_diary'),
    path('private/<int:u_id>', views.private, name='private'),
    path('private/<int:u_id>/setting/', views.private_setting,name='private_setting'),
    
    path('diary/<int:d_id>', views.public, name='public'),
]