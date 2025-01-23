
# Create your views here.
import pandas as pd
import os
from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from collections import defaultdict


USUARIOS = {
    "admin": "admin",
    "user1": "Carlos",
    "user2": "Jorge"
}

def CustomLoginView(request):
    if "user" in request.session:  # Si ya está autenticado
        return redirect("menu_principal")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Validar las credenciales
        if username in USUARIOS and USUARIOS[username] == password:
            # Guardar el estado de autenticación en la sesión
            request.session["user"] = username
            return redirect(request.GET.get("next", "menu_principal"))
        else:
            messages.error(request, "Usuario o contraseña incorrectos. Intenta de nuevo.")

    return render(request, "login.html")

def logout_view(request):
    request.session.flush()  # Eliminar todos los datos de la sesión
    return redirect("login")

def menu(request):
    if "user" not in request.session:
        return redirect(f"/?next=/menu/")  # Redirigir a la página de login con `next`
    
    # Renderizar el menú principal
    return render(request, "index.html", {"user": request.session["user"]})

#Mixin personalizado para verificar la autenticación en vistas basadas en clases.
class SessionAuthRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if "user" not in request.session:
            return redirect(f"/?next={request.path}")
        return super().dispatch(request, *args, **kwargs)
    
#METODOS

# Vista para listar métodos

class MetodosListView(SessionAuthRequiredMixin, ListView):
    model = Metodos
    template_name = 'metodos/metodos_list.html'
    context_object_name = 'metodos'

# Vista para ver detalles de un método
class MetodosDetailView(SessionAuthRequiredMixin, DetailView):
    model = Metodos
    template_name = 'metodos/metodos_detail.html'
    context_object_name = 'metodo'

# Vista para crear un nuevo método
class MetodosCreateView(SessionAuthRequiredMixin, CreateView):
    model = Metodos
    template_name = 'metodos/metodos_form.html'
    form_class = MetodosForm
    success_url = reverse_lazy('metodos_list')

# Vista para actualizar un método existente
class MetodosUpdateView(SessionAuthRequiredMixin, UpdateView):
    model = Metodos
    template_name = 'metodos/metodos_form.html'
    fields = ['nombre', 'descripcion']
    success_url = reverse_lazy('metodos_list')

# Vista para eliminar un método
class MetodosDeleteView(SessionAuthRequiredMixin, DeleteView):
    model = Metodos
    template_name = 'metodos/metodos_confirm_delete.html'
    success_url = reverse_lazy('metodos_list')

#TECNICA DE CIERRE

# Vista para listar métodos

class TecnicaCierreListView(SessionAuthRequiredMixin, ListView):
    
    model = TecnicaCierre
    template_name = 'tecnica_cierre/tecnica_cierre_list.html'
    context_object_name = 'tecnica_cierre'

# Vista para ver detalles de un método
class TecnicaCierreDetailView(SessionAuthRequiredMixin, DetailView):
    model = TecnicaCierre
    template_name = 'tecnica_cierre/tecnica_cierre_detail.html'
    context_object_name = 'tecnica_cierre'

# Vista para crear un nuevo método
class TecnicaCierreCreateView(SessionAuthRequiredMixin, CreateView):
    model = TecnicaCierre
    template_name = 'tecnica_cierre/tecnica_cierre_form.html'
    form_class = TecnicaCierreForm
    success_url = reverse_lazy('tecnica_cierre_list')

# Vista para actualizar un método existente
class TecnicaCierreUpdateView(SessionAuthRequiredMixin, UpdateView):
    model = TecnicaCierre
    template_name = 'tecnica_cierre/tecnica_cierre_form.html'
    fields = ['nombre', 'descripcion']
    success_url = reverse_lazy('tecnica_cierre_list')

# Vista para eliminar un método
class TecnicaCierreDeleteView(SessionAuthRequiredMixin, DeleteView):
    model = TecnicaCierre
    template_name = 'tecnica_cierre/tecnica_cierre_confirm_delete.html'
    success_url = reverse_lazy('tecnica_cierre_list')

#RECURSOS DIDACTICOS

# Vista para listar métodos

class RecursosDidacticosListView(SessionAuthRequiredMixin, ListView):
    
    model = RecursosDidacticos
    template_name = 'recursos_didacticos/recursos_didacticos_list.html'
    context_object_name = 'recursos_didacticos'

