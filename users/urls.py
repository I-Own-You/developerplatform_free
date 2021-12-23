from django.shortcuts import render
from django.urls.conf import path

from . import views

urlpatterns = [
    path('', views.dev_page, name='dev-page'),

    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('my-account/', views.my_account, name='my-account'),
    path('my-account/proj-creation', views.proj_create, name='proj-create'),
    path('inbox/', views.inbox, name='inbox'),
    path('inbox/messages/<int:id>/', views.message, name='message'),
    path('inbox/create-message/<int:id>/',
         views.create_message, name='create-message'),
]
