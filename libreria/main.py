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
from modulos.empleados import abrir_empleados
from modulos.cajeros import abrir_cajeros

ventana = tk.Tk()

ventana.title("Sistema Librería")
ventana.geometry("800x600")

def abrir_inventario():

    ventana_inventario = tk.Toplevel()

    ventana_inventario.title("Inventario")
    ventana_inventario.geometry("300x350")

    tk.Label(
        ventana_inventario,
        text="Inventario",
        font=("Arial", 14)
    ).pack(pady=10)

    tk.Button(
        ventana_inventario,
        text="Libros",
        width=20,
        command=abrir_libros
    ).pack(pady=5)

    tk.Button(
        ventana_inventario,
        text="Productos",
        width=20,
        command=abrir_productos
    ).pack(pady=5)

    tk.Button(
        ventana_inventario,
        text="Autores",
        width=20,
        command=abrir_autores
    ).pack(pady=5)

    tk.Button(
        ventana_inventario,
        text="Categorías",
        width=20,
        command=abrir_categorias
    ).pack(pady=5)

    tk.Button(
        ventana_inventario,
        text="Editoriales",
        width=20,
        command=abrir_editoriales
    ).pack(pady=5)

    tk.Button(
        ventana_inventario,
        text="Sagas",
        width=20,
        command=abrir_sagas
    ).pack(pady=5)

def abrir_menu_ventas():

    ventana_ventas = tk.Toplevel()

    ventana_ventas.title("Ventas")
    ventana_ventas.geometry("300x200")

    tk.Label(
        ventana_ventas,
        text="Ventas",
        font=("Arial", 14)
    ).pack(pady=10)

    tk.Button(
        ventana_ventas,
        text="Nueva Venta",
        width=20,
        command=abrir_ventas
    ).pack(pady=5)

    tk.Button(
        ventana_ventas,
        text="Historial de Ventas",
        width=20,
        command=abrir_historial_ventas
    ).pack(pady=5)

def abrir_personal():

    ventana_personal = tk.Toplevel()

    ventana_personal.title("Personal")
    ventana_personal.geometry("300x200")

    tk.Label(
        ventana_personal,
        text="Personal",
        font=("Arial", 14)
    ).pack(pady=10)

    tk.Button(
        ventana_personal,
        text="Empleados",
        width=20,
        command=abrir_empleados
    ).pack(pady=5)

    tk.Button(
        ventana_personal,
        text="Cajeros",
        width=20,
        command=abrir_cajeros
    ).pack(pady=5)

titulo = tk.Label(
    ventana,
    text="Sistema de Gestión de Librería",
    font=("Arial", 18)
)

titulo.pack(pady=30)

tk.Button(
    ventana,
    text="Ventas",
    width=20,
    height=2,
    command=abrir_menu_ventas
).pack(pady=20)

frame_menu = tk.Frame(ventana)
frame_menu.pack(pady=20)

tk.Button(
    frame_menu,
    text="Inventario",
    width=20,
    height=2,
    command=abrir_inventario
).grid(
    row=0,
    column=0,
    padx=40,
    pady=15
)

tk.Button(
    frame_menu,
    text="Clientes",
    width=20,
    height=2,
    command=abrir_clientes
).grid(
    row=0,
    column=1,
    padx=40,
    pady=15
)

tk.Button(
    frame_menu,
    text="Reportes",
    width=20,
    height=2,
    command=abrir_menu_reportes
).grid(
    row=1,
    column=0,
    padx=40,
    pady=15
)

tk.Button(
    frame_menu,
    text="Personal",
    width=20,
    height=2,
    command=abrir_personal
).grid(
    row=1,
    column=1,
    padx=40,
    pady=15
)

ventana.mainloop()