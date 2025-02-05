import os
import subprocess
import sys
import mysql.connector
import re
from pathlib import Path
from dotenv import set_key, load_dotenv

def install_package(package, version="latest"):
    """Verifica si el paquete está instalado, muestra la versión y lo instala si no está."""
    try:
        installed_version = subprocess.check_output([sys.executable, "-m", "pip", "show", package], text=True)
        if installed_version:
            print(f"{package} ya está instalado.")
            return
    except subprocess.CalledProcessError:
        pass
    
    print(f"Instalando {package}...")
    pip_cmd = [sys.executable, "-m", "pip", "install", f"{package}=={version}"] if version != "latest" else [sys.executable, "-m", "pip", "install", package]
    subprocess.run(pip_cmd, check=True)

def install_dependencies():
    """Instala las dependencias necesarias si no están instaladas."""
    dependencies = {
        "python-dotenv": "0.18.0",
        "mysql-connector-python": "8.0.25",
        "pyrate-limiter": "2.8.1",
        "argon2-cffi": "21.3.0"
    }
    for package, version in dependencies.items():
        install_package(package, version)
    install_package("requests")
    print("Dependencias instaladas correctamente.")

def get_user_input(prompt, default=None):
    """Solicita entrada al usuario con opción de valor por defecto."""
    while True:
        value = input(f'{prompt} [{default}]: ') if default else input(f'{prompt}: ')
        if value.strip():
            return value.strip()
        elif default is not None:
            return default
        print("El valor no puede estar vacío. Inténtalo de nuevo.")

def validate_mysql_dbname(dbname):
    """Valida el nombre de la base de datos para MySQL."""
    if not re.match(r'^[a-zA-Z0-9_]+$', dbname):
        print("Error: El nombre de la base de datos contiene caracteres no permitidos. Solo se permiten letras, números y guiones bajos (_).")
        return False
    return True

def confirm_data(data):
    """Muestra los datos al usuario y solicita confirmación."""
    print("\nVerifique los datos ingresados:")
    for key, value in data.items():
        print(f"{key}: {value}")
    return input("¿Los datos son correctos? (S/N): ").strip().lower() == 's'

def verify_mysql_connection(mysql_data):
    """Verifica si la conexión a MySQL es correcta."""
    try:
        connection = mysql.connector.connect(
            host=mysql_data["MYSQL_HOST"],
            user=mysql_data["MYSQL_USER"],
            password=mysql_data["MYSQL_PASS"],
            port=mysql_data["MYSQL_PORT"]
        )
        connection.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error de conexión a MySQL: {err}")
        return False

def create_database_if_not_exists(mysql_data):
    """Crea la base de datos si no existe."""
    try:
        connection = mysql.connector.connect(
            host=mysql_data["MYSQL_HOST"],
            user=mysql_data["MYSQL_USER"],
            password=mysql_data["MYSQL_PASS"],
            port=mysql_data["MYSQL_PORT"]
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{mysql_data['MYSQL_DATABASE']}`")
        cursor.close()
        connection.close()
        print("Base de datos verificada o creada.")
    except mysql.connector.Error as err:
        print(f"Error al verificar/crear la base de datos: {err}")

def import_sql_file(file_path, mysql_data):
    """Importa un archivo SQL en la base de datos."""
    try:
        command = (
            f"mysql -h {mysql_data['MYSQL_HOST']} -u {mysql_data['MYSQL_USER']} "
            f"-p{mysql_data['MYSQL_PASS']} -P {mysql_data['MYSQL_PORT']} "
            f"{mysql_data['MYSQL_DATABASE']} < {file_path}"
        )
        subprocess.run(command, shell=True, check=True)
        print(f"Archivo {file_path} importado correctamente.")
    except subprocess.CalledProcessError as err:
        print(f"Error al importar {file_path}: {err}")

def create_env_file():
    """Crea o actualiza el archivo .env con los valores de MySQL."""
    env_path = Path('.') / '.env'
    env_path.touch(exist_ok=True)
    load_dotenv(dotenv_path=env_path)
    
    while True:
        mysql_data = {
            "MYSQL_HOST": get_user_input("Ingrese el host de MySQL", os.getenv("MYSQL_HOST", "localhost")),
            "MYSQL_USER": get_user_input("Ingrese el usuario de MySQL", os.getenv("MYSQL_USER", "root")),
            "MYSQL_PASS": get_user_input("Ingrese la contraseña de MySQL", os.getenv("MYSQL_PASS", "")),
            "MYSQL_DATABASE": get_user_input("Ingrese el nombre de la base de datos", os.getenv("MYSQL_DATABASE", "tbot_local")),
            "MYSQL_PORT": get_user_input("Ingrese el puerto de MySQL", os.getenv("MYSQL_PORT", "3306"))
        }
        
        if not validate_mysql_dbname(mysql_data["MYSQL_DATABASE"]):
            print("Por favor, ingrese un nombre de base de datos válido.")
            continue
        
        if confirm_data(mysql_data) and verify_mysql_connection(mysql_data):
            break
        print("Datos incorrectos, intente nuevamente.")
    
    with env_path.open("w") as env_file:
        for key, value in mysql_data.items():
            env_file.write(f"{key}={value}\n")
    
    print("Archivo .env creado correctamente.")
    create_database_if_not_exists(mysql_data)
    import_sql_file("Migrations/tbot-base.sql", mysql_data)

if __name__ == "__main__":
    install_dependencies()
    create_env_file()
