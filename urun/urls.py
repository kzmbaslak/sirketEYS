from django.urls import path
from .views import *

app_name = 'urun'
urlpatterns = [
    path('',urunIndex,name='index'),
    #path('detail/<slug:slug>/',urunDetail,name='detail'),
    path('create/',urunCreate,name='create'),
    path('update/<slug:slug>/',urunUpdate,name='update'),
    path('delete/<int:id>/',urunDelete,name='delete'),
]