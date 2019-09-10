from django.contrib import admin
from .models import Duyuru
# Register your models here.
class DuyuruAdmin(admin.ModelAdmin):
    list_display = ['baslik','slug']
    class Meta:
        model = Duyuru

admin.site.register(Duyuru,DuyuruAdmin)