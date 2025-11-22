# PGPI-G1.7
Proyecto grupal para PGPI curso 2025/2026.

## Mockups
Puede encontrarlos [aquí](https://marvelapp.com/prototype/agedh8d)

## Para ejecutar el proyecto:
### Base de Datos (PostgreSQL)

1. **Instalar PostgreSQL**
   - Descargar e instalar desde: [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)  
   - Durante la instalación:
     - Mantener el puerto por defecto (`5432`).

2. **Abrir SQL Shell (psql) o pgAdmin**

3. **Crear base de datos `charmaway`**  
   ```bash
   psql -U postgres
   CREATE DATABASE charmaway;
   CREATE USER charmaway_user WITH PASSWORD 'charmaway_password';
   GRANT ALL PRIVILEGES ON DATABASE charmaway TO charmaway_user;
   ALTER USER charmaway_user CREATEDB;
   \c charmaway
   GRANT ALL PRIVILEGES ON SCHEMA public TO charmaway_user;
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO charmaway_user;
   \q
   ```
     
### Proyecto
1. Crear y acceder a un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate (Linux/MacOS)
   venv\Scripts\activate (Windows)
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Acceder a la carpeta del proyecto:
   ```bash
   cd charmaway/
   ```
4. Aplicar migraciones:
   ```bash
   python manage.py migrate
   ```
5. Aplicar seeders (datos):
   ```bash
   python seed_all.py
   ```
5. Ejecutar la aplicación:
   ```bash
   python manage.py runserver
   ```
6. Ejecutar las pruebas
   - Para ejecutar todos los tests del proyecto (todas las aplicaciones):
   ```bash
   python manage.py test
   ```
   - Para ejecutar los tests de una aplicación específica (por ejemplo, `administrator`):
   ```bash
   python manage.py test administrator
   ```