from django import forms
from .models import Ekip,EkipUye,Talep,Proje
from calisan.models import Calisan

class EkipForm(forms.ModelForm):
    calisanlar = forms.ModelMultipleChoiceField(queryset=Calisan.objects.all())
    class Meta:
        model = Ekip
        fields = [
            'adi',
        ]
class EkipUyeForm(forms.ModelForm):
    class Meta:
        model = EkipUye
        fields = [
            'calisan',
            'yetki',
        ]
class TalepForm(forms.ModelForm):
    class Meta:
        model = Talep
        fields = [
            'baslik',
            'text',
            'maliyet',
        ]
class ProjeForm(forms.ModelForm):
    class Meta:
        model = Proje
        fields = [
            'adi',
            'yoneticiCalisan',
        ]