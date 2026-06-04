**Instalación y ejecución del proyecto**

**Requisitos**
Antes de ejecutar el sistema, asegúrese de tener instalado:
- PostgreSQL
- DBeaver (o cualquier cliente compatible con PostgreSQL)
- Python 3.x
- Librerías requeridas del proyecto (pip install psycopg2)

**Configuración de la base de datos**
1. Abrir DBeaver y crear una nueva conexión a PostgreSQL.
2. Crear una base de datos vacía para el proyecto, por ejemplo:

CREATE DATABASE libreria;

3. Ejecutar el archivo:
create-db.sql

Este script crea todas las tablas, tipos ENUM, restricciones y relaciones necesarias para el sistema.

4. Una vez finalizada la creación de la estructura, ejecutar:
insert-db.sql

Este script inserta los datos iniciales utilizados por el sistema.

**Configuración del proyecto**
1. Abrir la carpeta:
libreria/
2. Verificar que el archivo de conexión a la base de datos (database.py) contenga los datos correctos de la conexión PostgreSQL:

host="localhost"
database="libreria"
user="postgres"
password="su_contraseña"
Instalar las dependencias necesarias:
pip install psycopg2
Ejecución del sistema

3. Ubicarse dentro de la carpeta del proyecto:

cd libreria

4. Ejecutar el archivo principal:

python main.py

Al ejecutar main.py se abrirá la ventana principal del Sistema de Gestión de Librería, desde donde se puede acceder a los módulos de Inventario, Ventas, Clientes, Personal y Reportes.
