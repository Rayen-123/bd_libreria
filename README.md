**Instalación y ejecución del proyecto**

**Requisitos**
Antes de ejecutar el sistema, asegúrese de tener instalado:
- PostgreSQL
- DBeaver (o cualquier cliente compatible con PostgreSQL)
- Python 3.x
- Librerías requeridas del proyecto (pip install psycopg2)

**Configuración de la base de datos transaccional**
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
libreria_interfaz/
2. Verificar que el archivo de conexión a la base de datos (database.py) contenga los datos correctos de la conexión PostgreSQL:

host="localhost"
database="libreria"
user="postgres"
password="su_contraseña"
Instalar las dependencias necesarias:
pip install psycopg2
Ejecución del sistema

3. Ubicarse dentro de la carpeta del proyecto:

cd libreria_interfaz

4. Ejecutar el archivo principal:

python main.py

Al ejecutar main.py se abrirá la ventana principal del Sistema de Gestión de Librería, desde donde se puede acceder a los módulos de Inventario, Ventas, Clientes, Personal y Reportes.

**configuracion base de datos analitica**
previamente cargada base de datos transaccional 
1. Abrir DBeaver y crear una nueva conexión a PostgreSQL.
2. Crear una base de datos vacía para el proyecto, por ejemplo:

CREATE DATABASE analisis_libreria;

3. Ejecutar el archivo:
analisis.sql

Este script crea todas las tablas, tipos ENUM, restricciones y relaciones necesarias para el sistema.

<b>Cargar datos de transaccional a analitica<b>

1. Abrir carpeta:
Analisis/

2. Verificar que el archivo de etl_libreria tenga los datos correctos de la conexion PostgreSQL:

DB_TRANSACCIONAL = {
    "host": "localhost",
    "port": 5432,
    "database": "libreria",      
    "user": "postgres",
    "password": "tu contraseña"      
}

DB_ANALISIS = {
    "host": "localhost",
    "port": 5432,
    "database": "analisis_libreria", 
    "user": "postgres",
    "password": "tu_contraseña"la ventana principal del Sistema de Gestión de Librería, desde donde se puede acceder a los módulos de Inventario, Ventas, Clientes, Personal y Reportes.
}

Instalar las dependencias necesarias:
pip install psycopg2 schedule

<b>Ejecución del sistema<b>

3. Ubicarse dentro de la carpeta
cd Analisis

4. Ejecutar
python extraccion_datos.py

Al ejecutar extraccion_datos.py se estara cargando todos los datos de la base de datos transaccional a la analitica todos los dias a las 3:00 am que es cuando no existe uso de los datos 

**Ver Graficos**
previamente cargada toda la informacion a base de datos analitica

1. Abrir carpeta:
Analisis/

2. Verifica que el archivo graficos.py tenga los datos correctos de la conexion PostgreSQL:

cadena_conexion = 'postgresql+psycopg2://postgres:<b>tu_contraseña<b>@localhost:5432/analisis_libreria'

Instalar las dependencias necesarias:
pip install pandas matplotlib sqlalchemy

<b>Ejecución del sistema<b>

3. Ubicarse dentro de la carpeta
cd Analisis

4. Ejecutar
python graficos.py

Al ejecutar graficos.py ejecutara uno a uno los graficos de analisis de los datos
