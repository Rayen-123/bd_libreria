import tkinter as tk
from tkinter import ttk
from database import conectar


def obtener_empleados():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id_empleado,
            nombre,
            apellido,
            rut,
            rol,
            tipo_turno
        FROM empleado
        ORDER BY id_empleado
    """)

    empleados = cur.fetchall()

    cur.close()
    conn.close()

    return empleados


def abrir_empleados():

    ventana = tk.Toplevel()

    ventana.title("Empleados")
    ventana.geometry("900x500")

    tk.Label(
        ventana,
        text="Listado de Empleados",
        font=("Arial", 16)
    ).pack(pady=10)

    tabla = ttk.Treeview(
        ventana,
        columns=(
            "ID",
            "Nombre",
            "Apellido",
            "RUT",
            "Rol",
            "Turno"
        ),
        show="headings"
    )

    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Apellido", text="Apellido")
    tabla.heading("RUT", text="RUT")
    tabla.heading("Rol", text="Rol")
    tabla.heading("Turno", text="Turno")

    tabla.pack(
        fill="both",
        expand=True,
        pady=10
    )

    empleados = obtener_empleados()

    for empleado in empleados:

        tabla.insert(
            "",
            "end",
            values=empleado
        )