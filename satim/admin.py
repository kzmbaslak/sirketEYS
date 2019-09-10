from django.contrib import admin
from .models import SatimFatura
# Register your models here.

class SatimFaturaAdmin(admin.ModelAdmin):
    
    class Meta:
        model = SatimFatura

admin.site.register(SatimFatura)