import tkinter as tk
from tkinter import ttk
from database import conectar

def obtener_autores():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT id_autor, nombre, apellido
        FROM autor
        ORDER BY nombre
    """)

    autores = cur.fetchall()

    cur.close()
    conn.close()

    return autores

def obtener_categorias():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT id_categoria, tipo
        FROM categoria
        ORDER BY tipo
    """)

    categorias = cur.fetchall()

    cur.close()
    conn.close()

    return categorias

def obtener_editoriales():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT id_editorial, nombre
        FROM editorial
        ORDER BY nombre
    """)

    editoriales = cur.fetchall()

    cur.close()
    conn.close()

    return editoriales

def obtener_sagas():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT id_saga, nombre
        FROM sagas
        ORDER BY nombre
    """)

    sagas = cur.fetchall()

    cur.close()
    conn.close()

    return sagas

def guardar_libro(titulo,precio,id_autor,id_categoria,id_editorial,id_saga,anio,estante):

    conn = conectar()
    cur = conn.cursor()

    # Crear producto
    cur.execute("""
        INSERT INTO producto(nombre, precio)
        VALUES (%s, %s)
        RETURNING id_producto
    """, (
        titulo,
        precio
    ))

    id_producto = cur.fetchone()[0]

    # Crear libro
    cur.execute("""
        INSERT INTO libro(
            id_autor,
            id_categoria,
            id_editorial,
            id_saga,
            titulo,
            anio_publicacion,
            precio,
            estante,
            id_producto
        )
        VALUES(
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
    """, (
        id_autor,
        id_categoria,
        id_editorial,
        id_saga,
        titulo,
        anio,
        precio,
        estante,
        id_producto
    ))

    conn.commit()

    cur.close()
    conn.close()

