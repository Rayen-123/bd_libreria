import tkinter as tk
from tkinter import ttk
from database import conectar

def abrir_categorias():

    ventana_categorias = tk.Toplevel()

    ventana_categorias.title("Categorias")
    ventana_categorias.geometry("1100x600")

    tk.Label(
        ventana_categorias,
        text="Gestión de Categorias",
        font=("Arial", 16)
    ).pack(pady=10)

    #Formulario
    frame_form = tk.Frame(ventana_categorias)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="Tipo").grid(row=0, column=0)

    entry_tipo = tk.Entry(frame_form)
    entry_tipo.grid(row=0, column=1)

    categoria_seleccionada = None

    #CRUD categorias
    def cargar_categorias():

        for fila in tabla.get_children():
            tabla.delete(fila)

        categorias = obtener_categorias()

        for categoria in categorias:
            tabla.insert("", "end", values=categoria)

    def seleccionar_categoria(event):

        nonlocal categoria_seleccionada

        seleccion = tabla.selection()

        if not seleccion:
            return

        valores = tabla.item(seleccion[0])["values"]

        categoria_seleccionada = valores[0]

        entry_tipo.delete(0, tk.END)

        entry_tipo.insert(0, valores[1])

    def guardar():

        tipo = entry_tipo.get()

        guardar_categoria(tipo)

        cargar_categorias()

        entry_tipo.delete(0, tk.END)

        print("Categoria guardada")
        
    def editar():

        if categoria_seleccionada is None:
            return

        actualizar_categoria(
            categoria_seleccionada,
            entry_tipo.get(),
        )

        cargar_categorias()

    def eliminar():

        seleccion = tabla.selection()

        if not seleccion:
            return

        valores = tabla.item(seleccion[0])["values"]

        id_categoria = valores[0]

        eliminar_categoria(id_categoria)

        cargar_categorias()

    tk.Button(
        ventana_categorias,
        text="Guardar categoria",
        command=guardar
    ).pack(pady=10)

    #Tabla de categorias
    tabla = ttk.Treeview(
        ventana_categorias,
        columns=("ID", "Tipo"),
        show="headings"
    )

    tabla.heading("ID", text="ID")
    tabla.heading("Tipo", text="Tipo")

    tabla.pack(fill="both", expand=True)

    tabla.bind(
        "<<TreeviewSelect>>",
        seleccionar_categoria
    )

    def cargar_categorias():

        for fila in tabla.get_children():
            tabla.delete(fila)

        categorias = obtener_categorias()

        for categoria in categorias:
            tabla.insert("", "end", values=categoria)

    cargar_categorias()
    
    tk.Button(
        ventana_categorias,
        text="Eliminar categoria",
        command=eliminar
    ).pack(pady=5)

    tk.Button(
        ventana_categorias,
        text="Actualizar categoria",
        command=editar
    ).pack(pady=5)


#CRUD categorias SQL
def guardar_categoria(tipo):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO categoria(tipo)
        VALUES (%s)
    """, (tipo,))

    conn.commit()

    cur.close()
    conn.close()

def obtener_categorias():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT id_categoria, tipo
        FROM categoria
        ORDER BY id_categoria
    """)

    categorias = cur.fetchall()

    cur.close()
    conn.close()

    return categorias

def eliminar_categoria(id_categoria):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM categoria
        WHERE id_categoria = %s
    """, (id_categoria))

    conn.commit()

    cur.close()
    conn.close()

def actualizar_categoria(id_categoria, tipo):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        UPDATE categoria
        SET tipo = %s,
        WHERE id_categoria = %s
    """, (id_categoria, tipo))

    conn.commit()

    cur.close()
    conn.close()