from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from datetime import datetime
import os
from collections import defaultdict
from django.db.models import Count, Q
from django.conf import settings
from django.template.loader import get_template
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from .models import *
from .forms import *
from django.http import HttpResponse,JsonResponse
from reportlab.lib.enums import TA_CENTER
from urllib.parse import unquote  # Correcto
from reportlab.lib.pagesizes import letter
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Table, TableStyle, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from urllib.parse import unquote
from xhtml2pdf import pisa


# Registrar la fuente Arial
pdfmetrics.registerFont(TTFont('Arial', 'static/font/Arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'static/font/Arial_Bold.ttf'))


USUARIOS = {
    "admin": "admin",
    "user1": "Carlos",
    "Ing. Carlos Guzman": "Carlos",
    "Ing. Jorge Jaramillo": "Jorge"
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
            request.session["rol"] = "Coordinador"
            request.session["nombre_coordinador"] = "Ing. Jorge Jaramillo"
            request.session["materia_cor"] = ["Desarrollo de Software", "REDES Y TELECOMUNICACIONES"]
            return redirect(request.GET.get("next", "menu_principal"))
        else:
            messages.error(request, "Usuario o contraseña incorrectos. Intenta de nuevo.")

    return render(request, "login.html")
@csrf_exempt
def recibir_datos(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)

            # --- ✅ INICIO: Nueva Lógica de Autenticación ---

            # 1. Extraemos la información clave del JSON
            persona_info = datos.get('persona', {})
            distributivo = datos.get('distributivo_activo', [])
            
            # Verificamos que los datos mínimos existan
            if not persona_info or not distributivo:
                return JsonResponse({
                    'success': False, 
                    'mensaje': 'Faltan datos de persona o distributivo en la petición.'
                }, status=400)

            # 2. Creamos la sesión del usuario con los datos recibidos
            #    (Igual que hacía tu antiguo login)
            request.session["user"] = persona_info.get('nombres', 'Usuario Anónimo')
            request.session["rol"] = "Docente"  # Puedes extraer esto del token si lo decodificas
            request.session["nombre_completo"] = f"{persona_info.get('nombres')} {persona_info.get('apellidos')}"
            
            # 3. Procesamos la lista de materias para la plantilla
            #    Extraemos el nombre de la carrera de cada materia
            materias = [item.get('carrera') for item in distributivo]
            # Usamos set() para obtener las carreras únicas y evitar duplicados
            request.session["materia_cor"] = list(set(materias))
            
            # --- ✅ FIN: Lógica de Autenticación ---

            # 4. Respondemos con éxito y la URL a la que se debe redirigir
            return JsonResponse({
                'success': True,
                'mensaje': 'Autenticación exitosa. Redirigiendo al menú principal...',
                'redirect_url': reverse('menu_principal') # Genera la URL a /menu/ dinámicamente
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'mensaje': 'Error: El formato del JSON es inválido.'
            }, status=400)
    else:
        return JsonResponse({
            'success': False,
            'mensaje': 'Error: Este endpoint solo acepta peticiones POST.'
        }, status=405)



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

class Anexo1ListView(SessionAuthRequiredMixin, ListView):
    model = Anexo1
    template_name = 'anexo/list.html'
    context_object_name = 'anexos'

    def get_queryset(self):
        # Obtener el 'id' desde los parámetros de la URL
        materia = self.kwargs.get('materia')  # Usar kwargs para acceder al parámetro 'id'

        if materia:
            # Filtrar por materia si el id está presente
            return Anexo1.objects.filter(materia=materia).order_by('numero_actividad')
        else:
            # Si no hay id, devolver todos los registros
            return Anexo1.objects.all().order_by('numero_actividad')

class Trabajo_Fecha(SessionAuthRequiredMixin, ListView):
    model = TrabajoFecha
    template_name = 'trabajo_fecha/list.html'
    context_object_name = 'trabajo_fecha'

    def get_queryset(self):
        # Obtener el 'id' desde los parámetros de la URL
        fecha = self.kwargs.get('fecha')  # Usar kwargs para acceder al parámetro 'id'

        if fecha:
            # Filtrar por materia si el id está presente
            return TrabajoFecha.objects.filter(fecha=fecha).order_by('fecha')
        else:
            # Si no hay id, devolver todos los registros
            return TrabajoFecha.objects.all().order_by('fecha')

class PlanesListView(SessionAuthRequiredMixin, ListView):
    model = Planes
    template_name = 'planes/planes_list.html'
    context_object_name = 'planes'

    def get_queryset(self):
        user = self.request.session.get('user')
        materia = self.request.GET.get('materia')

        if user:
            queryset = Planes.objects.filter(numero_actividad__docente=user).distinct().prefetch_related('numero_actividad')
            if materia:
                queryset = queryset.filter(numero_actividad__materia=materia)
            return queryset
        return Planes.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.session.get('user')

        if user:
            # Obtener todas las materias donde el docente tiene actividades
            todas_las_materias = (
                Anexo1.objects.filter(docente=user)
                .values_list('materia', flat=True)
                .distinct()
            )

            # Crear un diccionario con todas las materias, asegurando que las vacías también estén
            planes_por_materia = {materia: [] for materia in todas_las_materias}

            # Llenar solo las materias que tienen planes
            for plan in context['planes']:
                if plan.numero_actividad.exists():
                    materia = plan.numero_actividad.first().materia
                    planes_por_materia[materia].append(plan)

            # Convertir a lista de tuplas para facilitar la iteración en la plantilla
            context['planes_por_materia'] = list(planes_por_materia.items())
            context['materias_disponibles'] = todas_las_materias
            context['user'] = user
            context['materia_seleccionada'] = self.request.GET.get('materia', todas_las_materias.first() if todas_las_materias else None)

        return context

def crear_plan(request, materia):
    docente = request.session.get('user')
    if not docente:
        messages.error(request, "No se encontró información del docente.")
        return redirect('planes_list')

    # 🔹 Excluir actividades que ya fueron seleccionadas
    actividades_disponibles = Anexo1.objects.filter(
        docente=docente, materia=materia
    ).exclude(id__in=Planes.objects.values_list('numero_actividad', flat=True))

    if not actividades_disponibles.exists():
        messages.error(request, "No hay actividades disponibles para esta materia.")
        return redirect('planes_list')

    # 🔹 Obtener el número del próximo plan
    ultimo_plan = Planes.objects.filter(numero_actividad__materia=materia).order_by('-id').first()
    nuevo_numero_plan = f"{int(ultimo_plan.plan_nombre.split()[-1]) + 1}" if ultimo_plan else "1"

    # 🔹 PAGINAR DE 8 EN 8
    page = request.GET.get('page', 1)
    paginator = Paginator(actividades_disponibles, 8)  
    actividades_paginadas = paginator.get_page(page)  # Obtenemos la página actual

    if request.method == 'POST':
        form = PlanesForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.plan_nombre = nuevo_numero_plan
            plan.desarrollo_clase = request.POST.get('desarrollo_clase')
            plan.save()
            plan.numero_actividad.set(form.cleaned_data.get('numero_actividad', []))
            plan.recurso_didactico.set(form.cleaned_data.get('recurso_didactico', []))
            plan.forma_ense.set(form.cleaned_data.get('forma_ense', []))
            plan.tecnica_cierre.set(form.cleaned_data.get('tecnica_cierre', []))
            messages.success(request, "Plan creado exitosamente.")
            return redirect('planes_list')
        else:
            messages.error(request, "Por favor, corrija los errores en el formulario.")
    else:
        form = PlanesForm(initial={'plan_nombre': nuevo_numero_plan})
        form.fields['numero_actividad'].queryset = actividades_paginadas.object_list  # Cargamos solo las actividades de la página actual

    return render(request, 'planes/planes_form.html', {
        'form': form,
        'materia': materia,
        'actividades_paginadas': actividades_paginadas,  # Pasamos la paginación a la plantilla
    })

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
                        numero_actividad=row['Actividad'],
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
                        numero_actividad=row['Actividad'],
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

def upload_exceltf(request):
    if request.method == 'POST':
        form = TrabajoFechaForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']

            try:
                # Leer el archivo Excel
                df = pd.read_excel(archivo)

                # Validar columnas requeridas
                required_columns = ['Fecha', 'Nombre']
                for column in required_columns:
                    if column not in df.columns:
                        messages.error(request, f"Error: Falta la columna '{column}' en el archivo.")
                        return redirect('upload_tfexcel')

                # Guardar el archivo en la carpeta de medios con un nombre único
                ruta_archivo = os.path.join('fecha', archivo.name)
                with open(os.path.join(settings.MEDIA_ROOT, ruta_archivo), 'wb+') as destino:
                    for chunk in archivo.chunks():
                        destino.write(chunk)

                # Procesar cada fila del Excel
                procesados = 0
                omitidos = 0
                for _, row in df.iterrows():
                    if isinstance(row['Fecha'], datetime):
                        fecha = row['Fecha'].date().isoformat()  # Convierte a YYYY-MM-DD
                    else:
                        fecha = str(row['Fecha'])  # Asegura que sea string
                    
                    # Validar duplicados basados en el nombre y fecha
                    if TrabajoFecha.objects.filter(nombre=row['Nombre'], fecha=fecha).exists():
                        omitidos += 1
                        continue

                    # Crear registro si no es duplicado
                    TrabajoFecha.objects.create(
                        nombre=row['Nombre'],
                        fecha=fecha,
                        archivo=ruta_archivo
                    )
                    procesados += 1

                if omitidos == 0 and procesados > 0:
                    messages.success(request, f"Archivo procesado exitosamente: {procesados} registros agregados.")
                    return redirect('trabajo_fecha_list')
                elif omitidos > 0:
                    messages.success(request, f"Archivo procesado exitosamente: {procesados} registros agregados, {omitidos} omitidos por duplicidad.")
                    return redirect('upload_tfexcel')
            except Exception as e:
                messages.error(request, f"Error al procesar el archivo: {e}")
                return redirect('upload_tfexcel')
    else:
        form = TrabajoFechaForm()

    # 🔹 Obtener todas las fechas para enviarlas al template
    fechas = TrabajoFecha.objects.all()

    return render(request, 'trabajo_fecha/fecha.html', {
        'form': form,
        'fechas': fechas  # Pasar la lista de fechas a la plantilla
    })

def vista_plan_detalle(request, plan_id):
    plan = get_object_or_404(Planes, id=plan_id)
    return render(request, "planes/reporte_planes.html", {"plan": plan})


ENCABEZADO_IMG = "media/img/encabezado.jpg"
PIE_IMG = "media/img/pie.jpg"

def encabezado(canvas, doc):
    """Dibuja el encabezado en cada página."""
    canvas.saveState()
    if os.path.exists(ENCABEZADO_IMG):
        canvas.drawImage(ENCABEZADO_IMG, 0, 740, width=620, height=60)
    canvas.restoreState()

def pie_pagina(canvas, doc):
    """Dibuja el pie de página en cada página."""
    canvas.saveState()
    if os.path.exists(PIE_IMG):
        canvas.drawImage(PIE_IMG, 0, 0, width=620, height=50)
    canvas.restoreState()

def generar_plan_pdf(request, plan_id):
    plan = get_object_or_404(Planes, id=plan_id)
    tecnicacierr= plan.tecnica_cierre.all()
    formasense= plan.forma_ense.all()
    activi = plan.numero_actividad.all()
    recursos = plan.recurso_didactico.all()
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="plan_{plan_id}.pdf"'

    doc = BaseDocTemplate(response, pagesize=letter)

    # Definir marco de contenido (deja espacio para encabezado y pie)
    frame = Frame(40, 80, 500, 650, id="normal")

    # Agregar plantilla con encabezado y pie
    plantilla = PageTemplate(id="plantilla", frames=frame, onPage=encabezado, onPageEnd=pie_pagina)
    doc.addPageTemplates([plantilla])

    elementos = []

    # Estilos
    estilos = getSampleStyleSheet()
    estilos.add(ParagraphStyle(name="Arial11", fontName="Arial", fontSize=11, leading=14))
    estilos.add(ParagraphStyle(name="Sangria",parent=estilos["Normal"],firstLineIndent=30))
    estilos.add(ParagraphStyle(name="Sangrias",parent=estilos["Normal"],firstLineIndent=390))
    estilos.add(ParagraphStyle(name="Arial11b", fontName="Arial-Bold", fontSize=11, leading=14))
    estilos.add(ParagraphStyle(name="Titulo12", fontName="Arial-Bold", fontSize=11, leading=16))
    estilos.add(ParagraphStyle(name="TituloCentrado", fontName="Arial-Bold", fontSize=11, leading=16, alignment=TA_CENTER))

    anexo = plan.numero_actividad.first()
    # Título
    elementos.append(Spacer(1, 10))
    elementos.append(Paragraph(f"PLAN DE CLASES N°: {plan.plan_nombre}", estilos["TituloCentrado"]))
    elementos.append(Paragraph(f"CARRERA: {anexo.carrera.upper()}", estilos["TituloCentrado"]))
    elementos.append(Paragraph(f"ASIGNATURA: {anexo.materia.upper()}", estilos["TituloCentrado"]))
    elementos.append(Spacer(1, 10))
    fecha = Paragraph(
        f"<u><b>FECHA: </b></u> {plan.fecha_ejecucion}",
        estilos["Sangrias"]
    )
    elementos.append(fecha)
    docente = Paragraph(
        f"<u><b>DOCENTE:</b></u> {anexo.docente.upper()} ",
        estilos["Normal"]
    )
    elementos.append(docente)
    actividad_texto = "<b><u>NÚMERO DE ACTIVIDAD:</u></b> "
    for forma in activi:
        actividad_texto += f"{forma.numero_actividad}, "

    # Quitar la última coma y espacio
    actividad_texto = actividad_texto.rstrip(", ")
    # Crear el párrafo con los recursos didácticos
    actividad_texto = Paragraph(actividad_texto, estilos["Normal"])
    # Agregar ambos párrafos a los elementos del PDF
    elementos.append(actividad_texto)
    act_doc = Paragraph(
        f"<b><u>ACTIVIDAD DOCENTE:</u></b> {plan.actividad_docente}",
        estilos["Normal"]
    )
    elementos.append(act_doc)
    metodo = Paragraph(
        f"<u><b>MÉTODO:</b></u> {plan.metodo.nombre.upper()}",
        estilos["Normal"]
    )
    elementos.append(metodo)
    formaense_texto = "<b><u>FORMA DE ENSEÑANZA:</u></b> "
    for forma in formasense:
        formaense_texto += f"{forma.nombre.upper()}, "

    # Quitar la última coma y espacio
    formaense_texto = formaense_texto.rstrip(", ")
    # Crear el párrafo con los recursos didácticos
    formaense_texto = Paragraph(formaense_texto, estilos["Normal"])
    # Agregar ambos párrafos a los elementos del PDF
    elementos.append(formaense_texto)
    recursos_texto = "<b><u>RECURSOS DIDÁCTICOS:</u></b> "
    for recurso in recursos:
        recursos_texto += f"{recurso.nombre.upper()}, "

    # Quitar la última coma y espacio
    recursos_texto = recursos_texto.rstrip(", ")
    # Crear el párrafo con los recursos didácticos
    recursos_parrafo = Paragraph(recursos_texto, estilos["Normal"])
    # Agregar ambos párrafos a los elementos del PDF
    elementos.append(recursos_parrafo)
    elementos.append(Spacer(1, 10))
    introduccion = Paragraph(
        f"<b>I. <u> INTRODUCCIÓN</u></b>",
        estilos["Sangria"]
    )
    elementos.append(introduccion)
    elementos.append(Paragraph("I.1. Saludo y organización de la clase. ", estilos["Titulo12"]))
    elementos.append(Paragraph(f"{plan.saludo}", estilos["Normal"]))
    elementos.append(Spacer(1, 5))
    elementos.append(Paragraph("I.2. Análisis de la asistencia a clases. ", estilos["Titulo12"]))
    elementos.append(Paragraph(f"{plan.asistencia}", estilos["Normal"]))
    elementos.append(Spacer(1, 5))
    elementos.append(Paragraph("I.3. Trabajo con la fecha. ", estilos["Titulo12"]))
    elementos.append(Paragraph(f"{plan.trabajo_fecha}", estilos["Normal"]))
    elementos.append(Spacer(1, 5))
    elementos.append(Paragraph("I.4. Análisis de la técnica de cierre. ", estilos["Titulo12"]))
    elementos.append(Paragraph(f"{plan.an_tecnica_cierre}", estilos["Normal"]))
    elementos.append(Spacer(1, 5))
    elementos.append(Paragraph("I.5. Chequeo del trabajo independiente. ", estilos["Titulo12"]))
    elementos.append(Paragraph(f"{plan.trabajo_independiente}", estilos["Normal"]))
    elementos.append(Spacer(1, 5))
    elementos.append(Paragraph("I.6. Motivación a la clase. ", estilos["Titulo12"]))
    elementos.append(Paragraph(f"{plan.motivacion}", estilos["Normal"]))
    elementos.append(Spacer(1, 5))
    elementos.append(Paragraph("I.7. Anuncio del tema de la clase. ", estilos["Titulo12"]))
    elementos.append(Paragraph(f"{plan.actividad_docente}", estilos["Normal"]))
    elementos.append(Spacer(1, 5))
    elementos.append(Paragraph("I.8. Anuncio del objetivo de la clase. ", estilos["Titulo12"]))
    elementos.append(Paragraph(f"{plan.objetivo}", estilos["Normal"]))
    elementos.append(Spacer(1, 10))
    desarrollo = Paragraph(
        f"<b>II. <u> DESARROLLO</u></b>",
        estilos["Sangria"]
    )
    elementos.append(desarrollo)
    elementos.append(Spacer(1, 5))
    elementos.append(Paragraph(f"{plan.desarrollo_clase}", estilos["Normal"]))
    elementos.append(Spacer(1, 10))
    desarrollo = Paragraph(
        f"<b>III. <u> CONCLUSIONES GENERALES</u></b>",
        estilos["Sangria"]
    )
    elementos.append(desarrollo)
    elementos.append(Spacer(1, 5))
    elementos.append(Paragraph("III.1. Conclusiones de la clase. ", estilos["Titulo12"]))
    elementos.append(Paragraph(f"{plan.conclusion}", estilos["Normal"]))
    elementos.append(Spacer(1, 5))
    elementos.append(Paragraph("III.2. Evaluación del aprendizaje en la clase. ", estilos["Titulo12"]))
    elementos.append(Paragraph(f"{plan.evaluacion_aprendizaje}", estilos["Normal"]))
    elementos.append(Spacer(1, 5))
    elementos.append(Paragraph("III.3. Orientación del trabajo independiente. ", estilos["Titulo12"]))
    elementos.append(Paragraph(f"{plan.actividad_docente}", estilos["Normal"]))
    elementos.append(Spacer(1, 5))
    elementos.append(Paragraph("III.4. Anuncio del tema de la próxima clase. ", estilos["Titulo12"]))
    elementos.append(Paragraph(f"{plan.actividad_docente}", estilos["Normal"]))
    elementos.append(Spacer(1, 5)) 
    recursos_texto = "<b>III.5. Aplicación de técnica de cierre</b><br/> "
    for recurso in tecnicacierr:
        recursos_texto += f"{recurso.nombre.upper()}, "

    # Quitar la última coma y espacio
    recursos_texto = recursos_texto.rstrip(", ")
    # Crear el párrafo con los recursos didácticos
    recursos_parrafo = Paragraph(recursos_texto, estilos["Normal"])
    # Agregar ambos párrafos a los elementos del PDF
    elementos.append(recursos_parrafo)
    elementos.append(Spacer(1, 5))
    elementos.append(Paragraph("Bibliografía. ", estilos["Titulo12"]))
    elementos.append(Paragraph(f"{plan.bibliografia}", estilos["Normal"]))
    elementos.append(Spacer(1, 50))
    nombre_docente = request.session.get("user", "DOCENTE")
    nombre_coordinador = request.session.get("nombre_coordinador", "COORDINADOR DE CARRERA")
    datos = [
        ["Elaborado Por:", "Revisado Por:"],  # Primera fila vacía
        [nombre_docente.upper(), nombre_coordinador.upper()],
        ["DOCENTE", "COORDINADOR DE CARRERA"]  # Segunda fila con texto
    ]
    # Definir los anchos de columnas y alturas de filas
    ancho_columnas = [150, 150]  # Ambas columnas de 150 puntos
    alto_filas = [20, 80, 20]  # Primera fila más grande (80 puntos), segunda fila más pequeña (40 puntos)
    # Crear la tabla con tamaños personalizados
    tabla = Table(datos, colWidths=ancho_columnas, rowHeights=alto_filas)
    # Aplicar estilos a la tabla
    tabla.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),  # Bordes de la tabla
        ("ALIGN", (0, 1), (-1, -1), "CENTER"),  # Alinear todo al centro excepto la primera fila
        ("ALIGN", (0, 0), (-1, 0), "LEFT"),  # Alinear primera fila a la izquierda
        ("VALIGN", (0, 0), (-1, 0), "BOTTOM"),  # Alinear la primera fila en la parte inferior
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),  # Toda la tabla en negrita
    ]))
    elementos.append(tabla)
    elementos.append(Spacer(1, 20))
    # Construir PDF
    doc.build(elementos)

    return response

