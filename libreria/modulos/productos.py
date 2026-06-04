import tkinter as tk
from tkinter import ttk
from database import conectar

def abrir_productos():

    ventana_productos = tk.Toplevel()

    ventana_productos.title("Productos")
    ventana_productos.geometry("1100x600")

    tk.Label(
        ventana_productos,
        text="Gestión de Productos",
        font=("Arial", 16)
    ).pack(pady=10)

    #Formulario
    frame_form = tk.Frame(ventana_productos)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="Nombre").grid(row=0, column=0)

    entry_nombre = tk.Entry(frame_form)
    entry_nombre.grid(row=0, column=1)

    tk.Label(frame_form, text="Precio").grid(row=1, column=0)

    entry_precio = tk.Entry(frame_form)
    entry_precio.grid(row=1, column=1)

    producto_seleccionado = None

    #CRUD Productos
    def cargar_productos():

        for fila in tabla.get_children():
            tabla.delete(fila)

        productos = obtener_productos()

        for producto in productos:
            tabla.insert("", "end", values=producto)

    def seleccionar_producto(event):

        nonlocal producto_seleccionado

        seleccion = tabla.selection()

        if not seleccion:
            return

        valores = tabla.item(seleccion[0])["values"]

        producto_seleccionado = valores[0]

        entry_nombre.delete(0, tk.END)
        entry_precio.delete(0, tk.END)

        entry_nombre.insert(0, valores[1])
        entry_precio.insert(0, valores[2])

    def guardar():

        nombre = entry_nombre.get()
        precio = entry_precio.get()
 
        guardar_producto(
            nombre,
            precio
        )

        cargar_productos()

        entry_nombre.delete(0, tk.END)
        entry_precio.delete(0, tk.END)

        print("Producto guardado")
        
    def editar():

        if producto_seleccionado is None:
            return

        actualizar_producto(
            producto_seleccionado,
            entry_nombre.get(),
            entry_precio.get(),
        )

        cargar_productos()

    def eliminar():

        seleccion = tabla.selection()

        if not seleccion:
            return

        valores = tabla.item(seleccion[0])["values"]

        id_producto = valores[0]

        eliminar_producto(id_producto)

        cargar_productos()

    tk.Button(
        ventana_productos,
        text="Guardar Producto",
        command=guardar
    ).pack(pady=10)

    #Tabla de productos
    tabla = ttk.Treeview(
        ventana_productos,
        columns=("ID", "Nombre", "Precio"),
        show="headings"
    )

    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Precio", text="Precio")

    tabla.pack(fill="both", expand=True)

    tabla.bind(
        "<<TreeviewSelect>>",
        seleccionar_producto
    )

    def cargar_productos():

        for fila in tabla.get_children():
            tabla.delete(fila)

        productos = obtener_productos()

        for producto in productos:
            tabla.insert("", "end", values=producto)

    cargar_productos()
    
    tk.Button(
        ventana_productos,
        text="Eliminar Producto",
        command=eliminar
    ).pack(pady=5)

    tk.Button(
        ventana_productos,
        text="Actualizar Producto",
        command=editar
    ).pack(pady=5)


#CRUD Productos SQL
def guardar_producto(nombre, precio):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO producto(nombre, precio)
        VALUES (%s, %s)
    """, (nombre, precio))

    conn.commit()

    cur.close()
    conn.close()

def obtener_productos():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT id_producto, nombre, precio
        FROM producto
        ORDER BY id_producto
    """)

    productos = cur.fetchall()

    cur.close()
    conn.close()

    return productos

def eliminar_producto(id_producto):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM producto
        WHERE id_producto = %s
    """, (id_producto,))

    conn.commit()

    cur.close()
    conn.close()

def actualizar_producto(id_producto, nombre, precio):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        UPDATE producto
        SET nombre = %s,
            precio = %s
        WHERE id_producto = %s
    """, (nombre, precio, id_producto))

    conn.commit()

    cur.close()
    conn.close()