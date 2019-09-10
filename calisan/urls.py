from django.urls import path
from .views import *

app_name = 'calisan'

urlpatterns = [
    path('',calisanIndex,name='index'),
    path('detail/<slug:slug>/',calisanDetail,name='detail'),
    path('create/',calisanCreate,name='create'),
    path('update/<int:id>/',calisanUpdate,name='update'),
    path('delete/<int:id>/',calisanDelete,name='delete'),
    path('passive/<int:id>/',calisanPassive,name='passive'),
    path('active/<int:id>/',calisanActive,name='active'),
    path('maas/',maasCreate,name='maascreate'),
    path('sgkprim/',sgkprimCreate,name='sgkprimcreate'),
    path('izin/',izinCreate,name='izincreate'),
    path('izin/update/<int:id>/',izinUpdate,name="izinUpdate"),
    path('kart/',kartCreate,name='kartcreate'),
    path('kart/delete/<int:id>/',kartDelete,name='kartDelete'),
]
