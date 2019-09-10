from django.urls import path
from .views import *

app_name = 'alim'
urlpatterns = [
    path('',alimIndex,name='index'),
    #path('detail/<slug:slug>/',alimDetail,name='detail'),
    path('detail/<slug:slug>/',alimDetail,name='detail'),
    path('create/',alimCreate,name='create'),
    #path('update/<slug:slug>/',alimUpdate,name='update'),
    path('update/<int:id>/',alimUpdate,name='update'),
    #path('delete/<slug:slug>/',alimDelete,name='delete'),
    path('delete/<int:id>/',alimDelete,name='delete'),
]