from django.conf.urls import url
from django.urls import path
from .views import *

app_name = 'home'
urlpatterns = [
    path('',homeIndex,name = 'index'),
    path('duyuru/<slug:slug>/',duyuruDetail,name='detail'),
    path('create/',duyuruCreate,name='create'),
    path('update/<slug:slug>/',duyuruUpdate,name='update'),
    path('delete/<slug:slug>/',duyuruDelete,name='delete'),
]
