from django import forms

from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "precio", "descuento"]
        labels = {
            "nombre": "Nombre",
            "precio": "Precio (€)",
            "descuento": "Descuento (%)",
        }
        widgets = {
            "precio": forms.NumberInput(attrs={"min": "0", "step": "0.01"}),
            "descuento": forms.NumberInput(attrs={"min": "0", "max": "100"}),
        }
