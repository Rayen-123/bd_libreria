import tkinter as tk
from tkinter import ttk
from database import conectar

def abrir_editoriales():

    ventana_editoriales = tk.Toplevel()

    ventana_editoriales.title("Editoriales")
    ventana_editoriales.geometry("1100x600")

    tk.Label(
        ventana_editoriales,
        text="Gestión de Editoriales",
        font=("Arial", 16)
    ).pack(pady=10)

    #Formulario
    frame_form = tk.Frame(ventana_editoriales)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="Nombre").grid(row=0, column=0)

    entry_nombre = tk.Entry(frame_form)
    entry_nombre.grid(row=0, column=1)

    tk.Label(frame_form, text="País").grid(row=1, column=0)

    entry_pais = tk.Entry(frame_form)
    entry_pais.grid(row=1, column=1)

    tk.Label(frame_form, text="Teléfono").grid(row=2, column=0)

    entry_telefono = tk.Entry(frame_form)
    entry_telefono.grid(row=2, column=1)

    tk.Label(frame_form, text="Correo").grid(row=3, column=0)

    entry_correo = tk.Entry(frame_form)
    entry_correo.grid(row=3, column=1)

    editorial_seleccionado = None

    #CRUD editoriales
    def cargar_editoriales():

        for fila in tabla.get_children():
            tabla.delete(fila)

        editoriales = obtener_editoriales()

        for editorial in editoriales:
            tabla.insert("", "end", values=editorial)

    def seleccionar_editorial(event):

        nonlocal editorial_seleccionado

        seleccion = tabla.selection()

        if not seleccion:
            return

        valores = tabla.item(seleccion[0])["values"]

        editorial_seleccionado = valores[0]

        entry_nombre.delete(0, tk.END)
        entry_pais.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)
        entry_correo.delete(0, tk.END)

        entry_nombre.insert(0, valores[1])
        entry_pais.insert(0, valores[2])
        entry_telefono.insert(0, valores[3])
        entry_correo.insert(0, valores[4])

    def guardar():

        nombre = entry_nombre.get()
        pais = entry_pais.get()
        telefono = entry_telefono.get()
        correo = entry_correo.get()

        guardar_editorial(
            nombre,
            pais,
            telefono,
            correo
        )

        cargar_editoriales()

        entry_nombre.delete(0, tk.END)
        entry_pais.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)
        entry_correo.delete(0, tk.END)

        print("editorial guardado")
        
    def editar():

        if editorial_seleccionado is None:
            return

        actualizar_editorial(
            editorial_seleccionado,
            entry_nombre.get(),
            entry_pais.get(),
            entry_telefono.get(),
            entry_correo.get(),
        )

        cargar_editoriales()

    def eliminar():

        seleccion = tabla.selection()

        if not seleccion:
            return

        valores = tabla.item(seleccion[0])["values"]

        id_editorial = valores[0]

        eliminar_editorial(id_editorial)

        cargar_editoriales()

    tk.Button(
        ventana_editoriales,
        text="Guardar editorial",
        command=guardar
    ).pack(pady=10)

    #Tabla de editoriales
    tabla = ttk.Treeview(
        ventana_editoriales,
        columns=("ID", "Nombre", "Pais", "Telefono", "Correo"),
        show="headings"
    )

    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Pais", text="País")
    tabla.heading("Telefono", text="Teléfono")
    tabla.heading("Correo", text="Correo")

    tabla.pack(fill="both", expand=True)

    tabla.bind(
        "<<TreeviewSelect>>",
        seleccionar_editorial
    )

    def cargar_editoriales():

        for fila in tabla.get_children():
            tabla.delete(fila)

        editoriales = obtener_editoriales()

        for editorial in editoriales:
            tabla.insert("", "end", values=editorial)

    cargar_editoriales()
    
    tk.Button(
        ventana_editoriales,
        text="Eliminar editorial",
        command=eliminar
    ).pack(pady=5)

    tk.Button(
        ventana_editoriales,
        text="Actualizar editorial",
        command=editar
    ).pack(pady=5)


#CRUD editoriales SQL
def guardar_editorial(nombre, pais, telefono, correo):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO editorial(nombre, pais, telefono, correo)
        VALUES (%s, %s, %s, %s)
    """, (nombre, pais, telefono, correo,))

    conn.commit()

    cur.close()
    conn.close()

def obtener_editoriales():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT id_editorial, nombre, pais, telefono, correo
        FROM editorial
        ORDER BY id_editorial
    """)

    editoriales = cur.fetchall()

    cur.close()
    conn.close()

    return editoriales

def eliminar_editorial(id_editorial):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM editorial
        WHERE id_editorial = %s
    """, (id_editorial,))

    conn.commit()

    cur.close()
    conn.close()

def actualizar_editorial(id_editorial, nombre, pais, telefono, correo):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        UPDATE editorial
        SET nombre = %s,
            pais = %s,
            telefono = %s,
            correo = %s
        WHERE id_editorial = %s
    """, (nombre, pais, telefono, correo, id_editorial))

    conn.commit()

    cur.close()
    conn.close()