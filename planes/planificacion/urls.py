from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path("", CustomLoginView, name="login"),
    path("menu/", menu, name="menu_principal"),
    path("logout/", logout_view, name="logout"),

    path('metodos/', MetodosListView.as_view(), name='metodos_list'),
    path('metodos/<int:pk>/', MetodosDetailView.as_view(), name='metodos_detail'),
    path('metodos/create/', MetodosCreateView.as_view(), name='metodos_create'),
    path('metodos/<int:pk>/update/', MetodosUpdateView.as_view(), name='metodos_update'),
    path('metodos/<int:pk>/delete/', MetodosDeleteView.as_view(), name='metodos_delete'),

    path('tecnica_cierre/', TecnicaCierreListView.as_view(), name='tecnica_cierre_list'),
    path('tecnica_cierre/<int:pk>/', TecnicaCierreDetailView.as_view(), name='tecnica_cierre_detail'),
    path('tecnica_cierre/create/', TecnicaCierreCreateView.as_view(), name='tecnica_cierre_create'),
    path('tecnica_cierre/<int:pk>/update/', TecnicaCierreUpdateView.as_view(), name='tecnica_cierre_update'),
    path('tecnica_cierre/<int:pk>/delete/', TecnicaCierreDeleteView.as_view(), name='tecnica_cierre_delete'),

    path('recursos_didacticos/', RecursosDidacticosListView.as_view(), name='recursos_didacticos_list'),
    path('recursos_didacticos/<int:pk>/', RecursosDidacticosDetailView.as_view(), name='recursos_didacticos_detail'),
    path('recursos_didacticos/create/', RecursosDidacticosCreateView.as_view(), name='recursos_didacticos_create'),
    path('recursos_didacticos/<int:pk>/update/', RecursosDidacticosUpdateView.as_view(), name='recursos_didacticos_update'),
    path('recursos_didacticos/<int:pk>/delete/', RecursosDidacticosDeleteView.as_view(), name='recursos_didacticos_delete'),

    path('forma_ense/', FormaEnseListView.as_view(), name='forma_ense_list'),
    path('forma_ense/<int:pk>/', FormaEnseDetailView.as_view(), name='forma_ense_detail'),
    path('forma_ense/create/', FormaEnseCreateView.as_view(), name='forma_ense_create'),
    path('forma_ense/<int:pk>/update/', FormaEnseUpdateView.as_view(), name='forma_ense_update'),
    path('forma_ense/<int:pk>/delete/', FormaEnseDeleteView.as_view(), name='forma_ense_delete'),

    path("anexo/upload/", upload_excel, name="upload_excel"),
    path('anexos/<str:materia>/', Anexo1ListView.as_view(), name='anexo1_list'),

    path("trabajofecha/upload/", upload_exceltf, name="upload_tfexcel"),
    path('trabajofecha/<str:materia>/', Trabajo_Fecha.as_view(), name='trabajofecha_list'),

    path('planes/', PlanesListView.as_view(), name='planes_list'),
    path('planes/create/<str:materia>/', crear_plan, name='planes_create'),

    path("plan/<int:plan_id>/", vista_plan_detalle, name="detalle_plan"),
    path("plan/<int:plan_id>/pdf/", generar_plan_pdf, name="plan_pdf"),
    path('planes/<int:plan_id>/subir/', subir_plan_firmado, name='subir_plan_firmado'),

    path('reporte/<str:carrera>/', ReporteMateriasListView.as_view(), name='reporte_materias'),
    path('subir_archivo_firmado/', subir_archivo_firmado, name='subir_archivo_firmado'),
    path('reporte_pdf/<str:carrera>/', generar_reporte_pdf, name='reporte_pdf'),



]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
