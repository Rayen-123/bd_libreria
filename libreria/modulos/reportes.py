import tkinter as tk
from tkinter import ttk
from database import conectar

def abrir_menu_reportes():

    ventana = tk.Toplevel()

    ventana.title("Reportes")
    ventana.geometry("300x250")

    tk.Label(
        ventana,
        text="Reportes",
        font=("Arial", 14)
    ).pack(pady=10)

    tk.Button(
        ventana,
        text="Libros Más Vendidos",
        width=25,
        command=abrir_reporte_libros
    ).pack(pady=5)

    tk.Button(
        ventana,
        text="Clientes Frecuentes",
        width=25,
        command=abrir_reporte_clientes
    ).pack(pady=5)

    tk.Button(
        ventana,
        text="Ventas por Día",
        width=25,
        command=abrir_reporte_ventas_dia
    ).pack(pady=5)

    tk.Button(
        ventana,
        text="Ventas por Cajero",
        width=25,
        command=abrir_reporte_cajeros
    ).pack(pady=5)

def obtener_libros_mas_vendidos():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            l.titulo,
            SUM(dv.cantidad) AS vendidos
        FROM detalleventa dv
        JOIN libro l
            ON dv.id_producto = l.id_producto
        GROUP BY l.titulo
        ORDER BY vendidos DESC
    """)

    datos = cur.fetchall()

    cur.close()
    conn.close()

    return datos

def abrir_reporte_libros():

    ventana = tk.Toplevel()

    ventana.title("Libros Más Vendidos")
    ventana.geometry("700x500")

    tk.Label(
        ventana,
        text="Reporte de Libros Más Vendidos",
        font=("Arial", 16)
    ).pack(pady=10)

    tabla = ttk.Treeview(
        ventana,
        columns=(
            "Titulo",
            "Vendidos"
        ),
        show="headings"
    )

    tabla.heading(
        "Titulo",
        text="Título"
    )

    tabla.heading(
        "Vendidos",
        text="Cantidad Vendida"
    )

    tabla.pack(
        fill="both",
        expand=True,
        pady=10
    )

    datos = obtener_libros_mas_vendidos()

    for fila in datos:

        tabla.insert(
            "",
            "end",
            values=fila
        )

def obtener_clientes_frecuentes():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            c.nombre || ' ' || c.apellido AS cliente,
            SUM(v.total) AS total_comprado
        FROM venta v
        JOIN cliente c
            ON v.id_cliente = c.id_cliente
        GROUP BY c.id_cliente, c.nombre, c.apellido
        ORDER BY total_comprado DESC
    """)

    datos = cur.fetchall()

    cur.close()
    conn.close()

    return datos

def abrir_reporte_clientes():

    ventana = tk.Toplevel()

    ventana.title("Clientes Frecuentes")
    ventana.geometry("700x500")

    tk.Label(
        ventana,
        text="Clientes que Más Compran",
        font=("Arial", 16)
    ).pack(pady=10)

    tabla = ttk.Treeview(
        ventana,
        columns=("Cliente", "Total"),
        show="headings"
    )

    tabla.heading("Cliente", text="Cliente")
    tabla.heading("Total", text="Total Comprado")

    tabla.pack(fill="both", expand=True)

    for fila in obtener_clientes_frecuentes():
        tabla.insert("", "end", values=fila)

def obtener_ventas_por_dia():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            DATE(fecha_hora) AS fecha,
            SUM(total) AS total_vendido
        FROM venta
        GROUP BY DATE(fecha_hora)
        ORDER BY fecha DESC
    """)

    datos = cur.fetchall()

    cur.close()
    conn.close()

    return datos

def abrir_reporte_ventas_dia():

    ventana = tk.Toplevel()

    ventana.title("Ventas por Día")
    ventana.geometry("600x500")

    tk.Label(
        ventana,
        text="Ventas por Día",
        font=("Arial", 16)
    ).pack(pady=10)

    tabla = ttk.Treeview(
        ventana,
        columns=("Fecha", "Total"),
        show="headings"
    )

    tabla.heading("Fecha", text="Fecha")
    tabla.heading("Total", text="Total Vendido")

    tabla.pack(fill="both", expand=True)

    for fila in obtener_ventas_por_dia():
        tabla.insert("", "end", values=fila)

def obtener_ventas_por_cajero():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            e.nombre || ' ' || e.apellido AS cajero,
            COUNT(v.id_venta) AS ventas
        FROM venta v
        JOIN cajero c
            ON v.id_cajero = c.id_cajero
        JOIN empleado e
            ON c.id_empleado = e.id_empleado
        GROUP BY e.nombre, e.apellido
        ORDER BY ventas DESC
    """)

    datos = cur.fetchall()

    cur.close()
    conn.close()

    return datos

def abrir_reporte_cajeros():

    ventana = tk.Toplevel()

    ventana.title("Ventas por Cajero")
    ventana.geometry("700x500")

    tk.Label(
        ventana,
        text="Ventas por Cajero",
        font=("Arial", 16)
    ).pack(pady=10)

    tabla = ttk.Treeview(
        ventana,
        columns=("Cajero", "Ventas"),
        show="headings"
    )

    tabla.heading("Cajero", text="Cajero")
    tabla.heading("Ventas", text="Cantidad de Ventas")

    tabla.pack(fill="both", expand=True)

    for fila in obtener_ventas_por_cajero():
        tabla.insert("", "end", values=fila)