import os
import sys
import subprocess
import re
import shutil
from pathlib import Path

# Dependencias necesarias
DEPENDENCIES = {
    "python-dotenv": "latest",
    "mysql-connector-python": "latest",
    "pyrate-limiter": "latest",
    "argon2-cffi": "latest",
    "requests": "latest"
}

def ensure_package_installed(package, version="latest"):
    """Verifica si el paquete está instalado y lo instala si no está."""
    try:
        subprocess.run([sys.executable, "-m", "pip", "show", package], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print(f"📦 Instalando {package}...")
        install_cmd = [sys.executable, "-m", "pip", "install", f"{package}=={version}" if version != "latest" else package]
        subprocess.run(install_cmd, check=True, stdout=subprocess.DEVNULL)
        print(f"✅ {package} instalado correctamente.")

# Instalar dependencias antes de importar
for package, version in DEPENDENCIES.items():
    ensure_package_installed(package, version)

# Importar librerías después de la instalación
from dotenv import load_dotenv
import mysql.connector

def ensure_mysql_in_path():
    """Verifica si MySQL está en el PATH. Si no, intenta agregarlo automáticamente."""
    mysql_executable = shutil.which("mysql")

    if mysql_executable:
        return mysql_executable  # MySQL ya está disponible en el sistema

    # Ruta por defecto en Windows
    mysql_default_path = r"C:\Program Files\MySQL\MySQL Server 8.0\bin"

    if os.path.exists(mysql_default_path):
        print(f"⚠️ MySQL no está en el PATH. Agregándolo temporalmente desde: {mysql_default_path}")
        os.environ["PATH"] += os.pathsep + mysql_default_path
        mysql_executable = os.path.join(mysql_default_path, "mysql.exe")
        return mysql_executable

    print(f"❌ No se encontró MySQL en '{mysql_default_path}'. Asegúrate de que MySQL esté instalado correctamente.")
    sys.exit(1)

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
    """Valida el nombre de la base de datos."""
    return bool(re.match(r'^[a-zA-Z0-9_]+$', dbname))

def confirm_data(data):
    """Muestra los datos y solicita confirmación."""
    print("\n📋 Verifique los datos ingresados:")
    for key, value in data.items():
        print(f"{key}: {value}")
    return input("¿Los datos son correctos? (S/N): ").strip().lower() == 's'

def verify_mysql_connection(mysql_data):
    """Verifica si la conexión a MySQL es válida."""
    try:
        connection = mysql.connector.connect(
            host=mysql_data["MYSQL_HOST"],
            user=mysql_data["MYSQL_USER"],
            password=mysql_data["MYSQL_PASS"],
            port=mysql_data["MYSQL_PORT"]
        )
        connection.close()
        print("✅ Conexión a MySQL verificada correctamente.")
        return True
    except mysql.connector.Error as err:
        print(f"❌ Error de conexión a MySQL: {err}")
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
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]

        if mysql_data['MYSQL_DATABASE'] not in databases:
            cursor.execute(f"CREATE DATABASE `{mysql_data['MYSQL_DATABASE']}`")
            print(f"✅ Base de datos '{mysql_data['MYSQL_DATABASE']}' creada.")
        else:
            print(f"✅ La base de datos '{mysql_data['MYSQL_DATABASE']}' ya existe.")
        
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"❌ Error al crear/verificar la base de datos: {err}")
        sys.exit(1)

def import_sql_file(file_path, mysql_data):
    """Importa un archivo SQL en la base de datos."""
    if not Path(file_path).exists():
        print(f"❌ Error: El archivo {file_path} no existe.")
        sys.exit(1)

    mysql_executable = ensure_mysql_in_path()

    try:
        command = (
            f'"{mysql_executable}" -h {mysql_data["MYSQL_HOST"]} -u {mysql_data["MYSQL_USER"]} '
            f'-p{mysql_data["MYSQL_PASS"]} -P {mysql_data["MYSQL_PORT"]} '
            f'{mysql_data["MYSQL_DATABASE"]} < "{file_path}"'
        )
        subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL)
        print(f"✅ Archivo {file_path} importado correctamente.")
    except subprocess.CalledProcessError as err:
        print(f"❌ Error al importar {file_path}: {err}")
        sys.exit(1)

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
            print("⚠️ Nombre de base de datos inválido. Solo se permiten letras, números y guiones bajos (_).")
            continue
        
        if confirm_data(mysql_data) and verify_mysql_connection(mysql_data):
            break
        print("🔄 Datos incorrectos, intente nuevamente.")
    
    with env_path.open("w") as env_file:
        for key, value in mysql_data.items():
            env_file.write(f"{key}={value}\n")
    
    print("✅ Archivo .env creado correctamente.")
    create_database_if_not_exists(mysql_data)
    import_sql_file("Migrations/tbot-base.sql", mysql_data)

def main():
    create_env_file()

if __name__ == "__main__":
    main()
