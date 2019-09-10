from django.contrib import admin
from .models import Urun
# Register your models here.

class UrunAdmin(admin.ModelAdmin):
    
    class Meta:
        model = Urun


admin.site.register(Urun)