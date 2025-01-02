# Sistema de inventario para la reposición de productos

Agroselva es una pequeña empresa dedicada a la venta de productos agrícolas. Con el tiempo, se identificó que los procesos manuales de gestión provocaban desabastecimientos frecuentes de productos, afectando la eficiencia operativa. Para resolver este problema, se desarrolló esta aplicación, diseñada para digitalizar los procesos y simplificar la reposición de inventario, haciendo que sea más fácil de utilizar.

---

## Imagenes del proyecto

Repositorio del frontend https://github.com/miguelmallquidiaz/agroselva-react 

### Login

![login](https://i.imgur.com/bhGSCLY.png)

### Panel de administrador

![admin almacen](https://i.imgur.com/sAyYrUE.png)

### Panel para el empleado

![empleado](https://i.imgur.com/4MpTwcI.png)

### Registrar pedido para rebastecer el local

![pedido](https://i.imgur.com/4MpTwcI.png)

### Verificar que contiene el pedido para rebastecer

![verificación](https://i.imgur.com/aLQ7OX7.png)

---

## Tecnologías utilizadas

- React y Tailwind CSS para el frontend.
- Python con FastAPI y PostgreSQL para el backend.

## 🚀 **Instalación local**

Sigue estos pasos para instalar y ejecutar la aplicación en tu entorno local:

### 1. Crear un entorno virtual
```bash
python -m venv venv
```

### 2. Activar el entorno virtual
- En Windows:
```bash
./venv/Scripts/activate
```

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos PostgreSQL
- Crea una base de datos en PostgreSQL utilizando [Render](https://render.com) u otro proveedor de servicios.
- Obtén la URL externa de la base de datos.

### 5. Crear el archivo `.env`
Crea un archivo `.env` en la raíz del proyecto (fuera de la carpeta `app`) con las siguientes variables de entorno:
```env
DATABASE_URL=poner la url externar o utilizar el de local postgresql://postgres:admin@localhost/agroselvadb
FRONTEND_URL=URL_de_la_página_web
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e3238d3e721212121
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=40
ADMIN_EMAIL=correo
ADMIN_PASSWORD=contraseña
PYTHON_VERSION=3.12.5
```

### 6. Ejecutar la aplicación
```bash
uvicorn app.main:app --reload
```

### 7. Ingresar a la documentación de los endpoint en local
```bash
http://localhost:8000/docs
```

## Se muestran todos los endpoint en la documentación

![api](https://i.imgur.com/GNOmymk.png)
