from django import forms
from .models import AlimFatura

class AlimForm(forms.ModelForm):
    
    class Meta:
        model = AlimFatura
        fields = [
            'urunAdi',
            'urunAdedi',
            'birimFiyati',
        ]