class ReporteMateriasListView(ListView):
    model = Anexo1
    template_name = 'reportes/reporte.html'
    context_object_name = 'materias'

    def get_queryset(self):
        """Obtiene las materias y cursos asociados al docente en la carrera seleccionada."""
        carrera = self.kwargs.get('carrera')
        user = self.request.session.get('user')

        if carrera:
            carrera = unquote(carrera)  # Decodificar el nombre de la carrera

        if user and carrera:
            materias = (
                Anexo1.objects.filter(docente=user, carrera=carrera)
                .values('materia', 'semestre')  # Obtener materia y curso (semestre)
                .distinct()
            )
            return materias
        return []

    def get_context_data(self, **kwargs):
        """Organiza las materias por curso y obtiene los planes de clase asociados."""
        context = super().get_context_data(**kwargs)
        carrera = self.kwargs.get('carrera')

        if carrera:
            carrera = unquote(carrera)

        # Agrupar materias por curso (semestre)
        materias_por_curso = defaultdict(list)
        for item in self.get_queryset():
            materias_por_curso[item['semestre']].append(item['materia'])

        # Obtener las materias que tienen planes de clase
        materias_con_planes = set(
            Anexo1.objects.filter(carrera=carrera, planes__isnull=False)
            .values_list('materia', flat=True)
            .distinct()
        )

        # Obtener los planes organizados por materia
        planes_por_materia = {
            materia: Planes.objects.filter(
                numero_actividad__materia=materia,
                archivo_firmado__isnull=False
            ).exclude(archivo_firmado='').distinct()
            for materia in materias_con_planes
        }

        # Depuración (Puedes removerlo después de verificar)
        print("Materias por curso:", dict(materias_por_curso))
        print("Materias con planes:", materias_con_planes)
        print("Planes por materia:", {k: list(v) for k, v in planes_por_materia.items()})

        context['carrera'] = carrera
        context['materias_por_curso'] = dict(materias_por_curso)  # Convertir defaultdict a dict
        context['materias_con_planes'] = materias_con_planes
        context['planes_por_materia'] = planes_por_materia
        return context
    
