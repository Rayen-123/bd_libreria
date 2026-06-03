from database import conectar
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def obtener_clientes():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT id_cliente, nombre, apellido
        FROM cliente
        ORDER BY nombre
    """)

    clientes = cur.fetchall()

    cur.close()
    conn.close()

    return clientes

def obtener_productos():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT id_producto, nombre, precio
        FROM producto
        ORDER BY nombre
    """)

    productos = cur.fetchall()

    cur.close()
    conn.close()

    return productos

def obtener_sucursales():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT id_sucursal, nombre
        FROM sucursal
        ORDER BY nombre
    """)

    sucursales = cur.fetchall()

    cur.close()
    conn.close()

    return sucursales

def obtener_cajeros():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            c.id_cajero,
            e.nombre,
            e.apellido
        FROM cajero c
        JOIN empleado e
            ON c.id_empleado = e.id_empleado
        ORDER BY e.nombre
    """)

    cajeros = cur.fetchall()

    cur.close()
    conn.close()

    return cajeros

#CRUD SQL Venta
def crear_venta(id_cliente, id_caja, id_cajero):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO venta(
            fecha_hora,
            total,
            id_cliente,
            id_caja,
            id_cajero
        )
        VALUES(
            NOW(),
            0,
            %s,
            %s,
            %s
        )
        RETURNING id_venta
    """, (
        id_cliente,
        id_caja,
        id_cajero
    ))

    id_venta = cur.fetchone()[0]

    conn.commit()

    cur.close()
    conn.close()

    return id_venta
    
def agregar_detalle(id_venta, id_producto,cantidad,precio):

    conn = conectar()
    cur = conn.cursor()

    subtotal = cantidad * precio

    cur.execute("""
        INSERT INTO detalleventa(
            id_venta,
            id_producto,
            cantidad,
            precio_unitario,
            subtotal
        )
        VALUES(
            %s,
            %s,
            %s,
            %s,
            %s
        )
    """, (id_venta,id_producto,cantidad,precio,subtotal))

    conn.commit()

    cur.close()
    conn.close()

    return subtotal
    
def actualizar_total(id_venta, total):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        UPDATE venta
        SET total = %s
        WHERE id_venta = %s
    """, (total, id_venta))

    conn.commit()

    cur.close()
    conn.close()


def abrir_ventas():

    ventana = tk.Toplevel()

    ventana.title("Ventas")
    ventana.geometry("700x500")

    #Cliente
    tk.Label(
        ventana,
        text="Cliente"
    ).pack()

    combo_cliente = ttk.Combobox(
        ventana,
        width=40
    )

    combo_cliente.pack(pady=5)

    clientes = obtener_clientes()

    combo_cliente["values"] = [
        f"{cliente[0]} - {cliente[1]} {cliente[2]}"
        for cliente in clientes
    ]

    #Sucursal
    tk.Label(
        ventana,
        text="Sucursal"
    ).pack()

    combo_sucursal = ttk.Combobox(
        ventana,
        width=40
    )

    combo_sucursal.pack(pady=5)

    sucursales = obtener_sucursales()

    combo_sucursal["values"] = [
        f"{s[0]} - {s[1]}"
        for s in sucursales
    ]

    #Cajero
    tk.Label(
        ventana,
        text="Cajero"
    ).pack()

    combo_cajero = ttk.Combobox(
        ventana,
        width=40
    )

    combo_cajero.pack(pady=5)

    cajeros = obtener_cajeros()

    combo_cajero["values"] = [
        f"{c[0]} - {c[1]} {c[2]}"
        for c in cajeros
    ]

    #Producto
    tk.Label(
        ventana,
        text="Producto"
    ).pack()

    combo_producto = ttk.Combobox(
        ventana,
        width=40
    )

    combo_producto.pack(pady=5)

    productos = obtener_productos()

    combo_producto["values"] = [
        f"{producto[0]} - {producto[1]}"
        for producto in productos
    ]

    tk.Label(
        ventana,
        text="Cantidad"
    ).pack()

    entry_cantidad = tk.Entry(ventana)

    entry_cantidad.pack(pady=5)

    
    def registrar():

        id_cliente = int(
            combo_cliente.get().split(" - ")[0]
        )

        id_producto = int(
            combo_producto.get().split(" - ")[0]
        )

        id_sucursal = int(
            combo_sucursal.get().split(" - ")[0]
        )

        id_cajero = int(
            combo_cajero.get().split(" - ")[0]
        )

        cantidad = int(
            entry_cantidad.get()
        )

        producto = next(
            p for p in productos
            if p[0] == id_producto
        )

        precio = producto[2]

        id_venta = crear_venta(
            id_cliente
        )

        subtotal = agregar_detalle(
            id_venta,
            id_producto,
            cantidad,
            precio
        )

        actualizar_total(
            id_venta,
            subtotal
        )

        messagebox.showinfo(
        "Venta",
        "Venta registrada correctamente"
        )
        print("Venta registrada")

        combo_cliente.set("")
        combo_producto.set("")
        entry_cantidad.delete(0, tk.END)

    tk.Button(
        ventana,
        text="Registrar Venta",
        command=registrar
    ).pack(pady=20)

    