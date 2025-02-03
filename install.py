import os
import subprocess
import sys

# Verificar si `dotenv` está instalado, si no, instalarlo
try:
    from dotenv import set_key, load_dotenv
except ModuleNotFoundError:
    print("`python-dotenv` no está instalado. Instalándolo ahora...")
    subprocess.run([sys.executable, "-m", "pip", "install", "python-dotenv", "--quiet"], check=True)
    from dotenv import set_key, load_dotenv  # Intentar importar nuevamente

from pathlib import Path

# Definir el archivo .env en la carpeta raíz
env_path = Path('.') / '.env'

def get_user_input(prompt, default=None):
    while True:
        value = input(f'{prompt} [{default}]: ') if default else input(f'{prompt}: ')
        if value.strip():
            return value.strip()
        elif default is not None:
            return default
        print("El valor no puede estar vacío. Inténtalo de nuevo.")

def confirm_data(data):
    print("\nVerifique los datos ingresados:")
    for key, value in data.items():
        print(f"{key}: {value}")
    return input("¿Los datos son correctos? (S/N): ").strip().lower() == 's'

def create_env_file():
    """Crea un archivo .env y solicita los valores al usuario, permitiendo corrección."""
    if env_path.exists():
        print("El archivo .env ya existe. Se actualizarán los valores.")
    
    # Crear o cargar el .env
    env_path.touch(exist_ok=True)
    load_dotenv(dotenv_path=env_path)
    
    while True:
        mysql_data = {
            "MYSQL_HOST": get_user_input("Ingrese el host de MySQL", os.getenv("MYSQL_HOST")),
            "MYSQL_USER": get_user_input("Ingrese el usuario de MySQL", os.getenv("MYSQL_USER")),
            "MYSQL_PASS": get_user_input("Ingrese la contraseña de MySQL", os.getenv("MYSQL_PASS")),
            "MYSQL_DATABASE": get_user_input("Ingrese el nombre de la base de datos", os.getenv("MYSQL_DATABASE")),
            "MYSQL_PORT": get_user_input("Ingrese el puerto de MySQL", os.getenv("MYSQL_PORT"))
        }
        
        if confirm_data(mysql_data):
            break
        print("Volvamos a ingresar los datos...")
    
    # Guardar datos en el .env sin comillas
    with env_path.open("w") as env_file:
        for key, value in mysql_data.items():
            env_file.write(f"{key}={value}\n")
    
    print("Archivo .env creado correctamente.")

def install_dependencies():
    """Instala las dependencias necesarias si aún no están instaladas."""
    dependencies = {
        "mysql-connector-python": "8.0.25",
        "pyrate-limiter": "2.8.1",
        "argon2-cffi": "21.3.0",
        "requests": "latest"
    }
    
    for package, version in dependencies.items():
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            print(f"Instalando {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", f"{package}=={version}", "--quiet"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print("Dependencias instaladas correctamente.")

if __name__ == "__main__":
    create_env_file()
    install_dependencies()
