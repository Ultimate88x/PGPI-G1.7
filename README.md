# PGPI-G1.7
Proyecto grupal para PGPI curso 2025/2026.

## Para ejecutar el proyecto:
### Base de Datos:
  - Instalar MariaDB.
  - Crear usuario:
       username = root, password = root
  - Crear base de datos 'charmaway'.
  - Crear y dar permisos (excepto GRANT y LOCK TABLES) sobre la base de datos 'charmaway' a un usuario:
      username = charmaway_user, password = charmaway_user
### Proyecto
1. Crear y acceder a un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate        # En Linux / macOS
   venv\Scripts\activate           # En Windows
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
5. Ejecutar la aplicación:
   ```bash
   python manage.py runserver
   ```
