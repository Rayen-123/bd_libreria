import psycopg2
import csv
import os

# Configuración de tu base de datos analítica
DB_ANALISIS = {
    "host": "localhost",
    "port": 5432,
    "database": "analisis_libreria",
    "user": "postgres",
    "password": "21970" 
}

OUTPUT_DIR = "."

consultas = [
    {
        "archivo": "libros_mas_vendidos.csv",
        "sql": """
            SELECT 
                COALESCE(p.titulo_libro, p.nombre_producto) AS producto,
                COALESCE(p.autor_nombre, 'Desconocido') AS autor,
                SUM(h.cantidad) AS copias_vendidas,
                SUM(h.subtotal) AS ingresos_generados
            FROM hechos_ventas h
            JOIN dim_producto p ON h.id_producto = p.id_producto
            GROUP BY producto, autor
            ORDER BY copias_vendidas DESC
            LIMIT 15;
        """
    },
    {
        "archivo": "clientes_frecuentes.csv",
        "sql": """
            SELECT 
                c.nombre_completo AS cliente,
                COUNT(DISTINCT h.id_venta_origen) AS total_compras,
                SUM(h.cantidad) AS articulos_comprados,
                SUM(h.subtotal) AS total_gastado
            FROM hechos_ventas h
            JOIN dim_cliente c ON h.id_cliente = c.id_cliente
            GROUP BY c.nombre_completo
            ORDER BY total_compras DESC, total_gastado DESC
            LIMIT 20;
        """
    },
    {
        "archivo": "ventas_por_dia.csv",
        "sql": """
            SELECT 
                t.fecha,
                t.dia_semana,
                SUM(h.cantidad) AS cantidad_vendida,
                SUM(h.subtotal) AS ingresos_diarios
            FROM hechos_ventas h
            JOIN dim_tiempo t ON h.id_tiempo = t.id_tiempo
            GROUP BY t.fecha, t.dia_semana
            ORDER BY t.fecha ASC;
        """
    },
    {
        "archivo": "ventas_por_cajero.csv",
        "sql": """
            SELECT 
                e.nombre_completo AS cajero,
                e.tipo_turno,
                COUNT(h.id_detalle_origen) AS operaciones_realizadas,
                SUM(h.cantidad) AS cantidad_vendida,
                SUM(h.subtotal) AS ingresos_generados
            FROM hechos_ventas h
            JOIN dim_empleado e ON h.id_empleado = e.id_empleado
            WHERE e.rol = 'cajero'
            GROUP BY e.nombre_completo, e.tipo_turno
            ORDER BY ingresos_generados DESC;
        """
    }
]

def extraer_datos():
    print("Iniciando extracción de datos a CSV...\n")
    conn = None

    try:
        conn = psycopg2.connect(**DB_ANALISIS)
        
        with conn.cursor() as cur:
            for c in consultas:
                archivo = c["archivo"]
                print(f"Generando {archivo}...")
                
                cur.execute(c["sql"])
                resultados = cur.fetchall()
                
                if resultados:
                    columnas = [desc[0] for desc in cur.description]
                    ruta_archivo = os.path.join(OUTPUT_DIR, archivo)
                    with open(ruta_archivo, "w", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow(columnas)
                        writer.writerows(resultados)
                        
                    print(f"  → ¡Listo! {len(resultados)} filas exportadas.\n")
                else:
                    print(f"  → La consulta no devolvió datos (Verifica si hay ventas en la BD).\n")

    except Exception as e:
        print(f"❌ Error durante la extracción: {e}")

    finally:
        if conn:
            conn.close()
        print("Proceso finalizado. Conexión cerrada.")

if __name__ == "__main__":
    extraer_datos()