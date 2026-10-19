from django.urls import path

from . import views

app_name = "catalogo"

urlpatterns = [
    path("productos/", views.lista_productos, name="lista_productos"),
    path("productos/nuevo/", views.nuevo_producto, name="nuevo_producto"),
]
