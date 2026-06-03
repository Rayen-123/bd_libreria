import tkinter as tk
from clientes import abrir_clientes
from productos import abrir_productos
from ventas import abrir_ventas
from libros import abrir_libros

ventana = tk.Tk()

ventana.title("Sistema Librería")
ventana.geometry("800x600")

titulo = tk.Label(
    ventana,
    text="Sistema de Gestión de Librería",
    font=("Arial", 18)
)

titulo.pack(pady=20)

tk.Button(
    ventana,
    text="Clientes",
    width=20,
    command=abrir_clientes
).pack(pady=10)

tk.Button(
    ventana,
    text="Productos",
    command=abrir_productos
).pack(pady=10)

tk.Button(
    ventana,
    text="Ventas",
    command=abrir_ventas
).pack(pady=10)

tk.Button(
    ventana,
    text="Libros",
    command=abrir_libros
).pack(pady=10)

ventana.mainloop()