from django import forms
from .models import SatimFatura

class SatimForm(forms.ModelForm):
    class Meta:
        model = SatimFatura
        fields = [
            'urun',
            'adedi',
            'aliciAdi',
        ]