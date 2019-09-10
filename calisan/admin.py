from django.contrib import admin
from .models import *
# Register your models here.

class CalisanAdmin(admin.ModelAdmin):
    list_display = ['user','slug']
    class Meta:
        model = Calisan
class YetkiAdmin(admin.ModelAdmin):
    list_display = ['id','adi']
    class Meta:
        model = Yetki
admin.site.register(Calisan,CalisanAdmin)
admin.site.register(Yetki,YetkiAdmin)
admin.site.register(Kart)
admin.site.register(SgkPrim)
admin.site.register(Izin)
admin.site.register(MaasOdeme)
admin.site.register(Kategori)