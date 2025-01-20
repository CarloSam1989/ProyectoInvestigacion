from django.urls import path
from .views import *

urlpatterns = [
    path("", CustomLoginView, name="login"),
    path("menu/", menu, name="menu_principal"),
    path("logout/", logout_view, name="logout"),
]
