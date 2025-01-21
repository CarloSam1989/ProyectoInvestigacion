from django.urls import path
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
]
