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
  5. Crear base de datos 'charmaway' y 'charmaway_test'.
  ```bash
  CREATE DATABASE charmaway;
  CREATE DATABASE charmaway_test;
   ```
  6. Crear usuario: username = charmaway_user, password = charmaway_user
  ```bash
  CREATE USER 'charmaway_user'@'localhost' IDENTIFIED BY 'charmaway_user';
   ```
  7. Dar permisos (excepto GRANT y LOCK TABLES) sobre las bases de datos 'charmaway' y 'charmaway_test' al usuario:
  ```bash
  GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER, CREATE TEMPORARY TABLES, REFERENCES, EXECUTE, SHOW VIEW, CREATE VIEW, EVENT, TRIGGER ON charmaway.* TO 'charmaway_user'@'localhost';
  GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER, CREATE TEMPORARY TABLES, REFERENCES, EXECUTE, SHOW VIEW, CREATE VIEW, EVENT, TRIGGER ON charmaway_test.* TO 'charmaway_user'@'localhost';
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
5. Aplicar seeders (datos):
   ```bash
   python seed_all.py
   ```
5. Ejecutar la aplicación:
   ```bash
   python manage.py runserver
   ```

### Stripe:   
1. Para que stripe funcione y procese los pagos es necesario tener una cuenta de stripe.
2. Después es importante acceder a nuestro dashboard de stripe para obtener tanto nuestor publishable token como nuestro private/secret token.
3. Usa el .env.example como .env.
   ```bash
   mv .env.example .env
   ```
5. Sustituye los campos requeridos con tus tokens.
6. Para obtener wl webhook token, debes instalar el cli de stripe.
7. Una vez descargado y puesto en nuestro path, debemos ejecutar en una pantalla cmd.
   ```bash
   stripe listen --forward-to localhost:<PUERTO>/webhook
   ```
   Siendo PUERTO el puerto donde esté escuchando nuestra aplicación, en nuestro caso por defecto es el 8000.
8. Se mostrará este mensaje o uno similar:
  Ready! Your webhook signing secret is whsec_ABC123...
  whsec_ABC123... será el token que debe sustituirse en el .env.
9.Nuestro servicio estará escuchando y podrá probarse con una tarjeta de prueba:
  Tarjeta de prueba -> 4242 4242 4242 4242 11/44 111
10. Podremos ver las llamadas que nos llegan al webhiik desde el cmd donde ejecutamos nuestro comando.
11. En nuestro dashboard de Stripe aparecerán también dichos movimientos.
12. 
### Tests:
1. Para que django los detecte, los tests de cada módulo tienen que estar en un archivo llamado explícitamente 'tests.py' dentro de cada uno de los módulos correspondientes.
2. Para ejecutar los tests:
   ```bash
   pytest
   ```
