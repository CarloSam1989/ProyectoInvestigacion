import json
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

class PlanesForm(forms.ModelForm):
    plan_nombre = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    metodo = forms.ModelChoiceField(
        queryset=Metodos.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tecnica_cierre = forms.ModelMultipleChoiceField(
        queryset=TecnicaCierre.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    )
    forma_ense = forms.ModelMultipleChoiceField(
        queryset=FormasEnse.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    )
    recurso_didactico = forms.ModelMultipleChoiceField(
        queryset=RecursosDidacticos.objects.all(),  # Asegúrate de que no está vacío
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
  
    numero_actividad = forms.ModelMultipleChoiceField(
        queryset=Anexo1.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    )
   
    actividad_docente = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    asistencia = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    trabajo_fecha = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    motivacion = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )
    objetivo = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )
    saludo = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    conclusion = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    an_tecnica_cierre = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )
    chequeo_trabajo = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )
    evaluacion_aprendizaje = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'rows': 2})
    )
    trabajo_independiente = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'rows': 2})
    )
    bibliografia = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    desarrollo_clase = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8})
    )
    fecha_ejecucion= forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'}))
    
  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar las opciones para número de actividad
        self.fields['numero_actividad'].queryset = Anexo1.objects.all()
        self.fields['numero_actividad'].widget.choices = [
            (obj.pk, f"{obj.numero_actividad} + {obj.semestre}") for obj in self.fields['numero_actividad'].queryset
        ]

    class Meta:
        model = Planes
        fields = [
            'plan_nombre','metodo', 'fecha_ejecucion','tecnica_cierre', 'forma_ense', 'recurso_didactico', 
            'numero_actividad', 'actividad_docente', 'asistencia', 'trabajo_independiente',
            'trabajo_fecha','bibliografia', 'motivacion', 'objetivo','saludo','chequeo_trabajo',
            'desarrollo_clase', 'evaluacion_aprendizaje','conclusion', 'an_tecnica_cierre'
        ]

    def clean(self):
        cleaned_data = super().clean()
        desarrollo_clase_json = cleaned_data.get('desarrollo_clase_json')
        
        if desarrollo_clase_json:
            try:
                cleaned_data['desarrollo_clase'] = json.loads(desarrollo_clase_json)
            except json.JSONDecodeError:
                raise forms.ValidationError("Error procesando los datos de desarrollo de clase.")
        return cleaned_data
