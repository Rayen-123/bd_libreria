import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
from modulos._theme import *

def abrir_clientes():
    win = tk.Toplevel()
    win.title("Gestión de Clientes"); win.geometry("1050x640"); win.configure(bg=BG)
    header(win, "CLIENTES", "Agregar · Editar · Eliminar")

    form = tk.Frame(win, bg=PANEL, pady=12, padx=10)
    form.pack(fill="x", padx=20, pady=10)
    lbl(form, "Nombre",   0, 0); e_nombre   = entry(form, 0, 1)
    lbl(form, "Apellido", 0, 2); e_apellido = entry(form, 0, 3)
    lbl(form, "RUT",      1, 0); e_rut      = entry(form, 1, 1)
    lbl(form, "Teléfono", 1, 2); e_telefono = entry(form, 1, 3)

    cliente_sel = [None]

    def limpiar():
        for e in [e_nombre, e_apellido, e_rut, e_telefono]: e.delete(0, tk.END)
        cliente_sel[0] = None

    tabla = scrollable_table(win, ("ID","Nombre","Apellido","RUT","Teléfono"),
                             [55,160,160,140,140], name="Cli")

    def cargar():
        for r in tabla.get_children(): tabla.delete(r)
        for c in obtener_clientes(): tabla.insert("","end",values=c)

    def seleccionar(event):
        sel = tabla.selection()
        if not sel: return
        v = tabla.item(sel[0])["values"]
        cliente_sel[0] = v[0]
        e_nombre.delete(0,tk.END);   e_nombre.insert(0,v[1])
        e_apellido.delete(0,tk.END); e_apellido.insert(0,v[2])
        e_rut.delete(0,tk.END);      e_rut.insert(0,v[3])
        e_telefono.delete(0,tk.END); e_telefono.insert(0,v[4])

    tabla.bind("<<TreeviewSelect>>", seleccionar)

    def guardar():
        n,a,r,t = e_nombre.get(),e_apellido.get(),e_rut.get(),e_telefono.get()
        if not n or not r:
            messagebox.showwarning("Faltan datos","Nombre y RUT son obligatorios.",parent=win); return
        if guardar_cliente(n,a,r,t): cargar(); limpiar()
            
    def editar():
        if not cliente_sel[0]:
            messagebox.showwarning("Sin selección","Selecciona un cliente.",parent=win); return
        if actualizar_cliente(cliente_sel[0],e_nombre.get(),e_apellido.get(),e_rut.get(),e_telefono.get()):
            cargar(); messagebox.showinfo("","Cliente actualizado.",parent=win)

    def eliminar():
        sel = tabla.selection()
        if not sel:
            messagebox.showwarning("Sin selección","Selecciona un cliente.",parent=win); return
        v = tabla.item(sel[0])["values"]
        if messagebox.askyesno("Confirmar",f"¿Eliminar a {v[1]} {v[2]}?",parent=win):
            if eliminar_cliente(v[0]): cargar(); limpiar()

    bf = tk.Frame(win, bg=BG); bf.pack(pady=10)
    btn(bf,"+ Guardar",  guardar,  ACCENT).pack(side="left",padx=6)
    btn(bf,"Actualizar",editar,   BLUE).pack(side="left",padx=6)
    btn(bf,"x Eliminar",  eliminar, RED).pack(side="left",padx=6)
    btn(bf,"Limpiar",   limpiar,  SUBTEXT,12).pack(side="left",padx=6)
    cargar()

def guardar_cliente(nombre,apellido,rut,telefono):
    try:
        conn=conectar(); cur=conn.cursor()
        cur.execute("INSERT INTO cliente(nombre,apellido,rut,telefono) VALUES(%s,%s,%s,%s)",(nombre,apellido,rut,telefono))
        conn.commit(); cur.close(); conn.close(); return True
    except Exception as e:
        conn.rollback(); messagebox.showerror("Error",str(e)); return False

def obtener_clientes():
    conn=conectar(); cur=conn.cursor()
    cur.execute("SELECT id_cliente,nombre,apellido,rut,telefono FROM cliente ORDER BY id_cliente")
    r=cur.fetchall(); cur.close(); conn.close(); return r

def eliminar_cliente(id_cliente):
    try:
        conn=conectar(); cur=conn.cursor()
        cur.execute("DELETE FROM cliente WHERE id_cliente=%s",(id_cliente,))
        conn.commit(); cur.close(); conn.close(); return True
    except:
        conn.rollback()
        messagebox.showerror("Error","No se puede eliminar: el cliente tiene ventas registradas."); return False

def actualizar_cliente(id_cliente,nombre,apellido,rut,telefono):
    try:
        conn=conectar(); cur=conn.cursor()
        cur.execute("UPDATE cliente SET nombre=%s,apellido=%s,rut=%s,telefono=%s WHERE id_cliente=%s",(nombre,apellido,rut,telefono,id_cliente))
        conn.commit(); cur.close(); conn.close(); return True
    except Exception as e:
        conn.rollback(); messagebox.showerror("Error",str(e)); return False