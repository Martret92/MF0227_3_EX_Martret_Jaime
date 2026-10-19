from decimal import Decimal
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import reverse

from .forms import ProductoForm
from .models import Producto


class ProductoModeloTests(TestCase):
    def test_datos_del_profesor(self):
        ejemplos = [
            ("Teclado", "30.00", 0, "30.00"),
            ("Ratón", "20.00", 25, "15.00"),
            ("Monitor", "150.00", 10, "135.00"),
        ]
        for nombre, precio, descuento, esperado in ejemplos:
            with self.subTest(nombre=nombre):
                producto = Producto(nombre=nombre, precio=precio, descuento=descuento)
                producto.full_clean()
                producto.save()
                producto.refresh_from_db()
                self.assertEqual(producto.precio_final(), Decimal(esperado))
                self.assertIsInstance(producto.precio_final(), Decimal)

    def test_validadores_del_modelo_rechazan_valores_invalidos(self):
        for campo, valor in [("precio", Decimal("-0.01")), ("descuento", -1), ("descuento", 101)]:
            with self.subTest(campo=campo, valor=valor):
                producto = Producto(nombre="Prueba", precio=10, descuento=0)
                setattr(producto, campo, valor)
                with self.assertRaises(ValidationError) as error:
                    producto.full_clean()
                self.assertIn(campo, error.exception.message_dict)

    def test_descuento_por_defecto_y_limites(self):
        producto = Producto(nombre="Muestra", precio=Decimal("0.00"))
        self.assertEqual(producto.descuento, 0)
        for descuento in (0, 100):
            producto.descuento = descuento
            producto.full_clean()
            self.assertEqual(producto.precio_final(), Decimal("0"))

    def test_delega_en_las_clases_de_dominio(self):
        producto = Producto(nombre="Prueba", precio=Decimal("100"), descuento=0)
        with patch("catalogo.models.ProductoBase", autospec=True) as base:
            base.return_value.precio_final.return_value = Decimal("100")
            self.assertEqual(producto.precio_final(), Decimal("100"))
            base.assert_called_once_with("Prueba", Decimal("100"))
        producto.descuento = 20
        with patch("catalogo.models.ProductoOferta", autospec=True) as oferta:
            oferta.return_value.precio_final.return_value = Decimal("80")
            self.assertEqual(producto.precio_final(), Decimal("80"))
            oferta.assert_called_once_with("Prueba", Decimal("100"), 20)


class ProductoWebTests(TestCase):
    def setUp(self):
        self.listado = reverse("catalogo:lista_productos")
        self.alta = reverse("catalogo:nuevo_producto")

    def test_rutas_y_listado_vacio(self):
        self.assertEqual(self.listado, "/productos/")
        self.assertEqual(self.alta, "/productos/nuevo/")
        self.assertRedirects(self.client.get("/"), self.listado)
        respuesta = self.client.get(self.listado)
        self.assertContains(respuesta, "Todavía no hay productos registrados.")
        self.assertContains(respuesta, self.alta)

    def test_get_formulario_con_etiquetas_y_csrf(self):
        respuesta = self.client.get(self.alta)
        self.assertEqual(respuesta.status_code, 200)
        self.assertIsInstance(respuesta.context["formulario"], ProductoForm)
        for texto in ("Nombre", "Precio (€)", "Descuento (%)", "csrfmiddlewaretoken"):
            self.assertContains(respuesta, texto)

    def test_post_registra_ejemplos_y_listado_muestra_precios(self):
        for nombre, precio, descuento in [("Teclado", "30.00", 0), ("Ratón", "20.00", 25), ("Monitor", "150.00", 10)]:
            respuesta = self.client.post(self.alta, {"nombre": nombre, "precio": precio, "descuento": descuento})
            self.assertRedirects(respuesta, self.listado)
        self.assertEqual(Producto.objects.count(), 3)
        self.assertEqual(Producto.objects.get(nombre="Ratón").precio_final(), Decimal("15"))
        respuesta = self.client.get(self.listado)
        for texto in ("Teclado", "Ratón", "Monitor", "30.00 €", "20.00 €", "150.00 €", "15.00 €", "135.00 €", "25 %", "10 %"):
            self.assertContains(respuesta, texto)

    def test_post_invalido_muestra_errores_y_no_guarda(self):
        casos = [
            ("precio", "-0.01"),
            ("precio", "no es un precio"),
            ("precio", "1.001"),
            ("precio", "100000000.00"),
            ("descuento", -1),
            ("descuento", 101),
            ("descuento", "1.5"),
            ("nombre", ""),
            ("nombre", "x" * 101),
        ]
        for campo, valor in casos:
            with self.subTest(campo=campo, valor=valor):
                datos = {"nombre": "Prueba", "precio": "10.00", "descuento": 0}
                datos[campo] = valor
                respuesta = self.client.post(self.alta, datos)
                self.assertEqual(respuesta.status_code, 200)
                self.assertIn(campo, respuesta.context["formulario"].errors)
                self.assertContains(respuesta, "No se ha guardado el producto.")
                self.assertContains(respuesta, 'class="errorlist"')
                if campo != "nombre":
                    self.assertContains(respuesta, 'value="Prueba"')
        self.assertEqual(Producto.objects.count(), 0)

    def test_formulario_acepta_limites(self):
        for descuento in (0, 100):
            respuesta = self.client.post(self.alta, {"nombre": "Muestra", "precio": "0.00", "descuento": descuento})
            self.assertRedirects(respuesta, self.listado)
        self.assertEqual(Producto.objects.count(), 2)

    def test_csrf_rechaza_post_sin_token_y_acepta_token_valido(self):
        cliente = Client(enforce_csrf_checks=True)
        datos = {"nombre": "Ratón", "precio": "20.00", "descuento": 25}
        self.assertEqual(cliente.post(self.alta, datos).status_code, 403)
        self.assertEqual(Producto.objects.count(), 0)
        cliente.get(self.alta)
        datos["csrfmiddlewaretoken"] = cliente.cookies["csrftoken"].value
        self.assertRedirects(cliente.post(self.alta, datos), self.listado)
        self.assertEqual(Producto.objects.count(), 1)

    def test_listado_escapa_el_nombre_del_producto(self):
        Producto.objects.create(nombre="<script>alert(1)</script>", precio=10)
        respuesta = self.client.get(self.listado)
        self.assertContains(respuesta, "&lt;script&gt;alert(1)&lt;/script&gt;")
        self.assertNotContains(respuesta, "<script>alert(1)</script>")
