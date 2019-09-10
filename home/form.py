from django import forms
from .models import Duyuru

class DuyuruForm(forms.ModelForm):

    class Meta:
        model = Duyuru
        fields = [
            'baslik',
            'text',
        ]