from decimal import Decimal
from unittest import TestCase

from django.test import TestCase as DjangoTestCase

from .dominio import ProductoBase, ProductoOferta


class ProductoTests(TestCase):
    def test_producto_base_conserva_nombre_y_precio(self):
        producto = ProductoBase("Camiseta", 100)
        self.assertEqual(producto.nombre, "Camiseta")
        self.assertIsInstance(producto.precio_final(), Decimal)
        self.assertEqual(producto.precio_final(), Decimal("100"))

    def test_producto_oferta_aplica_descuento(self):
        producto = ProductoOferta("Camiseta", 100, 20)
        self.assertIsInstance(producto, ProductoBase)
        self.assertEqual(producto.descuento, Decimal("20"))
        self.assertIsInstance(producto.precio_final(), Decimal)
        self.assertEqual(producto.precio_final(), Decimal("80"))

    def test_precio_negativo_se_rechaza_en_ambas_clases(self):
        with self.assertRaises(ValueError):
            ProductoBase("Camiseta", -1)
        with self.assertRaises(ValueError):
            ProductoOferta("Camiseta", -1, 20)

    def test_descuentos_fuera_del_intervalo_se_rechazan(self):
        for descuento in (-1, 101):
            with self.subTest(descuento=descuento):
                with self.assertRaises(ValueError):
                    ProductoOferta("Camiseta", 100, descuento)

    def test_limites_del_descuento_son_validos(self):
        self.assertEqual(ProductoOferta("Camiseta", 100, 0).precio_final(), 100)
        self.assertEqual(ProductoOferta("Camiseta", 100, 100).precio_final(), 0)

    def test_precio_cero_es_valido(self):
        self.assertEqual(ProductoBase("Muestra", 0).precio_final(), 0)

    def test_calculo_decimal_no_introduce_error_binario(self):
        producto = ProductoOferta("Muestra", 0.1, Decimal("10"))
        self.assertEqual(producto.precio_final(), Decimal("0.09"))

    def test_valores_no_finitos_se_rechazan(self):
        for valor in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(valor=valor):
                with self.assertRaises(ValueError):
                    ProductoBase("Muestra", valor)
                with self.assertRaises(ValueError):
                    ProductoOferta("Muestra", 100, valor)


class ListadoProductosTests(DjangoTestCase):
    def test_productos_responde_http_200(self):
        respuesta = self.client.get("/productos/")
        self.assertEqual(respuesta.status_code, 200)
