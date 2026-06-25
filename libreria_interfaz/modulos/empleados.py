import tkinter as tk
from tkinter import ttk
from database import conectar
from modulos._theme import *

def obtener_empleados():
    conn=conectar(); cur=conn.cursor()
    cur.execute("SELECT id_empleado,nombre,apellido,rut,rol,tipo_turno FROM empleado ORDER BY id_empleado")
    r=cur.fetchall(); cur.close(); conn.close(); return r

def abrir_empleados():
    win = tk.Toplevel()
    win.title("Empleados"); win.geometry("950x520"); win.configure(bg=BG)
    header(win,"EMPLEADOS","Listado del personal")
    tabla = scrollable_table(win,("ID","Nombre","Apellido","RUT","Rol","Turno"),
                             [55,160,160,140,100,100],name="Emp",accent=SUBTEXT)
    for e in obtener_empleados(): tabla.insert("","end",values=e)