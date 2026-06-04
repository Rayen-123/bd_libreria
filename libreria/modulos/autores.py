import tkinter as tk
from tkinter import ttk
from database import conectar

def abrir_autores():

    ventana_autores = tk.Toplevel()

    ventana_autores.title("Autores")
    ventana_autores.geometry("1100x600")

    tk.Label(
        ventana_autores,
        text="Gestión de Autores",
        font=("Arial", 16)
    ).pack(pady=10)

    #Formulario
    frame_form = tk.Frame(ventana_autores)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="Nombre").grid(row=0, column=0)

    entry_nombre = tk.Entry(frame_form)
    entry_nombre.grid(row=0, column=1)

    tk.Label(frame_form, text="Apellido").grid(row=1, column=0)

    entry_apellido = tk.Entry(frame_form)
    entry_apellido.grid(row=1, column=1)

    tk.Label(frame_form, text="Nacionalidad").grid(row=2, column=0)

    entry_nacionalidad = tk.Entry(frame_form)
    entry_nacionalidad.grid(row=2, column=1)

    autor_seleccionado = None

    #CRUD Autores
    def cargar_Autores():

        for fila in tabla.get_children():
            tabla.delete(fila)

        Autores = obtener_Autores()

        for autor in Autores:
            tabla.insert("", "end", values=autor)

    def seleccionar_autor(event):

        nonlocal autor_seleccionado

        seleccion = tabla.selection()

        if not seleccion:
            return

        valores = tabla.item(seleccion[0])["values"]

        autor_seleccionado = valores[0]

        entry_nombre.delete(0, tk.END)
        entry_apellido.delete(0, tk.END)
        entry_nacionalidad.delete(0, tk.END)

        entry_nombre.insert(0, valores[1])
        entry_apellido.insert(0, valores[2])
        entry_nacionalidad.insert(0, valores[3])

    def guardar():

        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        nacionalidad = entry_nacionalidad.get()

        guardar_autor(
            nombre,
            apellido,
            nacionalidad
        )

        cargar_Autores()

        entry_nombre.delete(0, tk.END)
        entry_apellido.delete(0, tk.END)
        entry_nacionalidad.delete(0, tk.END)

        print("Autor guardado")
        
    def editar():

        if autor_seleccionado is None:
            return

        actualizar_autor(
            autor_seleccionado,
            entry_nombre.get(),
            entry_apellido.get(),
            entry_nacionalidad.get(),
        )

        cargar_Autores()

    def eliminar():

        seleccion = tabla.selection()

        if not seleccion:
            return

        valores = tabla.item(seleccion[0])["values"]

        id_autor = valores[0]

        eliminar_autor(id_autor)

        cargar_Autores()

    tk.Button(
        ventana_autores,
        text="Guardar Autor",
        command=guardar
    ).pack(pady=10)

    #Tabla de Autores
    tabla = ttk.Treeview(
        ventana_autores,
        columns=("ID", "Nombre", "Apellido", "Nacionalidad"),
        show="headings"
    )

    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Apellido", text="Apellido")
    tabla.heading("Nacionalidad", text="Nacionalidad")

    tabla.pack(fill="both", expand=True)

    tabla.bind(
        "<<TreeviewSelect>>",
        seleccionar_autor
    )

    def cargar_Autores():

        for fila in tabla.get_children():
            tabla.delete(fila)

        Autores = obtener_Autores()

        for autor in Autores:
            tabla.insert("", "end", values=autor)

    cargar_Autores()
    
    tk.Button(
        ventana_autores,
        text="Eliminar Autor",
        command=eliminar
    ).pack(pady=5)

    tk.Button(
        ventana_autores,
        text="Actualizar Autor",
        command=editar
    ).pack(pady=5)


#CRUD Autores SQL
def guardar_autor(nombre,apellido, nacionalidad):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO autor(nombre, apellido, nacionalidad)
        VALUES (%s, %s, %s)
    """, (nombre, apellido, nacionalidad,))

    conn.commit()

    cur.close()
    conn.close()

def obtener_Autores():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT id_autor, nombre, apellido, nacionalidad
        FROM autor
        ORDER BY id_autor
    """)

    Autores = cur.fetchall()

    cur.close()
    conn.close()

    return Autores

def eliminar_autor(id_autor):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM autor
        WHERE id_autor = %s
    """, (id_autor))

    conn.commit()

    cur.close()
    conn.close()

def actualizar_autor(id_autor, nombre, apellido, nacionalidad):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        UPDATE autor
        SET nombre = %s,
            apellido = %s,
            nacionalidad = %s,
        WHERE id_autor = %s
    """, (nombre, apellido, nacionalidad, id_autor))

    conn.commit()

    cur.close()
    conn.close()