def subir_plan_firmado(request, plan_id):
    plan = get_object_or_404(Planes, id=plan_id)
    if request.method == 'POST' and request.FILES.get('archivo_firmado'):
        archivo = request.FILES['archivo_firmado']
        plan.archivo_firmado = archivo
        plan.save()
    return redirect('planes_list')  # Ej: 'planes_list'

@csrf_exempt
def subir_archivo_firmado(request):
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        archivo = request.FILES.get('archivo_firmado')

        if plan_id and archivo:
            try:
                plan = Planes.objects.get(id=plan_id)
                plan.archivo_firmado = archivo
                plan.save()
                messages.success(request, "Archivo firmado actualizado correctamente.")
            except Planes.DoesNotExist:
                messages.error(request, "No se encontró el plan.")
        else:
            messages.error(request, "Datos incompletos.")
    
    # Redirigir a donde estabas antes
    return redirect(request.META.get('HTTP_REFERER', '/'))

def generar_reporte_pdf(request, carrera):
    carrera = unquote(carrera.strip())
    datos = defaultdict(lambda: defaultdict(list))

    materias = (
        Anexo1.objects.filter(carrera__iexact=carrera)
        .values('semestre', 'materia', 'docente')
        .distinct()
    )

    for item in materias:
        semestre = item['semestre']
        materia = item['materia']
        docente = item['docente']
        planes_count = Planes.objects.filter(
            numero_actividad__materia=materia
        ).distinct().count()
        planes_firmados = Planes.objects.filter(
            numero_actividad__materia=materia,
            archivo_firmado__isnull=False
        ).exclude(archivo_firmado='').distinct().count()

        datos[semestre][materia].append({
            'materia': materia,
            'semestre': semestre,
            'planes': planes_count,
            'docente': docente,
            'firmados': planes_firmados
        })

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="reporte_planes.pdf"'

    doc = BaseDocTemplate(response, pagesize=letter)
    frame = Frame(40, 80, 500, 650, id="normal")
    plantilla = PageTemplate(
        id="plantilla",
        frames=frame,
        onPage=encabezado,
        onPageEnd=pie_pagina
    )
    doc.addPageTemplates([plantilla])

    elementos = []
    estilos = getSampleStyleSheet()
    estilos.add(ParagraphStyle(
        name="TituloCentrado",
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        alignment=TA_CENTER
    ))

    elementos.append(Spacer(1, 20))
    elementos.append(Paragraph(f"REPORTE DE PLANES DE CLASE - {carrera.upper()}", estilos["TituloCentrado"]))
    elementos.append(Spacer(1, 10))

    for semestre, materias_dict in sorted(datos.items()):
        elementos.append(Paragraph(f"Semestre: {semestre}", estilos["Heading3"]))
        data = [["Materia", "Docente", "Total Planes", "Firmados", "Observaciones"]]

        for materia, registros in materias_dict.items():
            for registro in registros:
                # Buscar todos los planes asociados a esa materia
                planes_ids = Planes.objects.filter(
                    numero_actividad__materia=registro["materia"]
                ).values_list('id', flat=True)

                # Contar todas las observaciones para esos planes
                observaciones_count = ObservacionPlan.objects.filter(
                    plan_id__in=planes_ids
                ).count()

                fila = [
                    registro["materia"],
                    registro["docente"],
                    str(registro["planes"]),
                    str(registro["firmados"]),
                    str(observaciones_count)
                ]
                data.append(fila)

        tabla = Table(data, colWidths=[170, 110, 80, 80, 80])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))

        elementos.append(tabla)
        elementos.append(Spacer(1, 15))

    doc.build(elementos)

    return response


def agregar_observacion(request):
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        observacion_texto = request.POST.get('observacion')
        plan = get_object_or_404(Planes, pk=plan_id)

        ObservacionPlan.objects.create(
            plan=plan,
            observacion=observacion_texto,
            autor=request.user if request.user.is_authenticated else None
        )

        messages.success(request, "¡Observación guardada correctamente!")
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
class PlanesUpdateView(SessionAuthRequiredMixin, UpdateView):
    model = Planes
    form_class = PlanesForm
    template_name = 'planes/planes_form.html'

    def get_success_url(self):
        return reverse_lazy('planes_list') 
