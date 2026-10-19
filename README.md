# MF0227_3 · Fases 0, 1 y 2

Proyecto inicial para gestionar productos de una tienda con Python y Django.
El proyecto se llama `tienda` y su única aplicación propia es `catalogo`.
Incluye las clases de dominio de la Fase 1 y el modelo, formulario y listado
de productos de la Fase 2. No incluye la Fase 3.

## Requisitos

- Python 3.10 o superior (comprobado con Python 3.12).
- pip y el módulo venv.
- Django 5.2.18, declarado en `requirements.txt`.

Ejecuta los comandos desde la raíz del repositorio, donde está `manage.py`.

## Crear y activar el entorno virtual

```bash
python -m venv .venv
```

Linux y macOS:

```bash
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

## Instalar y preparar la base de datos

```bash
python -m pip install -r requirements.txt
python manage.py migrate
```

SQLite está configurado en `tienda/settings.py`. Las migraciones crean el archivo
local `db.sqlite3`, excluido de Git junto con el entorno virtual y las cachés.
No hace falta instalar un servidor de bases de datos ni configurar credenciales.

## Comprobar y ejecutar

```bash
python manage.py check
python manage.py runserver
```

La raíz redirige al listado `/productos/`. Desde «Añadir producto» se accede a
`/productos/nuevo/`, donde se puede registrar nombre, precio y descuento.
Un alta válida se guarda en SQLite y redirige al listado. Los datos inválidos
muestran sus errores en el formulario sin guardar el producto. Se utiliza CSRF.
Detén el servidor con `Ctrl+C` y sal del entorno virtual con `deactivate`.

## Validación y pruebas

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py migrate
python manage.py test
```

Las ocho pruebas de la Fase 1 se conservan en `catalogo/tests.py`. Las pruebas de
modelo y web están en `catalogo/test_web.py`: validación de datos, guardado mediante
POST, errores visibles, listado, precios finales y protección CSRF.

`Producto.precio_final()` delega en `ProductoBase` cuando no hay descuento y en
`ProductoOferta` cuando lo hay. La plantilla muestra el resultado con dos decimales;
no calcula el descuento. Los validadores estándar del modelo se ejecutan mediante
el `ModelForm` (y mediante `full_clean()` cuando se usa el modelo directamente).
Como es habitual en Django, `save()` por sí solo no ejecuta los validadores.

Se pueden registrar manualmente estos ejemplos, sin datos precargados:

| Nombre | Precio (€) | Descuento (%) | Precio final (€) |
| --- | --- | --- | --- |
| Teclado | 30.00 | 0 | 30.00 |
| Ratón | 20.00 | 25 | 15.00 |
| Monitor | 150.00 | 10 | 135.00 |

## Estructura

```text
manage.py
tienda/
    __init__.py
    settings.py
    urls.py
    asgi.py
    wsgi.py
catalogo/
    __init__.py
    admin.py
    apps.py
    models.py
    dominio.py
    forms.py
    views.py
    urls.py
    tests.py
    test_web.py
    migrations/
        __init__.py
        0001_initial.py
    templates/catalogo/
        base.html
        lista_productos.html
        nuevo_producto.html
requirements.txt
.gitignore
README.md
```

La configuración generada (`DEBUG=True` y clave de desarrollo) está destinada al
desarrollo local; antes de desplegar se requiere una configuración de producción.
