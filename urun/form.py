from django import forms
from .models import Urun

class UrunForm(forms.ModelForm):
    stok = forms.IntegerField()
    class Meta:
        model = Urun
        fields = [
        ]
class UrunYeniForm(forms.ModelForm):
    class Meta:
        model = Urun
        fields = [
            'adi',
            'birimFiyati',
            'stokMiktari',
        ]