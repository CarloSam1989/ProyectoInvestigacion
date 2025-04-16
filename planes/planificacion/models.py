from django.db import models
import os
from django.utils.timezone import now

class Metodos(models.Model):
    nombre = models.CharField(max_length=300)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
class TecnicaCierre(models.Model):
    nombre = models.CharField(max_length=300)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class FormasEnse(models.Model):
    nombre = models.CharField(max_length=300)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
class RecursosDidacticos(models.Model):
    nombre = models.CharField(max_length=300)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
def unico_archivo(instance, filename):
    # Agrega un timestamp para crear una ruta única
    timestamp = now().strftime("%Y%m%d%H%M%S")
    return os.path.join('fechas', f"{timestamp}_{filename}")

class TrabajoFecha(models.Model):
    nombre = models.TextField()
    fecha = models.DateField(null=True, blank=True)
    archivo = models.FileField(upload_to=unico_archivo, null=True, blank=True)

    class Meta:
        app_label = 'planificacion'  # Debe coincidir con la app

    def __str__(self):
        return f"{self.fecha} - {self.nombre}"

def unique_file_path(instance, filename):
    # Agrega un timestamp para crear una ruta única
    timestamp = now().strftime("%Y%m%d%H%M%S")
    return os.path.join('anexos', f"{timestamp}_{filename}")

class Anexo1(models.Model):
    docente = models.TextField()
    materia = models.TextField()
    carrera = models.TextField()
    semestre = models.CharField(max_length=10, default="Unknown")
    numero_actividad = models.IntegerField(default=0)
    tema = models.TextField()
    trabajo_independiente = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    archivo = models.FileField(upload_to=unique_file_path, null=True, blank=True)
   
    class Meta:
        app_label = 'planificacion'
    def __str__(self):
        return f"{self.numero_actividad} - {self.tema}"

class Planes(models.Model):
    metodo = models.ForeignKey(Metodos, on_delete=models.CASCADE)
    plan_nombre = models.TextField(null=True, blank=True)
    tecnica_cierre = models.ManyToManyField(TecnicaCierre, related_name='planes')
    forma_ense = models.ManyToManyField(FormasEnse)
    recurso_didactico = models.ManyToManyField(RecursosDidacticos)
    saludo = models.TextField(null=True, blank=True)
    bibliografia = models.TextField(null=True, blank=True)
    evaluacion_aprendizaje = models.TextField(null=True, blank=True)
    an_tecnica_cierre = models.TextField(null=True, blank=True)
    chequeo_trabajo = models.TextField(null=True, blank=True)
    trabajo_independiente = models.TextField(null=True, blank=True)
    numero_actividad = models.ManyToManyField(Anexo1, related_name='planes')
    actividad_docente = models.CharField(max_length=300)
    asistencia = models.TextField(null=True, blank=True)
    trabajo_fecha = models.ForeignKey(TrabajoFecha, on_delete=models.CASCADE)
    motivacion = models.TextField(null=True, blank=True)
    objetivo = models.TextField(null=True, blank=True)
    desarrollo_clase = models.TextField()
    conclusion = models.CharField(max_length=300, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_ejecucion = models.DateField(null=True, blank=True)
    archivo_firmado = models.FileField(upload_to='planes_firmados/', null=True, blank=True)

    def __str__(self):
        return self.plan_nombre[:50] if self.plan_nombre else "Sin nombre"

