from django.shortcuts import redirect, render

from .forms import ProductoForm
from .models import Producto


def lista_productos(request):
    productos = Producto.objects.order_by("pk")
    return render(request, "catalogo/lista_productos.html", {"productos": productos})


def nuevo_producto(request):
    if request.method == "POST":
        formulario = ProductoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect("catalogo:lista_productos")
    else:
        formulario = ProductoForm()
    return render(request, "catalogo/nuevo_producto.html", {"formulario": formulario})
