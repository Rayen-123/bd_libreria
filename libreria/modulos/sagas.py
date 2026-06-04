import tkinter as tk
from tkinter import ttk
from database import conectar

def abrir_sagas():

    ventana_sagas = tk.Toplevel()

    ventana_sagas.title("Sagas")
    ventana_sagas.geometry("1100x600")

    tk.Label(
        ventana_sagas,
        text="Gestión de Sagas",
        font=("Arial", 16)
    ).pack(pady=10)

    #Formulario
    frame_form = tk.Frame(ventana_sagas)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="Nombre").grid(row=0, column=0)

    entry_nombre = tk.Entry(frame_form)
    entry_nombre.grid(row=0, column=1)

    tk.Label(frame_form, text="Cantidad de libros").grid(row=1, column=0)

    entry_cantidad = tk.Entry(frame_form)
    entry_cantidad.grid(row=1, column=1)

    saga_seleccionado = None

    #CRUD sagas
    def cargar_sagas():

        for fila in tabla.get_children():
            tabla.delete(fila)

        sagas = obtener_sagas()

        for saga in sagas:
            tabla.insert("", "end", values=saga)

    def seleccionar_saga(event):

        nonlocal saga_seleccionado

        seleccion = tabla.selection()

        if not seleccion:
            return

        valores = tabla.item(seleccion[0])["values"]

        saga_seleccionado = valores[0]

        entry_nombre.delete(0, tk.END)
        entry_cantidad.delete(0, tk.END)

        entry_nombre.insert(0, valores[1])
        entry_cantidad.insert(0, valores[2])

    def guardar():

        nombre = entry_nombre.get()
        cantidad = entry_cantidad.get()

        guardar_saga(
            nombre,
            cantidad
        )

        cargar_sagas()

        entry_nombre.delete(0, tk.END)
        entry_cantidad.delete(0, tk.END)

        print("saga guardado")
        
    def editar():

        if saga_seleccionado is None:
            return

        actualizar_saga(
            saga_seleccionado,
            entry_nombre.get(),
            entry_cantidad.get(),
        )

        cargar_sagas()

    def eliminar():

        seleccion = tabla.selection()

        if not seleccion:
            return

        valores = tabla.item(seleccion[0])["values"]

        id_saga = valores[0]

        eliminar_saga(id_saga)

        cargar_sagas()

    tk.Button(
        ventana_sagas,
        text="Guardar saga",
        command=guardar
    ).pack(pady=10)

    #Tabla de sagas
    tabla = ttk.Treeview(
        ventana_sagas,
        columns=("ID", "Nombre", "Cantidad"),
        show="headings"
    )

    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Cantidad", text="Cantidad")

    tabla.pack(fill="both", expand=True)

    tabla.bind(
        "<<TreeviewSelect>>",
        seleccionar_saga
    )

    def cargar_sagas():

        for fila in tabla.get_children():
            tabla.delete(fila)

        sagas = obtener_sagas()

        for saga in sagas:
            tabla.insert("", "end", values=saga)

    cargar_sagas()
    
    tk.Button(
        ventana_sagas,
        text="Eliminar saga",
        command=eliminar
    ).pack(pady=5)

    tk.Button(
        ventana_sagas,
        text="Actualizar saga",
        command=editar
    ).pack(pady=5)


#CRUD sagas SQL
def guardar_saga(nombre,cantidad):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO sagas(nombre, cantidad_libros)
        VALUES (%s, %s)
    """, (nombre, cantidad))

    conn.commit()

    cur.close()
    conn.close()

def obtener_sagas():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT id_saga, nombre, cantidad_libros
        FROM sagas
        ORDER BY id_saga
    """)

    sagas = cur.fetchall()

    cur.close()
    conn.close()

    return sagas

def eliminar_saga(id_saga):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM sagas
        WHERE id_saga = %s
    """, (id_saga))

    conn.commit()

    cur.close()
    conn.close()

def actualizar_saga(id_saga, nombre, cantidad):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        UPDATE sagas
        SET nombre = %s,
            cantidad_libros = %s,
        WHERE id_saga = %s
    """, (nombre, cantidad, id_saga))

    conn.commit()

    cur.close()
    conn.close()