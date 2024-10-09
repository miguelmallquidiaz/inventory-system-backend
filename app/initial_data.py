from sqlalchemy.orm import Session
from .crud import user_crud
from .schemas import users_schema
from .database import SessionLocal
from passlib.context import CryptContext
import os

# Contexto para gestionar contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin_user():
    db = SessionLocal()  # Abrimos la sesión de base de datos
    try:
        admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
        admin_password = os.getenv("ADMIN_PASSWORD", "admin_password")

        # Verificamos si el usuario admin ya existe
        user = user_crud.get_user_by_email(db, email=admin_email)
        if not user:
            # Si no existe, verificamos si hay un usuario con el rol admin
            admin_exists = user_crud.get_user_by_role(db, role="admin")
            if not admin_exists:
                # Si no existe ningún admin, creamos el usuario admin
                admin_user = users_schema.UserCreate(
                    email=admin_email,
                    password=admin_password,  # Encriptamos la contraseña
                    name="miguel",
                    first_surname="mallqui",
                    second_last_name="diaz",
                    phone="944741052",
                    role="admin"
                )
                user_crud.create_user(db=db, user=admin_user)
                print("Usuario admin creado.")
            else:
                print("Ya existe un usuario con rol de admin.")
        else:
            print("El usuario admin ya existe.")
    except Exception as e:
        print(f"Error al crear el usuario admin: {e}")
    finally:
        # Aseguramos cerrar la sesión
        db.close()

# Si ejecutas este archivo directamente, creará el usuario admin
if __name__ == "__main__":
    create_admin_user()
