from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('planificacion.urls')),  # Incluye las URLs de tu aplicación principal
]
