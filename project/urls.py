
from django.conf.urls import include
from django.urls.conf import path
from . import views



urlpatterns = [
    path('', views.proj_page, name='proj-page'),
]
