import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import conectar

def obtener_ventas():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            v.id_venta,
            v.fecha_hora,
            c.nombre || ' ' || c.apellido,
            v.total
        FROM venta v
        JOIN cliente c
            ON v.id_cliente = c.id_cliente
        ORDER BY v.id_venta DESC
    """)

    ventas = cur.fetchall()

    cur.close()
    conn.close()

    return ventas

def obtener_detalle_venta(id_venta):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            p.nombre,
            d.cantidad,
            d.precio_unitario,
            d.subtotal
        FROM detalleventa d
        JOIN producto p
            ON d.id_producto = p.id_producto
        WHERE d.id_venta = %s
    """, (id_venta,))

    detalles = cur.fetchall()

    cur.close()
    conn.close()

    return detalles

def abrir_historial_ventas():

    ventana = tk.Toplevel()

    ventana.title("Historial de Ventas")
    ventana.geometry("900x600")

    venta_seleccionada = None

    tabla = ttk.Treeview(
        ventana,
        columns=(
            "ID",
            "Fecha",
            "Cliente",
            "Total"
        ),
        show="headings"
    )

    tabla.heading("ID", text="ID")
    tabla.heading("Fecha", text="Fecha")
    tabla.heading("Cliente", text="Cliente")
    tabla.heading("Total", text="Total")

    tabla.pack(
        fill="both",
        expand=True,
        pady=10
    )

    tk.Label(
        ventana,
        text="Detalle de la Venta",
        font=("Arial", 12)
    ).pack(pady=5)

    tabla_detalle = ttk.Treeview(
        ventana,
        columns=(
            "Producto",
            "Cantidad",
            "Precio",
            "Subtotal"
        ),
        show="headings"
    )

    tabla_detalle.heading("Producto", text="Producto")
    tabla_detalle.heading("Cantidad", text="Cantidad")
    tabla_detalle.heading("Precio", text="Precio Unitario")
    tabla_detalle.heading("Subtotal", text="Subtotal")

    tabla_detalle.pack(
        fill="both",
        expand=True,
        pady=10
    )

    def cargar_ventas():

        for fila in tabla.get_children():
            tabla.delete(fila)

        ventas = obtener_ventas()

        print(ventas)

        for venta in ventas:
            tabla.insert(
                "",
                "end",
                values=venta
            )
    
    def cargar_detalle(id_venta):

        for fila in tabla_detalle.get_children():
            tabla_detalle.delete(fila)

        detalles = obtener_detalle_venta(id_venta)

        for detalle in detalles:
            tabla_detalle.insert(
                "",
                "end",
                values=detalle
            )
    
    def seleccionar_venta(event):

        nonlocal venta_seleccionada

        seleccion = tabla.selection()

        if not seleccion:
            return

        valores = tabla.item(
            seleccion[0]
        )["values"]

        venta_seleccionada = valores[0]

        cargar_detalle(venta_seleccionada)

    def eliminar():

        if venta_seleccionada is None:
            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Desea eliminar esta venta?"
        )

        if not confirmar:
            return

        eliminar_venta(
            venta_seleccionada
        )

        cargar_ventas()

        for fila in tabla_detalle.get_children():
            tabla_detalle.delete(fila)

    tk.Button(
        ventana,
        text="Eliminar Venta",
        command=eliminar
    ).pack(pady=10)

    tabla.bind(
        "<<TreeviewSelect>>",
        seleccionar_venta
    )

    cargar_ventas()

def eliminar_venta(id_venta):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM detalleventa
        WHERE id_venta = %s
    """, (id_venta,))

    cur.execute("""
        DELETE FROM venta
        WHERE id_venta = %s
    """, (id_venta,))

    conn.commit()

    cur.close()
    conn.close()

