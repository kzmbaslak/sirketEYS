from django.contrib import admin
from .models import *
# Register your models here.
class ProjeGiderAdmin(admin.ModelAdmin):
    
    class Meta:
        model = ProjeGider
admin.site.register(ProjeGider)