# Vista para ver detalles de un método
class RecursosDidacticosDetailView(SessionAuthRequiredMixin, DetailView):
    model = RecursosDidacticos
    template_name = 'recursos_didacticos/recursos_didacticos_detail.html'
    context_object_name = 'recursos_didacticos'

# Vista para crear un nuevo método
class RecursosDidacticosCreateView(SessionAuthRequiredMixin, CreateView):
    model = RecursosDidacticos
    template_name = 'recursos_didacticos/recursos_didacticos_form.html'
    form_class = RecursosDidacticosForm
    success_url = reverse_lazy('recursos_didacticos_list')

# Vista para actualizar un método existente
class RecursosDidacticosUpdateView(SessionAuthRequiredMixin, UpdateView):
    model = RecursosDidacticos
    template_name = 'recursos_didacticos/recursos_didacticos_form.html'
    fields = ['nombre', 'descripcion']
    success_url = reverse_lazy('recursos_didacticos_list')

# Vista para eliminar un método
class RecursosDidacticosDeleteView(SessionAuthRequiredMixin, DeleteView):
    model = RecursosDidacticos
    template_name = 'recursos_didacticos/recursos_didacticos_confirm_delete.html'
    success_url = reverse_lazy('recursos_didacticos_list')

#FORMA ENSEÑANZA

# Vista para listar métodos

class FormaEnseListView(SessionAuthRequiredMixin, ListView):
    
    model = FormasEnse
    template_name = 'forma_ense/forma_ense_list.html'
    context_object_name = 'forma_ense'

# Vista para ver detalles de un método
class FormaEnseDetailView(SessionAuthRequiredMixin, DetailView):
    model = FormasEnse
    template_name = 'forma_ense/forma_ense_detail.html'
    context_object_name = 'forma_ense'

# Vista para crear un nuevo método
class FormaEnseCreateView(SessionAuthRequiredMixin, CreateView):
    model = FormasEnse
    template_name = 'forma_ense/forma_ense_form.html'
    form_class = FormasEnseForm
    success_url = reverse_lazy('forma_ense_list')

# Vista para actualizar un método existente
class FormaEnseUpdateView(SessionAuthRequiredMixin, UpdateView):
    model = FormasEnse
    template_name = 'forma_ense/forma_ense_form.html'
    fields = ['nombre', 'descripcion']
    success_url = reverse_lazy('forma_ense_list')

# Vista para eliminar un método
class FormaEnseDeleteView(SessionAuthRequiredMixin, DeleteView):
    model = FormasEnse
    template_name = 'forma_ense/forma_ense_confirm_delete.html'
    success_url = reverse_lazy('forma_ense_list')

#Saludo

# Vista para listar métodos

class SaludoListView(SessionAuthRequiredMixin, ListView):
    model = Saludo
    template_name = 'saludo/saludo_list.html'
    context_object_name = 'saludo'

    def get_queryset(self):
        # Obtener el usuario de la sesión
        user = self.request.session.get('user')

        # Filtrar por el campo docente que coincida con el usuario de la sesión
        if user:
            return Saludo.objects.filter(docente=user)
        else:
            # Retornar un queryset vacío si no hay un usuario en la sesión
            return Saludo.objects.none()

# Vista para ver detalles de un método
class SaludoDetailView(SessionAuthRequiredMixin, DetailView):
    model = Saludo
    template_name = 'saludo/saludo_detail.html'
    context_object_name = 'saludo'

