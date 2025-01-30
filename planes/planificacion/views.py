
# Create your views here.
import pandas as pd
import os
from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import *
from django.http import HttpResponse
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Table, TableStyle, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Registrar la fuente Arial
pdfmetrics.registerFont(TTFont('Arial', 'static/font/Arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'static/font/Arial_Bold.ttf'))


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

class PlanesListView(SessionAuthRequiredMixin, ListView):
    model = Planes
    template_name = 'planes/planes_list.html'
    context_object_name = 'planes'

    def get_queryset(self):
        # Obtener el usuario de la sesión
        user = self.request.session.get('user')

        if user:
            # Buscar planes donde el docente coincide con el usuario en sesión
            planes = Planes.objects.filter(anexo__docente=user)
            return planes
        else:
            return Planes.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.session.get('user')
        if user:
            planes = Planes.objects.filter(anexo__docente=user)
            if not planes:
                messages.info(self.request, "No existen planes asociados a este docente. Puedes crear uno nuevo.")
        return context


# Vista para crear un nuevo Plan
def crear_plan(request):
    # Obtener el docente desde la sesión
    docente = request.session.get('user')

    if not docente:
        messages.error(request, "No se encontró información del docente.")
        return redirect('planes_list')

    if request.method == 'POST':
        form = PlanesForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            
            # Asociar automáticamente la actividad seleccionada desde Anexo1
            actividad_id = request.POST.get('numero_actividad')
            try:
                actividad_anexo = Anexo1.objects.get(id=actividad_id, docente=docente)
                plan.anexo = actividad_anexo
                plan.numero_actividad = actividad_anexo.actividad
                plan.trabajo_independiente = actividad_anexo.trabajo_independiente
                
                # Almacenar el desarrollo de la clase desde el formulario
                plan.desarrollo_clase = request.POST.get('desarrollo_clase')  # CKEditor guarda HTML
                
                plan.save()

                # Guardar los recursos seleccionados (ManyToManyField)
                recursos = form.cleaned_data['recurso_didactico']
                plan.recurso_didactico.set(recursos)

                messages.success(request, "Plan creado exitosamente.")
                return redirect('planes_list')
            except Anexo1.DoesNotExist:
                messages.error(request, "La actividad seleccionada no es válida.")
        else:
            print(form.errors)
            messages.error(request, "Por favor, corrija los errores en el formulario.")
    else:
        # Filtrar actividades disponibles de Anexo1
        actividades_disponibles = Anexo1.objects.filter(docente=docente).exclude(
            id__in=Planes.objects.values_list('anexo_id', flat=True)
        )
        form = PlanesForm()
        form.fields['numero_actividad'].choices = [
            (actividad.id, f"{actividad.actividad} - {actividad.tema}") for actividad in actividades_disponibles
        ]

    return render(request, 'planes/planes_form.html', {
        'form': form,
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
    estilos.add(ParagraphStyle(name="Arial11b", fontName="Arial-Bold", fontSize=11, leading=14))
    estilos.add(ParagraphStyle(name="Titulo12", fontName="Arial-Bold", fontSize=11, leading=16))
    estilos.add(ParagraphStyle(name="TituloCentrado", fontName="Arial-Bold", fontSize=11, leading=16, alignment=TA_CENTER))


    # Título
    elementos.append(Spacer(1, 10))
    elementos.append(Paragraph(f"PLAN DE CLASES N°: {plan.plan_nombre}", estilos["TituloCentrado"]))
    elementos.append(Paragraph(f"CARRERA: {plan.anexo.carrera.upper()}", estilos["TituloCentrado"]))
    elementos.append(Paragraph(f"ASIGNATURA: {plan.anexo.materia.upper()}", estilos["TituloCentrado"]))
    elementos.append(Spacer(1, 20))
    docente = Paragraph(
        f"<u><b>DOCENTE:</b></u> {plan.anexo.docente.upper()}",
        estilos["Normal"]
    )
    elementos.append(docente)
    num_act = Paragraph(
        f"<b><u>NÚMERO DE ACTIVIDAD:</u></b> {plan.anexo.actividad}",
        estilos["Normal"]
    )
    elementos.append(num_act)
    act_doc = Paragraph(
        f"<b><u>ACTIVIDAD DOCENTE:</u></b> {plan.actividad_docente}",
        estilos["Normal"]
    )
    metodo = Paragraph(
        f"<u><b>MÉTODO:</b></u> {plan.metodo.nombre.upper()}",
        estilos["Normal"]
    )
    elementos.append(metodo)
    forma_ense = Paragraph(
        f"<b><u>FORMA DE ENSEÑANZA:</u></b> {plan.forma_ense.nombre.upper()}",
        estilos["Normal"]
    )
    elementos.append(forma_ense)
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
    elementos.append(Paragraph(f"{plan.anexo.tema}", estilos["Normal"]))
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
    elementos.append(Paragraph(f"{plan.anexo.trabajo_independiente}", estilos["Normal"]))
    elementos.append(Spacer(1, 5))
    elementos.append(Paragraph("III.4. Anuncio del tema de la próxima clase. ", estilos["Titulo12"]))
    elementos.append(Paragraph(f"{plan.anexo.trabajo_independiente}", estilos["Normal"]))
    elementos.append(Spacer(1, 5))
    elementos.append(Paragraph("III.5. Aplicación de técnica de cierre. ", estilos["Titulo12"]))
    elementos.append(Paragraph(f"{plan.tecnica_cierre.nombre}", estilos["Normal"]))
    elementos.append(Spacer(1, 5))
    elementos.append(Paragraph("Bibliografía. ", estilos["Titulo12"]))
    elementos.append(Paragraph(f"{plan.bibliografia}", estilos["Normal"]))
    elementos.append(Spacer(1, 50))
    datos = [
        ["Elaborado Por:", "Revisado Por:"],  # Primera fila vacía
        ["DOCENTE", "COORDINADOR DE CARRERA"]  # Segunda fila con texto
    ]
    # Definir los anchos de columnas y alturas de filas
    ancho_columnas = [150, 150]  # Ambas columnas de 150 puntos
    alto_filas = [20, 80]  # Primera fila más grande (80 puntos), segunda fila más pequeña (40 puntos)
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