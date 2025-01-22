from django import forms
from .models import Anexo1

class Anexo1Form(forms.ModelForm):
    archivo = forms.FileField(required=True)

    class Meta:
        model = Anexo1
        fields = [ 'archivo']
