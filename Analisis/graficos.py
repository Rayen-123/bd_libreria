import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# 1. Configurar la conexión a PostgreSQL
# Cambia 'usuario' y 'tu_contraseña' por tus credenciales reales
cadena_conexion = 'postgresql+psycopg2://postgres:21970@localhost:5432/analisis_libreria'
engine = create_engine(cadena_conexion)

# ==========================================
# GRÁFICO 1: Ingresos Totales por Categoría de Libro
# ==========================================
consulta_categorias = """
    SELECT 
        p.categoria_libro, 
        SUM(h.subtotal) as ingresos_totales
    FROM hechos_ventas h
    JOIN dim_producto p ON h.id_producto = p.id_producto
    WHERE p.tipo_item = 'Libro'
    GROUP BY p.categoria_libro
    ORDER BY ingresos_totales DESC;
"""

# Leer datos directamente a un DataFrame
df_categorias = pd.read_sql_query(consulta_categorias, engine)

# Crear gráfico de barras
plt.figure(figsize=(10, 6))
plt.bar(df_categorias['categoria_libro'], df_categorias['ingresos_totales'], color='skyblue')
plt.title('Ingresos Totales por Categoría de Libro')
plt.xlabel('Categoría')
plt.ylabel('Ingresos ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ==========================================
# GRÁFICO 2: Tendencia de Ventas Mensuales en el Año
# ==========================================
consulta_tendencia = """
    SELECT 
        t.mes, 
        t.nombre_mes,
        SUM(h.subtotal) as total_ventas
    FROM hechos_ventas h
    JOIN dim_tiempo t ON h.id_tiempo = t.id_tiempo
    WHERE t.anio = 2024 -- Puedes ajustar el año
    GROUP BY t.mes, t.nombre_mes
    ORDER BY t.mes;
"""

# Leer datos
df_tendencia = pd.read_sql_query(consulta_tendencia, engine)

# Crear gráfico de líneas
plt.figure(figsize=(10, 6))
plt.plot(df_tendencia['nombre_mes'], df_tendencia['total_ventas'], marker='o', linestyle='-', color='coral')
plt.title('Tendencia de Ventas Mensuales (2024)')
plt.xlabel('Mes')
plt.ylabel('Total de Ventas ($)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# ==========================================
# GRÁFICO 3: Ingresos Totales por Cajero
# ==========================================
consulta_cajeros = """
    SELECT 
        e.nombre_completo AS cajero,
        SUM(h.subtotal) as ingresos_totales
    FROM hechos_ventas h
    JOIN dim_empleado e ON h.id_empleado = e.id_empleado
    GROUP BY e.nombre_completo
    ORDER BY ingresos_totales DESC;
"""

# Cargar los datos
df_cajeros = pd.read_sql_query(consulta_cajeros, engine)

# Calcula el mínimo y el máximo del DataFrame
minimo = df_cajeros['ingresos_totales'].min()
maximo = df_cajeros['ingresos_totales'].max()

# Crear el gráfico de barras
plt.figure(figsize=(10, 6))
plt.bar(df_cajeros['cajero'], df_cajeros['ingresos_totales'], color='mediumseagreen')
plt.title('Ingresos Totales Registrados por Cajero')
plt.xlabel('Cajero')
plt.ylabel('Ingresos Totales ($)')
plt.ylim(minimo * 0.95, maximo * 1.01)
plt.xticks(rotation=45, ha='right') # Rota los nombres por si son muy largos
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# ==========================================
# GRÁFICO 4: Top 10 Libros Más Vendidos (Por Cantidad)
# ==========================================
consulta_libros_mas_vendidos = """
    SELECT 
        p.titulo_libro AS libro,
        SUM(h.cantidad) as unidades_vendidas
    FROM hechos_ventas h
    JOIN dim_producto p ON h.id_producto = p.id_producto
    WHERE p.tipo_item = 'Libro' AND p.titulo_libro IS NOT NULL
    GROUP BY p.titulo_libro
    ORDER BY unidades_vendidas DESC
    LIMIT 10;
"""

df_libros = pd.read_sql_query(consulta_libros_mas_vendidos, engine)

plt.figure(figsize=(11, 7))

# Usamos barras horizontales (barh) para que los títulos de los libros se lean perfectamente
barras_libros = plt.barh(df_libros['libro'][::-1], df_libros['unidades_vendidas'][::-1], color='indianred')

plt.title('Top 10 Libros Más Vendidos en la Librería')
plt.xlabel('Unidades Vendidas')
plt.ylabel('Título del Libro')

# Agregar el número exacto al final de cada barra para no andar adivinando
for barra in barras_libros:
    ancho_barra = barra.get_width()
    plt.text(ancho_barra + 0.2, barra.get_y() + barra.get_height()/2,
             f'{int(ancho_barra)} ud', 
             va='center', ha='left', fontsize=9, fontweight='bold', color='maroon')

# Darle un margen extra a la derecha para que las etiquetas de texto quepan bien
plt.xlim(0, df_libros['unidades_vendidas'].max() * 1.12)

# Calcular el mínimo y máximo dentro del Top 10
minimo = df_libros['unidades_vendidas'].min()
maximo = df_libros['unidades_vendidas'].max()
plt.xlim(minimo * 0.95, maximo * 1.01)

# Estética limpia sin los bordes innecesarios
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.grid(axis='x', linestyle='--', alpha=0.4)
plt.tight_layout()
plt.show()

# ==========================================
# GRÁFICO 5: Comparativa Directa de Ventas por Sucursal
# ==========================================
consulta_simple = """
    SELECT 
        s.nombre_sucursal,
        SUM(h.subtotal) as ingresos_totales
    FROM hechos_ventas h
    JOIN dim_sucursal s ON h.id_sucursal = s.id_sucursal
    GROUP BY s.nombre_sucursal
    ORDER BY ingresos_totales DESC;
"""

df_simple = pd.read_sql_query(consulta_simple, engine)

plt.figure(figsize=(9, 5))

# Gráfico de barras simple
plt.bar(df_simple['nombre_sucursal'], df_simple['ingresos_totales'], color='royalblue', edgecolor='navy')

plt.title('Ingresos Totales por Sucursal', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Sucursal', fontsize=12)
plt.ylabel('Ingresos Totales ($)', fontsize=12)

# Añadir una cuadrícula horizontal suave para facilitar la lectura de los montos
plt.grid(axis='y', linestyle='--', alpha=0.5)

# Ajustar las etiquetas del eje X para que no se encimen
plt.xticks(rotation=30, ha='right')

plt.tight_layout()
plt.show()