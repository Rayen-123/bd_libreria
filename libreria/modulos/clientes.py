import tkinter as tk
from tkinter import ttk
from database import conectar

def abrir_clientes():

    ventana_clientes = tk.Toplevel()

    ventana_clientes.title("Clientes")
    ventana_clientes.geometry("1100x600")

    tk.Label(
        ventana_clientes,
        text="Gestión de Clientes",
        font=("Arial", 16)
    ).pack(pady=10)

    #Formulario
    frame_form = tk.Frame(ventana_clientes)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="Nombre").grid(row=0, column=0)

    entry_nombre = tk.Entry(frame_form)
    entry_nombre.grid(row=0, column=1)

    tk.Label(frame_form, text="Apellido").grid(row=1, column=0)

    entry_apellido = tk.Entry(frame_form)
    entry_apellido.grid(row=1, column=1)

    tk.Label(frame_form, text="RUT").grid(row=2, column=0)

    entry_rut = tk.Entry(frame_form)
    entry_rut.grid(row=2, column=1)

    tk.Label(frame_form, text="Teléfono").grid(row=3, column=0)

    entry_telefono = tk.Entry(frame_form)
    entry_telefono.grid(row=3, column=1)

    cliente_seleccionado = None

    #CRUD Clientes
    def cargar_clientes():

        for fila in tabla.get_children():
            tabla.delete(fila)

        clientes = obtener_clientes()

        for cliente in clientes:
            tabla.insert("", "end", values=cliente)

    def seleccionar_cliente(event):

        nonlocal cliente_seleccionado

        seleccion = tabla.selection()

        if not seleccion:
            return

        valores = tabla.item(seleccion[0])["values"]

        cliente_seleccionado = valores[0]

        entry_nombre.delete(0, tk.END)
        entry_apellido.delete(0, tk.END)
        entry_rut.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)

        entry_nombre.insert(0, valores[1])
        entry_apellido.insert(0, valores[2])
        entry_rut.insert(0, valores[3])
        entry_telefono.insert(0, valores[4])

    def guardar():

        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        rut = entry_rut.get()
        telefono = entry_telefono.get()

        guardar_cliente(
            nombre,
            apellido,
            rut,
            telefono
        )

        cargar_clientes()

        entry_nombre.delete(0, tk.END)
        entry_apellido.delete(0, tk.END)
        entry_rut.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)

        print("Cliente guardado")
        
    def editar():

        if cliente_seleccionado is None:
            return

        actualizar_cliente(
            cliente_seleccionado,
            entry_nombre.get(),
            entry_apellido.get(),
            entry_rut.get(),
            entry_telefono.get()
        )

        cargar_clientes()

    def eliminar():

        seleccion = tabla.selection()

        if not seleccion:
            return

        valores = tabla.item(seleccion[0])["values"]

        id_cliente = valores[0]

        eliminar_cliente(id_cliente)

        cargar_clientes()

    tk.Button(
        ventana_clientes,
        text="Guardar Cliente",
        command=guardar
    ).pack(pady=10)

    #Tabla de clientes
    tabla = ttk.Treeview(
        ventana_clientes,
        columns=("ID", "Nombre", "Apellido", "RUT", "Telefono"),
        show="headings"
    )

    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Apellido", text="Apellido")
    tabla.heading("RUT", text="RUT")
    tabla.heading("Telefono", text="Teléfono")

    tabla.pack(fill="both", expand=True)

    tabla.bind(
        "<<TreeviewSelect>>",
        seleccionar_cliente
    )

    def cargar_clientes():

        for fila in tabla.get_children():
            tabla.delete(fila)

        clientes = obtener_clientes()

        for cliente in clientes:
            tabla.insert("", "end", values=cliente)

    cargar_clientes()
    
    tk.Button(
        ventana_clientes,
        text="Eliminar Cliente",
        command=eliminar
    ).pack(pady=5)

    tk.Button(
        ventana_clientes,
        text="Actualizar Cliente",
        command=editar
    ).pack(pady=5)


#CRUD Clientes SQL
def guardar_cliente(nombre,apellido, rut, telefono):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO cliente(nombre, apellido, rut, telefono)
        VALUES (%s, %s, %s, %s)
    """, (nombre, apellido, rut, telefono))

    conn.commit()

    cur.close()
    conn.close()

def obtener_clientes():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT id_cliente, nombre, apellido, rut, telefono
        FROM cliente
        ORDER BY id_cliente
    """)

    clientes = cur.fetchall()

    cur.close()
    conn.close()

    return clientes

def eliminar_cliente(id_cliente):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM cliente
        WHERE id_cliente = %s
    """, (id_cliente,))

    conn.commit()

    cur.close()
    conn.close()

def actualizar_cliente(id_cliente, nombre, apellido, rut, telefono):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        UPDATE cliente
        SET nombre = %s,
            apellido = %s,
            rut = %s,
            telefono = %s
        WHERE id_cliente = %s
    """, (nombre, apellido, rut, telefono, id_cliente))

    conn.commit()

    cur.close()
    conn.close()