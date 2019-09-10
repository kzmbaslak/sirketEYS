from django.contrib import admin
from .models import *
# Register your models here.

class ProjeAdmin(admin.ModelAdmin):
    
    class Meta:
        model = Proje

admin.site.register(Proje)
admin.site.register(Ekip)
admin.site.register(EkipUye)
admin.site.register(Talep)