import psycopg2
from psycopg2.extras import execute_values

# ==========================================
# CONFIGURACIÓN DE CONEXIONES
# ==========================================
DB_TRANSACCIONAL = {
    "host": "localhost",
    "port": 5432,
    "database": "libreria",      
    "user": "postgres",
    "password": "21970"      
}

DB_ANALISIS = {
    "host": "localhost",
    "port": 5432,
    "database": "analisis_libreria", 
    "user": "postgres",
    "password": "21970"
}

def ejecutar_etl():
    print("Iniciando proceso ETL...")
    conn_src = None
    conn_dst = None

    try:
        conn_src = psycopg2.connect(**DB_TRANSACCIONAL)
        conn_dst = psycopg2.connect(**DB_ANALISIS)

        with conn_src.cursor() as cur_src, conn_dst.cursor() as cur_dst:
            
            # ==========================================
            # 1. CARGA DE DIMENSIÓN: CLIENTE
            # ==========================================
            print("Extrayendo datos de clientes...")
            sql_extract_cliente = """
                SELECT 
                    id_cliente, 
                    TRIM(nombre || ' ' || COALESCE(apellido, '')) AS nombre_completo, 
                    rut, 
                    telefono
                FROM cliente;
            """
            cur_src.execute(sql_extract_cliente)
            filas_clientes = cur_src.fetchall()

            if filas_clientes:
                sql_insert_cliente = """
                    INSERT INTO dim_cliente
                    (id_cliente, nombre_completo, rut, telefono)
                    VALUES %s
                    ON CONFLICT (id_cliente) DO UPDATE SET
                        nombre_completo = EXCLUDED.nombre_completo,
                        telefono = EXCLUDED.telefono;
                """
                execute_values(cur_dst, sql_insert_cliente, filas_clientes)
                print(f"✅ Se cargaron/actualizaron {len(filas_clientes)} clientes.")

            # ==========================================
            # 2. CARGA DE DIMENSIÓN: SUCURSAL
            # ==========================================
            print("Extrayendo datos de sucursales...")
            sql_extract_sucursal = """
                SELECT id_sucursal, nombre AS nombre_sucursal, direccion, comuna
                FROM sucursal;
            """
            cur_src.execute(sql_extract_sucursal)
            filas_sucursales = cur_src.fetchall()

            if filas_sucursales:
                sql_insert_sucursal = """
                    INSERT INTO dim_sucursal
                    (id_sucursal, nombre_sucursal, direccion, comuna)
                    VALUES %s
                    ON CONFLICT (id_sucursal) DO UPDATE SET
                        nombre_sucursal = EXCLUDED.nombre_sucursal,
                        direccion = EXCLUDED.direccion,
                        comuna = EXCLUDED.comuna;
                """
                execute_values(cur_dst, sql_insert_sucursal, filas_sucursales)
                print(f"✅ Se cargaron/actualizaron {len(filas_sucursales)} sucursales.")

            # ==========================================
            # 3. CARGA DE DIMENSIÓN: EMPLEADO
            # ==========================================
            print("Extrayendo datos de empleados...")
            sql_extract_empleado = """
                SELECT 
                    id_empleado, 
                    TRIM(nombre || ' ' || apellido) AS nombre_completo, 
                    rut, 
                    rol::VARCHAR, 
                    tipo_turno::VARCHAR
                FROM empleado;
            """
            cur_src.execute(sql_extract_empleado)
            filas_empleados = cur_src.fetchall()

            if filas_empleados:
                sql_insert_empleado = """
                    INSERT INTO dim_empleado
                    (id_empleado, nombre_completo, rut, rol, tipo_turno)
                    VALUES %s
                    ON CONFLICT (id_empleado) DO UPDATE SET
                        nombre_completo = EXCLUDED.nombre_completo,
                        rol = EXCLUDED.rol,
                        tipo_turno = EXCLUDED.tipo_turno;
                """
                execute_values(cur_dst, sql_insert_empleado, filas_empleados)
                print(f"✅ Se cargaron/actualizaron {len(filas_empleados)} empleados.")

            # ==========================================
            # 4. CARGA DE DIMENSIÓN: PRODUCTO
            # ==========================================
            print("Extrayendo datos de productos (libros y artículos)...")
            sql_extract_producto = """
                SELECT 
                    p.id_producto,
                    p.nombre AS nombre_producto,
                    CASE WHEN l.id_libro IS NOT NULL THEN 'Libro' ELSE 'Otro' END AS tipo_item,
                    l.titulo AS titulo_libro,
                    c.tipo AS categoria_libro,
                    TRIM(a.nombre || ' ' || a.apellido) AS autor_nombre,
                    a.nacionalidad AS nacionalidad_autor,
                    e.nombre AS editorial_nombre,
                    s.nombre AS saga_nombre,
                    p.precio AS precio_referencial
                FROM producto p
                LEFT JOIN libro l ON p.id_producto = l.id_producto
                LEFT JOIN categoria c ON l.id_categoria = c.id_categoria
                LEFT JOIN autor a ON l.id_autor = a.id_autor
                LEFT JOIN editorial e ON l.id_editorial = e.id_editorial
                LEFT JOIN sagas s ON l.id_saga = s.id_saga;
            """
            cur_src.execute(sql_extract_producto)
            filas_productos = cur_src.fetchall()

            if filas_productos:
                sql_insert_producto = """
                    INSERT INTO dim_producto
                    (id_producto, nombre_producto, tipo_item, titulo_libro, categoria_libro, 
                     autor_nombre, nacionalidad_autor, editorial_nombre, saga_nombre, precio_referencial)
                    VALUES %s
                    ON CONFLICT (id_producto) DO UPDATE SET
                        nombre_producto = EXCLUDED.nombre_producto,
                        tipo_item = EXCLUDED.tipo_item,
                        titulo_libro = EXCLUDED.titulo_libro,
                        categoria_libro = EXCLUDED.categoria_libro,
                        autor_nombre = EXCLUDED.autor_nombre,
                        nacionalidad_autor = EXCLUDED.nacionalidad_autor,
                        editorial_nombre = EXCLUDED.editorial_nombre,
                        saga_nombre = EXCLUDED.saga_nombre,
                        precio_referencial = EXCLUDED.precio_referencial;
                """
                execute_values(cur_dst, sql_insert_producto, filas_productos)
                print(f"✅ Se cargaron/actualizaron {len(filas_productos)} productos.")

            # ==========================================
            # 5. CARGA DE DIMENSIÓN: TIEMPO
            # ==========================================
            print("Extrayendo datos de tiempo...")
            sql_extract_tiempo = """
                SELECT DISTINCT
                    TO_CHAR(fecha_hora, 'YYYYMMDD')::int AS id_tiempo,
                    DATE(fecha_hora) AS fecha,
                    EXTRACT(YEAR FROM fecha_hora)::int AS anio,
                    EXTRACT(MONTH FROM fecha_hora)::int AS mes,
                    TRIM(TO_CHAR(fecha_hora, 'TMMonth')) AS nombre_mes,
                    EXTRACT(DAY FROM fecha_hora)::int AS dia,
                    EXTRACT(QUARTER FROM fecha_hora)::int AS trimestre,
                    TRIM(TO_CHAR(fecha_hora, 'TMDay')) AS dia_semana
                FROM venta
                ORDER BY id_tiempo;
            """
            cur_src.execute(sql_extract_tiempo)
            filas_tiempo = cur_src.fetchall()

            if filas_tiempo:
                sql_insert_tiempo = """
                    INSERT INTO dim_tiempo
                    (id_tiempo, fecha, anio, mes, nombre_mes, dia, trimestre, dia_semana)
                    VALUES %s
                    ON CONFLICT (id_tiempo) DO NOTHING;
                """
                execute_values(cur_dst, sql_insert_tiempo, filas_tiempo)
                print(f"✅ Se cargaron/verificaron {len(filas_tiempo)} registros de tiempo.")

            # ==========================================
            # 6. CARGA DE LA TABLA DE HECHOS: VENTAS
            # ==========================================
            print("Extrayendo datos de la tabla de hechos...")
            sql_extract_hechos = """
                SELECT
                    TO_CHAR(v.fecha_hora, 'YYYYMMDD')::int AS id_tiempo,
                    dv.id_producto,
                    cj.id_sucursal,
                    v.id_cliente,
                    caj.id_empleado,
                    dv.cantidad,
                    dv.precio_unitario,
                    dv.subtotal,
                    v.id_venta AS id_venta_origen,
                    dv.id_detalle AS id_detalle_origen
                FROM detalleventa dv
                JOIN venta v ON dv.id_venta = v.id_venta
                JOIN caja cj ON v.id_caja = cj.id_caja
                JOIN cajero caj ON v.id_cajero = caj.id_cajero;
            """
            cur_src.execute(sql_extract_hechos)
            filas_hechos = cur_src.fetchall()

            if filas_hechos:
                sql_insert_hechos = """
                    INSERT INTO hechos_ventas
                    (id_tiempo, id_producto, id_sucursal, id_cliente, id_empleado, 
                     cantidad, precio_unitario, subtotal, id_venta_origen, id_detalle_origen)
                    VALUES %s
                    ON CONFLICT (id_detalle_origen) DO UPDATE SET
                        cantidad = EXCLUDED.cantidad,
                        precio_unitario = EXCLUDED.precio_unitario,
                        subtotal = EXCLUDED.subtotal;
                """
                execute_values(cur_dst, sql_insert_hechos, filas_hechos)
                print(f"✅ Se cargaron/actualizaron {len(filas_hechos)} registros en la tabla de hechos.")

        conn_dst.commit()
        print("🎉 Proceso ETL completado con éxito.")

    except Exception as e:
        print(f"❌ Error durante el ETL: {e}")
        if conn_dst:
            conn_dst.rollback() 

    finally:
        if conn_src:
            conn_src.close()
        if conn_dst:
            conn_dst.close()
        print("Conexiones a las bases de datos cerradas.")

if __name__ == "__main__":
    ejecutar_etl()