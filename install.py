import os
import sys
import subprocess
import re
from pathlib import Path

# Ensure dependencies are installed before importing
def ensure_package_installed(package, version="latest"):
    """Check if a package is installed and install it if not."""
    try:
        subprocess.run([sys.executable, "-m", "pip", "show", package], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print(f"Installing {package}...")
        install_cmd = [sys.executable, "-m", "pip", "install", f"{package}=={version}" if version != "latest" else package]
        subprocess.run(install_cmd, check=True, stdout=subprocess.DEVNULL)
        print(f"{package} installed successfully.")

# Install dotenv before importing it
ensure_package_installed("python-dotenv", "latest")

# Now we can import dotenv
from dotenv import load_dotenv
import mysql.connector
import argparse

# Dependencies dictionary
DEPENDENCIES = {
    "python-dotenv": "0.18.0",
    "mysql-connector-python": "8.0.25",
    "pyrate-limiter": "2.8.1",
    "argon2-cffi": "21.3.0",
    "requests": "latest"
}

def install_dependencies():
    """Install required dependencies."""
    for package, version in DEPENDENCIES.items():
        ensure_package_installed(package, version)
    print(" All dependencies were installed successfully.")

def get_user_input(prompt, default=None):
    """Request input from the user with an optional default value."""
    while True:
        value = input(f'{prompt} [{default}]: ') if default else input(f'{prompt}: ')
        if value.strip():
            return value.strip()
        elif default is not None:
            return default
        print("Value cannot be empty. Please try again.")

def validate_mysql_dbname(dbname):
    """Validate database name."""
    return bool(re.match(r'^[a-zA-Z0-9_]+$', dbname))

def confirm_data(data):
    """Show entered data and request confirmation."""
    print("\n Please verify the entered data:")
    for key, value in data.items():
        print(f"{key}: {value}")
    return input("Is the data correct? (Y/N): ").strip().lower() == 'y'

def verify_mysql_connection(mysql_data):
    """Check if MySQL connection is valid."""
    try:
        connection = mysql.connector.connect(
            host=mysql_data["MYSQL_HOST"],
            user=mysql_data["MYSQL_USER"],
            password=mysql_data["MYSQL_PASS"],
            port=mysql_data["MYSQL_PORT"]
        )
        connection.close()
        print("MySQL connection verified successfully.")
        return True
    except mysql.connector.Error as err:
        print(f"MySQL connection error: {err}")
        return False

def create_database_if_not_exists(mysql_data):
    """Create the database if it does not exist."""
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
        print(f"Database '{mysql_data['MYSQL_DATABASE']}' verified or created.")
    except mysql.connector.Error as err:
        print(f" Error creating database: {err}")
        sys.exit(1)

def create_env_file():
    """Create or update the .env file with MySQL values."""
    env_path = Path('.') / '.env'
    env_path.touch(exist_ok=True)
    load_dotenv(dotenv_path=env_path)
    
    while True:
        mysql_data = {
            "MYSQL_HOST": get_user_input("Enter MySQL host", os.getenv("MYSQL_HOST", "localhost")),
            "MYSQL_USER": get_user_input("Enter MySQL user", os.getenv("MYSQL_USER", "root")),
            "MYSQL_PASS": get_user_input("Enter MySQL password", os.getenv("MYSQL_PASS", "")),
            "MYSQL_DATABASE": get_user_input("Enter database name", os.getenv("MYSQL_DATABASE", "tbot_local")),
            "MYSQL_PORT": get_user_input("Enter MySQL port", os.getenv("MYSQL_PORT", "3306"))
        }
        
        if not validate_mysql_dbname(mysql_data["MYSQL_DATABASE"]):
            print("Invalid database name. Only letters, numbers, and underscores (_) are allowed.")
            continue
        
        if confirm_data(mysql_data) and verify_mysql_connection(mysql_data):
            break
        print("Invalid data, please try again.")
    
    with env_path.open("w") as env_file:
        for key, value in mysql_data.items():
            env_file.write(f"{key}={value}\n")
    
    print(".env file created successfully.")
    create_database_if_not_exists(mysql_data)

def main():
    """Main function of the script."""
    parser = argparse.ArgumentParser(description="🔧 Initial project setup.")
    parser.add_argument("--install-deps", action="store_true", help="Install required dependencies.")
    parser.add_argument("--create-env", action="store_true", help="Create the .env file and configure the database.")
    args = parser.parse_args()

    if args.install_deps:
        install_dependencies()
    if args.create_env:
        create_env_file()

    if not args.install_deps and not args.create_env:
        install_dependencies()
        create_env_file()

if __name__ == "__main__":
    main()
