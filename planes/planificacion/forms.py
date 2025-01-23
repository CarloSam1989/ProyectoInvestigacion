from django import forms
from .models import *

class Anexo1Form(forms.ModelForm):
    archivo = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'})  # Aplicar estilo de Bootstrap
    )

    class Meta:
        model = Anexo1
        fields = ['archivo']

class MetodosForm(forms.ModelForm):
    class Meta:
        model = Metodos
        fields = ['nombre', 'descripcion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class TecnicaCierreForm(forms.ModelForm):
    class Meta:
        model = TecnicaCierre
        fields = ['nombre', 'descripcion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
class RecursosDidacticosForm(forms.ModelForm):
    class Meta:
        model = RecursosDidacticos
        fields = ['nombre', 'descripcion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        
class FormasEnseForm(forms.ModelForm):
    class Meta:
        model = FormasEnse
        fields = ['nombre', 'descripcion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class SaludoForm(forms.ModelForm):
    class Meta:
        model = Saludo
        fields = ['materia', 'saludo', 'docente']

    materia = forms.ChoiceField(
        choices=[(materia, materia) for materia in Anexo1.objects.values_list('materia', flat=True).distinct()],
        widget=forms.Select(attrs={'class': 'form-control'})  # Bootstrap styling
    )

    saludo = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el saludo'})
    )

   
