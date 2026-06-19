import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def crear_graficos():
    print("Cargando datos desde los CSV...")
    
    try:
        # Leer los archivos CSV
        df_libros = pd.read_csv('libros_mas_vendidos.csv')
        df_clientes = pd.read_csv('clientes_frecuentes.csv')
        df_dias = pd.read_csv('ventas_por_dia.csv')
        df_cajeros = pd.read_csv('ventas_por_cajero.csv')

        sns.set_theme(style="whitegrid")

        # --- Limpieza de columnas de seguridad ---
        for df in [df_libros, df_clientes, df_dias, df_cajeros]:
            df.columns = df.columns.str.strip()
        
        # Renombramos la primera columna dinámicamente para evitar KeyErrors 
        # en caso de que la BD devuelva nombres ligeramente diferentes
        df_libros.rename(columns={df_libros.columns[0]: 'producto'}, inplace=True)
        df_clientes.rename(columns={df_clientes.columns[0]: 'cliente'}, inplace=True)
        df_cajeros.rename(columns={df_cajeros.columns[0]: 'cajero'}, inplace=True)

        # ---------------------------------------------------------
        # 1. Libros / Productos Más Vendidos (Barras Horizontales)
        # ---------------------------------------------------------
        print("Generando gráfico de libros más vendidos...")
        fig1, ax1 = plt.subplots(figsize=(12, 6))
        
        top_10 = df_libros.head(10)
        sns.barplot(data=top_10, x='copias_vendidas', y='producto', palette='magma', ax=ax1)
        
        ax1.set_title('Top 10 Libros / Productos Más Vendidos', fontsize=14, pad=15)
        ax1.set_xlabel('Unidades Vendidas', fontsize=12)
        ax1.set_ylabel('Producto', fontsize=12)

        fig1.tight_layout()
        fig1.savefig('01_libros_mas_vendidos.png', dpi=300)

        # ---------------------------------------------------------
        # 2. Clientes Frecuentes (Gráfico de Dispersión)
        # ---------------------------------------------------------
        print("Generando gráfico de clientes frecuentes...")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        
        sns.scatterplot(data=df_clientes, x='total_compras', y='total_gastado', 
                        size='articulos_comprados', hue='cliente', sizes=(50, 400), 
                        palette='tab10', ax=ax2, legend=False)
        
        # Etiquetar los top 5 clientes
        for i in range(min(5, len(df_clientes))):
            ax2.text(df_clientes['total_compras'][i] + 0.1, 
                     df_clientes['total_gastado'][i], 
                     df_clientes['cliente'][i], fontsize=9)

        ax2.set_title('Top Clientes: Frecuencia de Compra vs Gasto Total', fontsize=14, pad=15)
        ax2.set_xlabel('Total de Compras (Frecuencia)', fontsize=12)
        ax2.set_ylabel('Total Gastado Acumulado ($)', fontsize=12)

        fig2.tight_layout()
        fig2.savefig('02_clientes_frecuentes.png', dpi=300)

        # ---------------------------------------------------------
        # 3. Ventas por Día (Gráfico de Líneas)
        # ---------------------------------------------------------
        print("Generando gráfico de ventas por día...")
        df_dias['fecha'] = pd.to_datetime(df_dias['fecha'])
        
        fig3, ax3 = plt.subplots(figsize=(12, 5))
        sns.lineplot(data=df_dias, x='fecha', y='ingresos_diarios', marker='o', color='teal', ax=ax3)
        
        ax3.set_title('Evolución Diaria de Ingresos', fontsize=14, pad=15)
        ax3.set_xlabel('Fecha', fontsize=12)
        ax3.set_ylabel('Ingresos Diarios Totales ($)', fontsize=12)
        plt.xticks(rotation=45)

        fig3.tight_layout()
        fig3.savefig('03_ventas_por_dia.png', dpi=300)

        # ---------------------------------------------------------
        # 4. Ventas por Cajero (Gráfico de Barras Agrupado)
        # ---------------------------------------------------------
        print("Generando gráfico de ventas por cajero...")
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        
        sns.barplot(data=df_cajeros, x='cajero', y='ingresos_generados', hue='tipo_turno', 
                    palette='Set2', ax=ax4)
        
        ax4.set_title('Ingresos Generados por Cajero y Turno', fontsize=14, pad=15)
        ax4.set_xlabel('Cajero', fontsize=12)
        ax4.set_ylabel('Ingresos Generados ($)', fontsize=12)
        plt.xticks(rotation=15)

        fig4.tight_layout()
        fig4.savefig('04_ventas_por_cajero.png', dpi=300)

        print("¡Listo! Las 4 imágenes PNG se han generado con éxito.")

    except FileNotFoundError as e:
        print(f"Error: No se encontró uno de los CSV. Asegúrate de ejecutar extraer_csv.py primero. Detalle: {e}")
    except Exception as e:
        print(f"Error inesperado al generar los gráficos: {e}")

if __name__ == "__main__":
    crear_graficos()