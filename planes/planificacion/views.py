
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
from django.db.models import Q

USUARIOS = {
    "admin": "admin",
    "user1": "admin",
    "user2": "admin"
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
    fields = ['nombre', 'descripcion']
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
    fields = ['nombre', 'descripcion']
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
    fields = ['nombre', 'descripcion']
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
    fields = ['nombre', 'descripcion']
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

# Vista para ver detalles de un método
class SaludoDetailView(SessionAuthRequiredMixin, DetailView):
    model = Saludo
    template_name = 'saludo/saludo_detail.html'
    context_object_name = 'saludo'

# Vista para crear un nuevo método
class SaludoCreateView(SessionAuthRequiredMixin, CreateView):
    model = Saludo
    template_name = 'saludo/saludo_form.html'
    fields = ['saludo', 'asignatura']
    success_url = reverse_lazy('saludo_list')

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


def anexo1_semestre_list(request, semestre):
    anexos = Anexo1.objects.filter(semestre=semestre).order_by("fecha")
    return render(request, "anexo/list.html", {"anexos": anexos, "semestre": semestre})

class Anexo1ListView(ListView):
    model = Anexo1
    template_name = 'anexo/list.html'
    context_object_name = 'anexos'

    def get_queryset(self):
        return Anexo1.objects.all().order_by('actividad')

def upload_excel(request):
    if request.method == 'POST':
        form = Anexo1Form(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            ruta_archivo = os.path.join('anexos', archivo.name)

            try:
                # Guardar el archivo en el sistema de archivos
                with open(os.path.join(settings.MEDIA_ROOT, ruta_archivo), 'wb+') as destino:
                    for chunk in archivo.chunks():
                        destino.write(chunk)

                # Leer el archivo Excel
                df = pd.read_excel(archivo)

                # Validar las columnas requeridas
                required_columns = [
                    'Docente', 'Materia', 'Carrera', 'Semestre', 
                    'Actividad', 'Tema', 'Trabajo Independiente'
                ]
                for column in required_columns:
                    if column not in df.columns:
                        messages.error(request, f"Error: Falta la columna '{column}' en el archivo.")
                        return redirect('anexo1_list')

                # Crear registros en la base de datos
                for _, row in df.iterrows():
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

                messages.success(request, "Datos cargados exitosamente.")
                return redirect('anexo1_list')
            except Exception as e:
                messages.error(request, f"Error al procesar el archivo: {e}")
                return redirect('anexo1_list')
    else:
        form = Anexo1Form()
    return render(request, 'anexo/anexo.html', {'form': form})