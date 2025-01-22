from django.db import models

class Saludo(models.Model):
    saludo = models.CharField(max_length=500)
    asignatura = models.IntegerField()
    docente = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.saludo

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
    

class Anexo1(models.Model):
    docente = models.TextField()
    materia = models.TextField()
    carrera = models.TextField()
    semestre = models.CharField(max_length=10, default="Unknown")
    actividad = models.CharField(max_length=300)
    tema = models.TextField()
    trabajo_independiente = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    archivo = models.FileField(upload_to='anexo/', null=True, blank=True)

    def __str__(self):
        return f"{self.tema} - {self.semestre}"


class Planes(models.Model):
    metodo = models.ForeignKey(Metodos, on_delete=models.CASCADE)
    tecnica_cierre = models.ForeignKey(TecnicaCierre, on_delete=models.CASCADE)
    forma_ense = models.ForeignKey(FormasEnse, on_delete=models.CASCADE)
    recurso_didactico = models.ForeignKey(RecursosDidacticos, on_delete=models.CASCADE)
    anexo = models.ForeignKey(Anexo1, on_delete=models.CASCADE)
    numero_actividad = models.CharField(max_length=100)
    actividad_docente = models.CharField(max_length=300)
    asistencia = models.CharField(max_length=400)
    trabajo_fecha = models.CharField(max_length=400)
    trabajo_independiente = models.CharField(max_length=400)
    motivacion = models.CharField(max_length=800)
    objetivo = models.CharField(max_length=800)
    desarrollo_clase = models.JSONField() 
    conclusion = models.CharField(max_length=300)
    evaluacion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_clase