# Vista para crear un nuevo método
class SaludoCreateView(SessionAuthRequiredMixin, CreateView):
    model = Saludo
    template_name = 'saludo/saludo_form.html'
    fields = ['materia', 'saludo']  # Excluir 'docente' porque se establecerá automáticamente
    success_url = reverse_lazy('saludo_list')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        # Modificar el campo "materia" para ser un ComboBox con las materias de Anexo1
        form.fields['materia'] = forms.ChoiceField(
            choices=[(materia, materia) for materia in Anexo1.objects.values_list('materia', flat=True).distinct()],
            required=True,
            widget=forms.Select(attrs={'class': 'form-control'})  # Aplicar estilo de Bootstrap
        )
        form.fields['saludo'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese el saludo'})
        return form

    def form_valid(self, form):
        # Establecer el campo "docente" con el usuario de la sesión
        form.instance.docente = self.request.session.get('user')
        return super().form_valid(form)

# Vista para actualizar un método existente
class SaludoUpdateView(SessionAuthRequiredMixin, UpdateView):
    model = Saludo
    template_name = 'saludo/saludo_form.html'
    fields = ['saludo', 'asignatura']
    success_url = reverse_lazy('fsaludo_list')

# Vista para eliminar un método
class SaludoDeleteView(SessionAuthRequiredMixin, DeleteView):
    model = Saludo
    template_name = 'saludo/saludo_confirm_delete.html'
    success_url = reverse_lazy('saludo_list')


class Anexo1ListView(SessionAuthRequiredMixin, ListView):
    model = Anexo1
    template_name = 'anexo/list.html'
    context_object_name = 'anexos'

    def get_queryset(self):
        # Obtener el 'id' desde los parámetros de la URL
        materia = self.kwargs.get('materia')  # Usar kwargs para acceder al parámetro 'id'

        if materia:
            # Filtrar por materia si el id está presente
            return Anexo1.objects.filter(materia=materia).order_by('actividad')
        else:
            # Si no hay id, devolver todos los registros
            return Anexo1.objects.all().order_by('actividad')

    
def upload_excel(request):
    if request.method == 'POST':
        form = Anexo1Form(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']

            try:
                # Leer el archivo Excel
                df = pd.read_excel(archivo)

                # Validar columnas requeridas
                required_columns = [
                    'Docente', 'Materia', 'Carrera', 'Semestre',
                    'Actividad', 'Tema', 'Trabajo Independiente'
                ]
                for column in required_columns:
                    if column not in df.columns:
                        messages.error(request, f"Error: Falta la columna '{column}' en el archivo.")
                        return redirect('upload_excel')

                # Obtener el nombre de la materia de la primera fila
                if 'Materia' not in df.columns or df.empty:
                    messages.error(request, "Error: El archivo no contiene información de materia.")
                    return redirect('upload_excel')

                nombre_materia = df.iloc[0]['Materia'].replace(" ", "_")
                archivo_nombre = f"{nombre_materia}.xlsx"

                # Guardar el archivo con el nuevo nombre
                ruta_archivo = os.path.join('anexos', archivo_nombre)
                with open(os.path.join(settings.MEDIA_ROOT, ruta_archivo), 'wb+') as destino:
                    for chunk in archivo.chunks():
                        destino.write(chunk)

                # Procesar cada fila
                procesados = 0
                omitidos = 0
                for _, row in df.iterrows():
                    # Validar duplicados basados en el contenido de cada fila
                    existe = Anexo1.objects.filter(
                        materia=row['Materia'],
                        semestre=row['Semestre'],
                        actividad=row['Actividad'],
                        tema=row['Tema'],
                        archivo=ruta_archivo
                    ).exists()
                    if existe:
                        omitidos += 1
                        continue

                    # Crear registro si no es duplicado
                    Anexo1.objects.create(
                        docente=row['Docente'],
                        materia=row['Materia'],
                        carrera=row['Carrera'],
                        semestre=row['Semestre'],
                        actividad=row['Actividad'],
                        tema=row['Tema'],
                        trabajo_independiente=row['Trabajo Independiente'],
                        archivo=ruta_archivo
                    )
                    procesados += 1
                if omitidos ==0 and procesados >0:
                    messages.success(
                        request,
                        f"Archivo procesado exitosamente: {procesados} registros agregados."
                    )
                    return redirect('anexo1_list')
                elif omitidos >0:
                    messages.success(
                        request,
                        f"Archivo procesado exitosamente: {procesados} registros agregados, {omitidos} omitidos por duplicidad."
                    )
                    return redirect('upload_excel')
            except Exception as e:
                messages.error(request, f"Error al procesar el archivo: {e}")
                return redirect('upload_excel')
    else:
        form = Anexo1Form()

    # Obtener el usuario actual desde la sesión
    user = request.session.get('user')

    # Filtrar las asignaturas por el usuario en sesión (campo docente)
    asignaturas_registradas = (
        Anexo1.objects.filter(docente=user)
        .values('materia')
        .distinct()
    )

    return render(request, 'anexo/anexo.html', {
        'form': form,
        'asignaturas_registradas': asignaturas_registradas
    })
