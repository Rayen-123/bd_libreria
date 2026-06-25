import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
from modulos._theme import *

def abrir_productos():
    win = tk.Toplevel()
    win.title("Gestión de Productos"); win.geometry("800x580"); win.configure(bg=BG)
    header(win, "PRODUCTOS", "Inventario de artículos y libros")

    form = tk.Frame(win, bg=PANEL, pady=12, padx=10)
    form.pack(fill="x", padx=20, pady=10)
    lbl(form,"Nombre",0,0);    e_nombre = entry(form,0,1,32)
    lbl(form,"Precio ($)",0,2); e_precio = entry(form,0,3,16)

    prod_sel = [None]
    def limpiar(): e_nombre.delete(0,tk.END); e_precio.delete(0,tk.END); prod_sel.__setitem__(0,None)

    tabla = scrollable_table(win,("ID","Nombre","Precio"),[60,420,130],name="Prod",accent=BLUE)

    def cargar():
        for r in tabla.get_children(): tabla.delete(r)
        for p in obtener_productos(): tabla.insert("","end",values=p)

    def seleccionar(event):
        sel = tabla.selection()
        if not sel: return
        v = tabla.item(sel[0])["values"]
        prod_sel[0]=v[0]; e_nombre.delete(0,tk.END); e_nombre.insert(0,v[1])
        e_precio.delete(0,tk.END); e_precio.insert(0,v[2])

    tabla.bind("<<TreeviewSelect>>",seleccionar)

    def guardar():
        if not e_nombre.get() or not e_precio.get():
            messagebox.showwarning("Faltan datos","Nombre y precio son obligatorios.",parent=win); return
        if guardar_producto(e_nombre.get(),e_precio.get()): cargar(); limpiar()

    def editar():
        if not prod_sel[0]:
            messagebox.showwarning("Sin selección","Selecciona un producto.",parent=win); return
        if actualizar_producto(prod_sel[0],e_nombre.get(),e_precio.get()): cargar()

    def eliminar():
        sel = tabla.selection()
        if not sel:
            messagebox.showwarning("Sin selección","Selecciona un producto.",parent=win); return
        v = tabla.item(sel[0])["values"]
        if messagebox.askyesno("Confirmar",f"¿Eliminar '{v[1]}'?",parent=win):
            if eliminar_producto(v[0]): cargar(); limpiar()

    bf = tk.Frame(win,bg=BG); bf.pack(pady=10)
    btn(bf,"+ Guardar",  guardar,  BLUE).pack(side="left",padx=6)
    btn(bf,"Actualizar",editar,   ACCENT).pack(side="left",padx=6)
    btn(bf,"x Eliminar",  eliminar, RED).pack(side="left",padx=6)
    btn(bf,"Limpiar",   limpiar,  SUBTEXT,12).pack(side="left",padx=6)
    cargar()

def guardar_producto(nombre,precio):
    try:
        conn=conectar(); cur=conn.cursor()
        cur.execute("INSERT INTO producto(nombre,precio) VALUES(%s,%s)",(nombre,precio))
        conn.commit(); cur.close(); conn.close(); return True
    except Exception as e:
        conn.rollback(); messagebox.showerror("Error",str(e)); return False

def obtener_productos():
    conn=conectar(); cur=conn.cursor()
    cur.execute("SELECT id_producto,nombre,precio FROM producto ORDER BY id_producto")
    r=cur.fetchall(); cur.close(); conn.close(); return r

def eliminar_producto(id_producto):
    try:
        conn=conectar(); cur=conn.cursor()
        cur.execute("DELETE FROM producto WHERE id_producto=%s",(id_producto,))
        conn.commit(); cur.close(); conn.close(); return True
    except Exception as e:
        conn.rollback(); messagebox.showerror("Error",f"No se puede eliminar: {e}"); return False

def actualizar_producto(id_producto,nombre,precio):
    try:
        conn=conectar(); cur=conn.cursor()
        cur.execute("UPDATE producto SET nombre=%s,precio=%s WHERE id_producto=%s",(nombre,precio,id_producto))
        conn.commit(); cur.close(); conn.close(); return True
    except Exception as e:
        conn.rollback(); messagebox.showerror("Error",str(e)); return False