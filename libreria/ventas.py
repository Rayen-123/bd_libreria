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

def obtener_cajas():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id_caja,
            numero_caja
        FROM caja
        ORDER BY numero_caja
    """)

    cajas = cur.fetchall()

    cur.close()
    conn.close()

    return cajas

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
    """, (
        total,
        id_venta
    ))

    conn.commit()

    cur.close()
    conn.close()


def abrir_ventas():

    ventana = tk.Toplevel()

    ventana.title("Ventas")
    ventana.geometry("900x700")

    detalle_venta = []

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
        f"{cajero[0]} - {cajero[1]}"
        for cajero in cajeros
    ]

    #Caja
    tk.Label(
        ventana,
        text="Caja"
    ).pack()

    combo_caja = ttk.Combobox(
        ventana,
        width=40
    )

    combo_caja.pack(pady=5)

    cajas = obtener_cajas()

    combo_caja["values"] = [
        f"{caja[0]} - Caja {caja[1]}"
        for caja in cajas
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
    tabla_detalle.heading("Precio", text="Precio")
    tabla_detalle.heading("Subtotal", text="Subtotal")

    tabla_detalle.pack(
        fill="both",
        expand=True,
        pady=10
    )

    def cargar_detalle():

        for fila in tabla_detalle.get_children():
            tabla_detalle.delete(fila)

        for item in detalle_venta:

            tabla_detalle.insert(
                "",
                "end",
                values=(
                    item["nombre"],
                    item["cantidad"],
                    item["precio"],
                    item["subtotal"]
                )
            )

    def agregar_producto():

        id_producto = int(
            combo_producto.get().split(" - ")[0]
        )

        cantidad = int(
            entry_cantidad.get()
        )

        producto = next(
            p for p in productos
            if p[0] == id_producto
        )

        precio = producto[2]

        subtotal = precio * cantidad

        detalle_venta.append({
            "id_producto": id_producto,
            "nombre": producto[1],
            "cantidad": cantidad,
            "precio": precio,
            "subtotal": subtotal
        })

        cargar_detalle()

        entry_cantidad.delete(0, tk.END)

    tk.Button(
        ventana,
        text="Agregar Producto",
        command=agregar_producto
    ).pack(pady=5)


    def mostrar_confirmacion():

        def aceptar():

            combo_cliente.set("")
            combo_cajero.set("")
            combo_caja.set("")
            combo_sucursal.set("")
            combo_producto.set("")

            entry_cantidad.delete(0, tk.END)

            detalle_venta.clear()
            cargar_detalle()

            ventana_ok.destroy()

        ventana_ok = tk.Toplevel()

        ventana_ok.title("Venta registrada")
        ventana_ok.geometry("350x180")
        ventana_ok.resizable(False, False)

        tk.Label(
            ventana_ok,
            text="Venta registrada correctamente",
            font=("Arial", 12, "bold")
        ).pack(pady=20)

        frame_botones = tk.Frame(ventana_ok)
        frame_botones.pack(pady=10)

        tk.Button(
            frame_botones,
            text="Aceptar",
            width=12,
            command=aceptar
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            frame_botones,
            text="Imprimir Boleta",
            width=15
        ).grid(row=0, column=1, padx=10)
    
    def registrar():

        if not detalle_venta:
            print("No hay productos en la venta")
            return

        id_cliente = int(
            combo_cliente.get().split(" - ")[0]
        )

        id_cajero = int(
            combo_cajero.get().split(" - ")[0]
        )

        id_caja = int(
            combo_caja.get().split(" - ")[0]
        )

        id_venta = crear_venta(
            id_cliente,
            id_caja,
            id_cajero
        )

        total = 0


        for item in detalle_venta:

            agregar_detalle(
                id_venta,
                item["id_producto"],
                item["cantidad"],
                item["precio"]
            )

            total += item["subtotal"]

        actualizar_total(
            id_venta,
            total
        )

        mostrar_confirmacion()




    tk.Button(
        ventana,
        text="Registrar Venta",
        command=registrar
    ).pack(pady=20)

    