from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .dominio import ProductoBase, ProductoOferta


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
    )
    descuento = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    def precio_final(self):
        if self.descuento == 0:
            producto = ProductoBase(self.nombre, self.precio)
        else:
            producto = ProductoOferta(self.nombre, self.precio, self.descuento)
        return producto.precio_final()

    def __str__(self):
        return self.nombre
