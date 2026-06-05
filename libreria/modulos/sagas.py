import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
from modulos._theme import *

def abrir_sagas():
    win = tk.Toplevel()
    win.title("Sagas"); win.geometry("700x520"); win.configure(bg=BG)
    header(win,"SAGAS","Agregar · Editar · Eliminar")

    form = tk.Frame(win,bg=PANEL,pady=12,padx=10); form.pack(fill="x",padx=20,pady=10)
    lbl(form,"Nombre",0,0);             e_nombre   = entry(form,0,1,28)
    lbl(form,"Cantidad de libros",0,2); e_cantidad = entry(form,0,3,10)

    sel=[None]
    def limpiar(): e_nombre.delete(0,tk.END); e_cantidad.delete(0,tk.END); sel[0]=None

    tabla = scrollable_table(win,("ID","Nombre","Cantidad"),[60,360,120],name="Sag",accent=BLUE)

    def cargar():
        for r in tabla.get_children(): tabla.delete(r)
        for s in obtener_sagas(): tabla.insert("","end",values=s)

    def seleccionar(event):
        s=tabla.selection()
        if not s: return
        v=tabla.item(s[0])["values"]; sel[0]=v[0]
        e_nombre.delete(0,tk.END);   e_nombre.insert(0,v[1])
        e_cantidad.delete(0,tk.END); e_cantidad.insert(0,v[2])

    tabla.bind("<<TreeviewSelect>>",seleccionar)

    def guardar():
        if not e_nombre.get():
            messagebox.showwarning("Faltan datos","El nombre es obligatorio.",parent=win); return
        guardar_saga(e_nombre.get(),e_cantidad.get()); cargar(); limpiar()

    def editar():
        if not sel[0]:
            messagebox.showwarning("Sin selección","Selecciona una saga.",parent=win); return
        actualizar_saga(sel[0],e_nombre.get(),e_cantidad.get()); cargar()

    def eliminar():
        s=tabla.selection()
        if not s:
            messagebox.showwarning("Sin selección","Selecciona una saga.",parent=win); return
        v=tabla.item(s[0])["values"]
        if messagebox.askyesno("Confirmar",f"¿Eliminar '{v[1]}'?",parent=win):
            eliminar_saga(v[0]); cargar(); limpiar()

    bf=tk.Frame(win,bg=BG); bf.pack(pady=10)
    btn(bf,"+ Guardar",  guardar,  BLUE).pack(side="left",padx=6)
    btn(bf,"Actualizar",editar,   ACCENT).pack(side="left",padx=6)
    btn(bf,"x Eliminar",  eliminar, RED).pack(side="left",padx=6)
    btn(bf,"Limpiar",   limpiar,  SUBTEXT,12).pack(side="left",padx=6)
    cargar()

def guardar_saga(nombre,cantidad):
    conn=conectar(); cur=conn.cursor()
    cur.execute("INSERT INTO sagas(nombre,cantidad_libros) VALUES(%s,%s)",(nombre,cantidad))
    conn.commit(); cur.close(); conn.close()

def obtener_sagas():
    conn=conectar(); cur=conn.cursor()
    cur.execute("SELECT id_saga,nombre,cantidad_libros FROM sagas ORDER BY id_saga")
    r=cur.fetchall(); cur.close(); conn.close(); return r

def eliminar_saga(id_saga):
    try:
        conn=conectar(); cur=conn.cursor()
        cur.execute("DELETE FROM sagas WHERE id_saga=%s",(id_saga,))
        conn.commit(); cur.close(); conn.close()
    except Exception as e:
        conn.rollback(); messagebox.showerror("Error",str(e))

def actualizar_saga(id_saga,nombre,cantidad):
    try:
        conn=conectar(); cur=conn.cursor()
        cur.execute("UPDATE sagas SET nombre=%s,cantidad_libros=%s WHERE id_saga=%s",(nombre,cantidad,id_saga))
        conn.commit(); cur.close(); conn.close()
    except Exception as e:
        conn.rollback(); messagebox.showerror("Error",str(e))