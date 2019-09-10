from django.contrib import admin
from .models import AlimFatura
# Register your models here.
class AlimFaturaAdmin(admin.ModelAdmin):
    class Meta:
        model = AlimFatura

admin.site.register(AlimFatura)