from django import forms
from .models import *
from django.contrib.auth.models import User

class CalisanForm(forms.ModelForm):
    class Meta:
        model = Calisan
        fields = [
            'tel',
            'yetki',
            'sgkNo',
            'maas',
            'image'
        ]

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'groups',
            'user_permissions',
            'is_staff',
        ]

class MaasForm(forms.ModelForm):
    tumMaas = forms.BooleanField(required=False,label="Tüm maaşları öde")
    class Meta:
        model = MaasOdeme
        fields = [
            'calisan',
        ]

class SgkPrimForm(forms.ModelForm):
    tumPrim = forms.BooleanField(required=False,label="Tüm sgk primleri öde")
    class Meta:
        model = SgkPrim
        fields = [
            'calisan',
        ]
    
class IzinForm(forms.ModelForm):
    tumIzin = forms.BooleanField(required=False,label="Tümüne izin ver")
    class Meta:
        model = Izin
        fields = [
            'calisan',
            'kategori',
            'izinTarihi',
            'gun',
        ]
class IzinYeniForm(forms.ModelForm):
    class Meta:
        model = Izin
        fields = [
            'kategori',
            'izinTarihi',
            'gun',
        ]
class KartForm(forms.ModelForm):
    class Meta:
        model = Kart
        fields = [
            'calisan',
            'kodu',
        ]