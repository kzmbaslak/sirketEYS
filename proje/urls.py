from django.urls import path
from .views import *

app_name = 'proje'

urlpatterns = [
    path('',projeIndex,name='index'),
    path('detail/<slug:slug>/',projeDetail,name='detail'),
    path('create/',projeCreate,name='create'),
    path('update/<int:id>/',projeUpdate,name='update'),
    path('delete/<int:id>/',projeDelete,name='delete'),
    path('ekip/create/<int:id>/',ekipCreate,name='ekipCreate'),
    path('ekip/update/<int:id>/',ekipUpdate,name='ekipUpdate'),
    path('ekip/delete/<int:id>/',ekipDelete,name='ekipDelete'),
    path('ekipuye/create/<int:id>/',ekipUyeCreate,name='ekipUyeCreate'),
    path('ekipuye/update/<int:id>/',ekipUyeUpdate,name='ekipUyeUpdate'),
    path('ekipuye/delete/<int:id>/',ekipUyeDelete,name='ekipUyeDelete'),
    path('talep/<int:id>/',talepDetail,name='talepDetail'),
    path('talep/create/<slug:slug>/',talepCreate,name='talepCreate'),
]