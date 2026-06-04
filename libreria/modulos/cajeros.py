import tkinter as tk
from tkinter import ttk
from database import conectar


def obtener_cajeros():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            c.id_cajero,
            e.nombre,
            e.apellido,
            e.rut
        FROM cajero c
        JOIN empleado e
            ON c.id_empleado = e.id_empleado
        ORDER BY c.id_cajero
    """)

    cajeros = cur.fetchall()

    cur.close()
    conn.close()

    return cajeros


def abrir_cajeros():

    ventana = tk.Toplevel()

    ventana.title("Cajeros")
    ventana.geometry("800x500")

    tk.Label(
        ventana,
        text="Listado de Cajeros",
        font=("Arial", 16)
    ).pack(pady=10)

    tabla = ttk.Treeview(
        ventana,
        columns=(
            "ID",
            "Nombre",
            "Apellido",
            "RUT"
        ),
        show="headings"
    )

    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Apellido", text="Apellido")
    tabla.heading("RUT", text="RUT")

    tabla.pack(
        fill="both",
        expand=True,
        pady=10
    )

    cajeros = obtener_cajeros()

    for cajero in cajeros:

        tabla.insert(
            "",
            "end",
            values=cajero
        )