# PGPI-G1.7
Proyecto grupal para PGPI curso 2025/2026.

## Mockups
Puede encontrarlos [aquí](https://marvelapp.com/prototype/agedh8d)
## Para ejecutar el proyecto:
### Base de Datos:
  1. Instalar MariaDB.
  2. Crear usuario root:
       username = root, password = root
  3. Incluir ...\MariaDB 12.0\bin en el path.
  4. Ejecutar MariaDB desde cmd o powershell.
  ```bash
   mysql -u root -p
   ```
  5. Crear base de datos 'charmaway'.
  ```bash
   mysql -u root -p
   ```
  6. Crear usuario: username = charmaway_user, password = charmaway_user
  ```bash
  CREATE USER 'charmaway_user'@'localhost' IDENTIFIED BY 'charmaway_user';
   ```
  7. Dar permisos (excepto GRANT y LOCK TABLES) sobre la base de datos 'charmaway' al usuario:
  ```bash
  GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER, CREATE TEMPORARY TABLES, REFERENCES, EXECUTE, SHOW VIEW, CREATE VIEW, EVENT, TRIGGER ON charmaway.* TO 'charmaway_user'@'localhost';
  FLUSH PRIVILEGES;
  ```
     
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
