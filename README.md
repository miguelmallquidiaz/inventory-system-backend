# Agroselva FastAPI Backend

Sistema de inventario desarrollado con FastAPI para gestionar el stock de productos y el control de acceso en Agroselva.

## Instalar localmente

```bash
1. Crear el entorno seguro
python -m venv venv

2. Ingresar en el entorno seguro
./venv/Scripts/activate

3. Instalar los paquetes de requirements.txt
pip install -r requirements.txt 

4. Crear la base de datos PostgreSQL en Render y obtener el External Database URL
```

Crear el archivo .env fuera de la carpeta app

```bash
DATABASE_URL=External Database URL ejemplo de manera local postgresql://postgres:admin@localhost/agroselvadb
FRONTEND_URL=página web
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e3238d3e721212121
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=40
ADMIN_EMAIL=correo
ADMIN_PASSWORD=contraseña
PYTHON_VERSION=3.12.5
```

Ejecutar la aplicación

```bash
uvicorn app.main:app --reload
```

## Deploy en Render

```bash
1. Ingresar a Web Services.
2. En Git Provider selecionar el repositorio del proyecto y darle a conectar.
3. Seleccionar el lenguaje Python3.
4. Seleccionar el branch
5. Start Command: uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
6. Instance Type: Free
7. Environment Variables: Copiar las variables de entorno
8. Deploy
```
