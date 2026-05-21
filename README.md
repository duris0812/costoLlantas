# Proveedor de Llantas

Esta aplicación Django calcula la asignación óptima de proveedores para distintos tipos de llanta usando A* y permite editar la matriz de costos desde la interfaz.

## Requisitos
- Python 3.8+
- pip

## Comandos locales rápidos
Instala dependencias:

```bash
python -m pip install -r requirements.txt
```

Ejecuta migraciones y servidor:

```bash
python manage.py migrate
python manage.py runserver
```

Para probar el cálculo manualmente usa la interfaz en `http://127.0.0.1:8000/`.

## Desplegar en Render
Ya incluí `render.yaml` y `Procfile` para facilitar el deploy.

Pasos resumidos:

1. Sube este directorio (`Proveedor_llantas`) a un repositorio Git (GitHub/GitLab). Si quieres, usa los comandos:

```bash
cd Proveedor_llantas
git init
git add .
git commit -m "App Proveedor de Llantas para deploy"
# crea el repo en GitHub y añade remote
git remote add origin <URL_DE_TU_REPO>
git push -u origin main
```

2. En Render crea un nuevo Web Service apuntando al repo. Puedes dejar `root directory` en `Proveedor_llantas` si subes en un repo monorepo.

3. Render detectará `render.yaml` y ejecutará los pasos:
   - `pip install -r requirements.txt`
   - `python manage.py migrate`
   - `python manage.py collectstatic --no-input`
   - `gunicorn llantas_project.wsgi:application`

4. Añade las variables de entorno en el panel de Render (si no usas `render.yaml`):
   - `SECRET_KEY` (generada)
   - `DEBUG=false`

Notas:
- `render.yaml` ya configura `buildCommand` y `startCommand` para un deploy automático.
- El proyecto usa `whitenoise` para servir estáticos en producción.

Si quieres, puedo inicializar el repo Git en tu máquina y hacer el primer push (necesitaré que me proporciones la URL remota).