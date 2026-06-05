import tkinter as tk
from tkinter import ttk
from database import conectar
from modulos._theme import *

def obtener_cajeros():
    conn=conectar(); cur=conn.cursor()
    cur.execute("SELECT c.id_cajero,e.nombre,e.apellido,e.rut FROM cajero c JOIN empleado e ON c.id_empleado=e.id_empleado ORDER BY c.id_cajero")
    r=cur.fetchall(); cur.close(); conn.close(); return r

def abrir_cajeros():
    win = tk.Toplevel()
    win.title("Cajeros"); win.geometry("800x480"); win.configure(bg=BG)
    header(win,"CAJEROS","Listado de cajeros")
    tabla = scrollable_table(win,("ID","Nombre","Apellido","RUT"),
                             [70,200,200,180],name="Caj",accent=SUBTEXT)
    for c in obtener_cajeros(): tabla.insert("","end",values=c)