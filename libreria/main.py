import tkinter as tk
from modulos.clientes import abrir_clientes
from modulos.productos import abrir_productos
from modulos.ventas import abrir_ventas
from modulos.libros import abrir_libros
from modulos.historial_ventas import abrir_historial_ventas
from modulos.autores import abrir_autores
from modulos.categorias import abrir_categorias
from modulos.editoriales import abrir_editoriales
from modulos.sagas import abrir_sagas
from modulos.reportes import abrir_menu_reportes

ventana = tk.Tk()

ventana.title("Sistema Librería")
ventana.geometry("800x600")

titulo = tk.Label(
    ventana,
    text="Sistema de Gestión de Librería",
    font=("Arial", 18)
)

titulo.pack(pady=20)

def abrir_inventario():

    ventana = tk.Toplevel()

    ventana.title("Inventario")
    ventana.geometry("300x300")

    tk.Label(
        ventana,
        text="Inventario",
        font=("Arial", 14)
    ).pack(pady=10)

    tk.Button(
        ventana,
        text="Libros",
        width=20,
        command=abrir_libros
    ).pack(pady=5)

    tk.Button(
        ventana,
        text="Productos",
        width=20,
        command=abrir_productos
    ).pack(pady=5)

    tk.Button(
        ventana,
        text="Autores",
        width=20,
        command=abrir_autores
    ).pack(pady=5)

    tk.Button(
        ventana,
        text="Categorías",
        width=20,
        command=abrir_categorias
    ).pack(pady=5)

    tk.Button(
        ventana,
        text="Editoriales",
        width=20,
        command=abrir_editoriales
    ).pack(pady=5)

    tk.Button(
        ventana,
        text="Sagas",
        width=20,
        command=abrir_sagas
    ).pack(pady=5)

def abrir_menu_ventas():

    ventana = tk.Toplevel()

    ventana.title("Ventas")
    ventana.geometry("300x200")

    tk.Label(
        ventana,
        text="Ventas",
        font=("Arial", 14)
    ).pack(pady=10)

    tk.Button(
        ventana,
        text="Nueva Venta",
        width=20,
        command=abrir_ventas
    ).pack(pady=5)

    tk.Button(
        ventana,
        text="Historial de Ventas",
        width=20,
        command=abrir_historial_ventas
    ).pack(pady=5)

def abrir_personal():

    ventana = tk.Toplevel()

    ventana.title("Personal")
    ventana.geometry("300x200")

    tk.Label(
        ventana,
        text="Personal",
        font=("Arial", 14)
    ).pack(pady=10)

    tk.Button(
        ventana,
        text="Empleados",
        width=20
    ).pack(pady=5)

    tk.Button(
        ventana,
        text="Cajeros",
        width=20
    ).pack(pady=5)


tk.Button(
    ventana,
    text="Inventario",
    width=20,
    command=abrir_inventario
).pack(pady=5)

tk.Button(
    ventana,
    text="Ventas",
    width=20,
    command=abrir_menu_ventas
).pack(pady=5)

tk.Button(
    ventana,
    text="Reportes",
    width=20,
    command=abrir_menu_reportes
).pack(pady=5)

tk.Button(
    ventana,
    text="Clientes",
    width=20,
    command=abrir_clientes
).pack(pady=5)

tk.Button(
    ventana,
    text="Personal",
    width=20,
    command=abrir_personal
).pack(pady=5)

ventana.mainloop()