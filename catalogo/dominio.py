"""Clases de dominio para representar productos y sus precios."""

from decimal import Decimal


class ProductoBase:
    """Producto con nombre y precio no negativo."""

    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = Decimal(str(precio))
        if not self.precio.is_finite() or self.precio < 0:
            raise ValueError("El precio debe ser un número finito no negativo.")

    def precio_final(self):
        return self.precio


class ProductoOferta(ProductoBase):
    """Producto al que se aplica un descuento porcentual entre 0 y 100."""

    def __init__(self, nombre, precio, descuento):
        super().__init__(nombre, precio)
        self.descuento = Decimal(str(descuento))
        if not self.descuento.is_finite() or not 0 <= self.descuento <= 100:
            raise ValueError("El descuento debe estar comprendido entre 0 y 100.")

    def precio_final(self):
        return super().precio_final() * (1 - self.descuento / Decimal("100"))
