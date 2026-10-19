# MF0227_3 · Fase 0

Proyecto inicial para gestionar productos de una tienda con Python y Django.
El proyecto se llama `tienda` y su única aplicación propia es `catalogo`.
Esta fase contiene la estructura estándar de Django, sin modelos de productos,
formularios ni vistas de las fases posteriores.

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

El servidor debe mostrar la página de bienvenida de Django en su dirección local
habitual, puerto 8000. Detén el servidor con `Ctrl+C` y sal del entorno virtual
con `deactivate`.

Todavía no hay pruebas funcionales propias: `catalogo/tests.py` conserva el archivo
estándar generado por Django. La comprobación de esta fase consiste en validar la
configuración, aplicar las migraciones y comprobar la bienvenida del servidor.

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
    views.py
    tests.py
    migrations/
        __init__.py
requirements.txt
.gitignore
README.md
```

La configuración generada (`DEBUG=True` y clave de desarrollo) está destinada al
desarrollo local; antes de desplegar se requiere una configuración de producción.
