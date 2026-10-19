# MF0227_3 · Gestión de productos de una tienda

Aplicación académica para registrar productos y consultar sus precios finales.
El proyecto se llama `tienda` y su única aplicación propia es `catalogo`.
Incluye la programación orientada a objetos (Fase 1), la aplicación web con base
de datos (Fase 2) y las pruebas y documentación para la entrega (Fase 3).

## Tecnologías

- **Python** para la lógica de dominio, con `Decimal` para los importes.
- **Django** para modelos, formularios, vistas, rutas, plantillas y pruebas.
- **SQLite** como base de datos local, sin servidor adicional.
- HTML y CSS básico, sin dependencias externas para la interfaz.

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

Para utilizar la aplicación:

1. Abre la dirección local que indica el servidor, normalmente `http://127.0.0.1:8000/`.
2. Pulsa «Añadir producto» y rellena nombre, precio y descuento porcentual.
   El nombre admite hasta 100 caracteres, el precio debe ser no negativo y tener
   como máximo dos decimales, y el descuento debe ser un entero entre 0 y 100.
3. Pulsa «Guardar producto». Si hay errores, corrige los campos indicados.
4. El listado muestra los productos guardados con nombre, precio original,
   descuento y precio final. «Volver al listado» permite salir del formulario.

## Validación y pruebas

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py migrate
python manage.py test
```

La suite contiene 20 pruebas. En `catalogo/tests.py` se conservan las ocho pruebas
de la Fase 1 y se añade la comprobación explícita de HTTP 200 en `/productos/`.
Este archivo también comprueba que 100 € con un descuento del 20 % devuelve
exactamente `Decimal("80")`, como exige el ejercicio 5.

Las pruebas de modelo y web se conservan en `catalogo/test_web.py`: validación de
datos, guardado mediante POST, errores visibles, listado, precios finales y CSRF.
Los ejemplos se registran mediante el formulario en una base de datos SQLite
de pruebas aislada que Django crea y destruye automáticamente; no se insertan
productos de ejemplo en `db.sqlite3` ni se distribuyen datos precargados.

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

`dominio.py` contiene `ProductoBase` y `ProductoOferta`; `models.py` define el
modelo persistente `Producto`. `forms.py`, `views.py`, `urls.py` y las plantillas
conectan el formulario y el listado con SQLite. La migración crea su tabla.

## Seguridad antes del despliegue

La configuración incluida es de desarrollo. Antes de desplegar en producción,
**desactiva `DEBUG` y carga `SECRET_KEY` desde una variable de entorno**, evitando
guardar una clave de producción en el código o en Git. Por ejemplo, en la
configuración de producción:

```python
import os

DEBUG = False
SECRET_KEY = os.environ["SECRET_KEY"]
```

Configura `SECRET_KEY` de forma segura en el entorno del servidor, con un valor
aleatorio propio. Este ejemplo describe la preparación para producción; no
modifica la configuración de desarrollo del proyecto. También deben configurarse
los dominios permitidos (`ALLOWED_HOSTS`) y utilizarse un servidor de producción.

## Preparar el ZIP de entrega

El archivo debe llamarse **`Martret_Jaime_MF0227.zip`** y contener únicamente el
proyecto definitivo. Tras revisar y fusionar la Fase 3, desde la raíz del
repositorio y con el trabajo guardado en Git, actualiza `main` y genera el ZIP:

```bash
git switch main
git pull --ff-only origin main
git status --short
git archive --format=zip --output=../Martret_Jaime_MF0227.zip HEAD
```

Comprueba que `git status --short` esté vacío antes de empaquetar. `git archive`
incluye los archivos del commit seleccionado: código, modelos, migraciones,
formularios, vistas, plantillas, pruebas, README, requirements.txt y `.gitignore`.
No incluye `.git/`, archivos locales ignorados ni archivos sin seguimiento, como
`.venv/`, `venv/`, `__pycache__/`, `.env` o `db.sqlite3`. No añadas esos archivos a
Git ni guardes temporales en el repositorio. El ZIP se crea en el directorio
superior para no incorporarlo al proyecto.

Puedes verificar su contenido con Python, sin instalar herramientas adicionales:

```bash
python -m zipfile -l ../Martret_Jaime_MF0227.zip
python -m zipfile -t ../Martret_Jaime_MF0227.zip
```

Antes de la fusión se puede generar un ZIP de revisión desde esta rama con el
mismo comando `git archive`, usando `HEAD`. La entrega definitiva debe generarse
desde el `main` que ya incluya la Fase 3. El ZIP no debe añadirse a GitHub.
