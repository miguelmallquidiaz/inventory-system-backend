from .crud import employee_crud
from .schemas import employee_schema
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
        first_name = os.getenv("FIRST_NAME", "miguel")
        last_name = os.getenv("LAST_NAME", "mallqui")

        # Verificamos si el usuario admin ya existe
        employee = employee_crud.get_employee_by_email(db, email=admin_email)
        if not employee:
            # Si no existe, verificamos si hay un usuario con el rol admin
            admin_exists = employee_crud.get_employee_by_role(db, role="almacen")
            if not admin_exists:
                # Si no existe ningún admin, creamos el usuario admin
                admin_user = employee_schema.EmployeeCreate(
                    first_name=first_name,
                    last_name=last_name,
                    email=admin_email,
                    password=admin_password,
                    role="almacen"
                )
                employee_crud.create_employee(db=db, employee=admin_user)
                print("Usuario creado.")
            else:
                print("Ya existe un usuario con este rol.")
        else:
            print("El usuario ya existe.")
    except Exception as e:
        print(f"Error al crear el usuario: {e}")
    finally:
        # Aseguramos cerrar la sesión
        db.close()

# Si ejecutas este archivo directamente, creará el usuario admin
if __name__ == "__main__":
    create_admin_user()
