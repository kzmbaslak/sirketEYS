from django.urls import path
from .views import *

app_name = 'ciro'
urlpatterns = [
    path('',ciroIndex,name='index'),
    #path('detail/<slug:slug>/',ciroDetail,name='detail'),
    #path('create/',ciroCreate,name='create'),
    #path('update/<int:id>/',ciroUpdate,name='update'),
    #path('delete/<int:id>/',ciroDelete,name='delete'),
]