def obtener_libros():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            l.id_libro,
            l.titulo,
            l.precio,
            l.anio_publicacion,
            l.estante,
            l.id_autor,
            l.id_categoria,
            l.id_editorial,
            l.id_saga,
            a.nombre || ' ' || a.apellido,
            c.tipo
        FROM libro l
        JOIN autor a
            ON l.id_autor = a.id_autor
        JOIN categoria c
            ON l.id_categoria = c.id_categoria
        ORDER BY l.id_libro
    """)

    libros = cur.fetchall()

    cur.close()
    conn.close()

    return libros

def abrir_libros():

    ventana_libros = tk.Toplevel()

    ventana_libros.title("Libros")
    ventana_libros.geometry("1200x700")

    tk.Label(
        ventana_libros,
        text="Gestión de Libros",
        font=("Arial", 16)
    ).pack(pady=10)

    #Formulario
    frame_form = tk.Frame(ventana_libros)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="Título").grid(row=0, column=0)

    entry_titulo = tk.Entry(frame_form, width=30)
    entry_titulo.grid(row=0, column=1)

    tk.Label(frame_form, text="Precio").grid(row=1, column=0)

    entry_precio = tk.Entry(frame_form)
    entry_precio.grid(row=1, column=1)

    tk.Label(frame_form, text="Año Publicación").grid(row=2, column=0)

    entry_anio = tk.Entry(frame_form)
    entry_anio.grid(row=2, column=1)

    tk.Label(frame_form, text="Estante").grid(row=3, column=0)

    entry_estante = tk.Entry(frame_form)
    entry_estante.grid(row=3, column=1)

    tk.Label(frame_form, text="Autor").grid(row=0, column=2)

    combo_autor = ttk.Combobox(
        frame_form,
        width=30
    )

    combo_autor.grid(row=0, column=3)

    autores = obtener_autores()

    combo_autor["values"] = [
        f"{autor[0]} - {autor[1]} {autor[2]}"
        for autor in autores
    ]

    #Categoria
    tk.Label(frame_form, text="Categoría").grid(row=1, column=2)

    combo_categoria = ttk.Combobox(
        frame_form,
        width=30
    )

    combo_categoria.grid(row=1, column=3)

    categorias = obtener_categorias()

    combo_categoria["values"] = [
        f"{categoria[0]} - {categoria[1]}"
        for categoria in categorias
    ]

    #Editorial
    tk.Label(frame_form, text="Editorial").grid(row=2, column=2)

    combo_editorial = ttk.Combobox(
        frame_form,
        width=30
    )

    combo_editorial.grid(row=2, column=3)

    editoriales = obtener_editoriales()

    combo_editorial["values"] = [
        f"{editorial[0]} - {editorial[1]}"
        for editorial in editoriales
    ]

    #Saga
    tk.Label(frame_form, text="Saga").grid(row=3, column=2)

    combo_saga = ttk.Combobox(
        frame_form,
        width=30
    )

    combo_saga.grid(row=3, column=3)

    sagas = obtener_sagas()

    combo_saga["values"] = [
        f"{saga[0]} - {saga[1]}"
        for saga in sagas
    ]

    libro_seleccionado = None
    datos_libro = None

    #Tabla
    tabla = ttk.Treeview(
        ventana_libros,
        columns=(
            "ID",
            "Titulo",
            "Precio",
            "Autor",
            "Categoria"
        ),
        show="headings"
    )

    tabla.heading("ID", text="ID")
    tabla.heading("Titulo", text="Título")
    tabla.heading("Precio", text="Precio")
    tabla.heading("Autor", text="Autor")
    tabla.heading("Categoria", text="Categoría")

    tabla.pack(
        fill="both",
        expand=True,
        pady=10
    )

    def seleccionar_libro(event):

        nonlocal libro_seleccionado
        nonlocal datos_libro

        seleccion = tabla.selection()

        if not seleccion:
            return

        id_libro = tabla.item(
            seleccion[0]
        )["values"][0]

        libros = obtener_libros()

        datos_libro = next(
            libro for libro in libros
            if libro[0] == id_libro
        )

        libro_seleccionado = datos_libro[0]

        entry_titulo.delete(0, tk.END)
        entry_precio.delete(0, tk.END)
        entry_anio.delete(0, tk.END)
        entry_estante.delete(0, tk.END)

        entry_titulo.insert(0, datos_libro[1])
        entry_precio.insert(0, datos_libro[2])
        entry_anio.insert(0, datos_libro[3])
        entry_estante.insert(0, datos_libro[4])

        # Autor
        for autor in autores:
            if autor[0] == datos_libro[5]:
                combo_autor.set(
                    f"{autor[0]} - {autor[1]} {autor[2]}"
                )
                break

        # Categoría
        for categoria in categorias:
            if categoria[0] == datos_libro[6]:
                combo_categoria.set(
                    f"{categoria[0]} - {categoria[1]}"
                )
                break

        # Editorial
        for editorial in editoriales:
            if editorial[0] == datos_libro[7]:
                combo_editorial.set(
                    f"{editorial[0]} - {editorial[1]}"
                )
                break

        # Saga
        for saga in sagas:
            if saga[0] == datos_libro[8]:
                combo_saga.set(
                    f"{saga[0]} - {saga[1]}"
                )
                break
    
    tabla.bind(
        "<<TreeviewSelect>>",
        seleccionar_libro
    )

    def cargar_libros():

        for fila in tabla.get_children():
            tabla.delete(fila)

        libros = obtener_libros()

        for libro in libros:

            tabla.insert(
                "",
                "end",
                values=(
                    libro[0],   # ID
                    libro[1],   # Titulo
                    libro[2],   # Precio
                    libro[9],   # Autor
                    libro[10]   # Categoria
                )
            )

    def guardar():

        id_autor = int(
            combo_autor.get().split(" - ")[0]
        )

        id_categoria = int(
            combo_categoria.get().split(" - ")[0]
        )

        id_editorial = int(
            combo_editorial.get().split(" - ")[0]
        )

        id_saga = int(
            combo_saga.get().split(" - ")[0]
        )

        guardar_libro(
            entry_titulo.get(),
            float(entry_precio.get()),
            id_autor,
            id_categoria,
            id_editorial,
            id_saga,
            int(entry_anio.get()),
            entry_estante.get()
        )

        cargar_libros()

        entry_titulo.delete(0, tk.END)
        entry_precio.delete(0, tk.END)
        entry_anio.delete(0, tk.END)
        entry_estante.delete(0, tk.END)

        combo_autor.set("")
        combo_categoria.set("")
        combo_editorial.set("")
        combo_saga.set("")

    tk.Button(
        ventana_libros,
        text="Guardar Libro",
        command=guardar
    ).pack(pady=10)

    cargar_libros()

    def editar():

        if libro_seleccionado is None:
            return

        actualizar_libro(
            libro_seleccionado,
            entry_titulo.get(),
            float(entry_precio.get())
        )

        cargar_libros()
    
    tk.Button(
        ventana_libros,
        text="Editar Libro",
        command=editar
    ).pack(pady=5)

    def eliminar():

        seleccion = tabla.selection()

        if not seleccion:
            return

        valores = tabla.item(
            seleccion[0]
        )["values"]

        id_libro = valores[0]

        eliminar_libro(id_libro)

        cargar_libros()

    tk.Button(
        ventana_libros,
        text="Eliminar Libro",
        command=eliminar
    ).pack(pady=5)


def actualizar_libro(id_libro,titulo,precio):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        UPDATE libro
        SET titulo = %s,
            precio = %s
        WHERE id_libro = %s
    """, (
        titulo,
        precio,
        id_libro
    ))

    conn.commit()

    cur.close()
    conn.close()

def eliminar_libro(id_libro):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM libro
        WHERE id_libro = %s
    """, (id_libro,))

    conn.commit()

    cur.close()
    conn.close()