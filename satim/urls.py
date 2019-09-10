from django.urls import path
from .views import *

app_name = 'satim'
urlpatterns = [
    path('',satimIndex,name='index'),
    path('detail/<slug:slug>/',satimDetail,name='detail'),
    path('create/',satimCreate,name='create'),
    path('update/<int:id>/',satimUpdate,name='update'),
    path('delete/<int:id>/',satimDelete,name='delete'),
]