from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from .database import engine
from . import models, auth
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routers import user, auth, category, client, subcategory, product, reservation
from .initial_data import create_admin_user
import uvicorn
# Cargar variables de entorno
load_dotenv()

# Definir URLs de frontend y versiones de la API
FRONTEND_URL = os.environ.get("FRONTEND_URL")
VERSION = "/api/v1"

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Definir el async context manager para el ciclo de vida
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando la aplicación y creando usuario admin si es necesario...")
    create_admin_user()  # Crear usuario admin al inicio

    yield  # Esperar hasta que la aplicación se detenga

    # Limpieza después de que la aplicación finalice
    print("Limpieza al terminar la aplicación...")

# Inicializar la aplicación con el ciclo de vida
app = FastAPI(title="Agroselva", description="Agroselva API", lifespan=lifespan)

# Configuración de CORS
origins = [
    "http://localhost:5173",
    FRONTEND_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta raíz para probar la API
@app.get("/")
async def root():
    return {"message": "Inicializando la API de Agroselva"}

# Incluir las rutas
app.include_router(auth.router, prefix=f"{VERSION}/auth", tags=["auth"])
app.include_router(user.router, prefix=f"{VERSION}/user", tags=["user"])
app.include_router(category.router, prefix=f"{VERSION}/category", tags=["category"])
app.include_router(client.router, prefix=f"{VERSION}/client", tags=["client"])
app.include_router(subcategory.router, prefix=f"{VERSION}/subcategory", tags=["subcategory"])
app.include_router(product.router, prefix=f"{VERSION}/product", tags=["product"])
app.include_router(reservation.router, prefix=f"{VERSION}/reservation", tags=["reservation"])

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Usa el puerto de la variable de entorno PORT
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)