import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
from modulos._theme import *

def abrir_editoriales():
    win = tk.Toplevel()
    win.title("Editoriales"); win.geometry("1050x580"); win.configure(bg=BG)
    header(win,"EDITORIALES","Agregar · Editar · Eliminar")

    form = tk.Frame(win,bg=PANEL,pady=12,padx=10); form.pack(fill="x",padx=20,pady=10)
    lbl(form,"Nombre",0,0);   e_nombre   = entry(form,0,1)
    lbl(form,"País",0,2);     e_pais     = entry(form,0,3)
    lbl(form,"Teléfono",1,0); e_telefono = entry(form,1,1)
    lbl(form,"Correo",1,2);   e_correo   = entry(form,1,3)

    sel=[None]
    def limpiar():
        for e in [e_nombre,e_pais,e_telefono,e_correo]: e.delete(0,tk.END)
        sel[0]=None

    tabla = scrollable_table(win,("ID","Nombre","País","Teléfono","Correo"),[55,180,120,140,200],name="Ed",accent=ACCENT)

    def cargar():
        for r in tabla.get_children(): tabla.delete(r)
        for e in obtener_editoriales(): tabla.insert("","end",values=e)

    def seleccionar(event):
        s=tabla.selection()
        if not s: return
        v=tabla.item(s[0])["values"]; sel[0]=v[0]
        e_nombre.delete(0,tk.END);   e_nombre.insert(0,v[1])
        e_pais.delete(0,tk.END);     e_pais.insert(0,v[2])
        e_telefono.delete(0,tk.END); e_telefono.insert(0,v[3])
        e_correo.delete(0,tk.END);   e_correo.insert(0,v[4])

    tabla.bind("<<TreeviewSelect>>",seleccionar)

    def guardar():
        if not e_nombre.get():
            messagebox.showwarning("Faltan datos","El nombre es obligatorio.",parent=win); return
        guardar_editorial(e_nombre.get(),e_pais.get(),e_telefono.get(),e_correo.get()); cargar(); limpiar()

    def editar():
        if not sel[0]:
            messagebox.showwarning("Sin selección","Selecciona una editorial.",parent=win); return
        actualizar_editorial(sel[0],e_nombre.get(),e_pais.get(),e_telefono.get(),e_correo.get()); cargar()

    def eliminar():
        s=tabla.selection()
        if not s:
            messagebox.showwarning("Sin selección","Selecciona una editorial.",parent=win); return
        v=tabla.item(s[0])["values"]
        if messagebox.askyesno("Confirmar",f"¿Eliminar '{v[1]}'?",parent=win):
            eliminar_editorial(v[0]); cargar(); limpiar()

    bf=tk.Frame(win,bg=BG); bf.pack(pady=10)
    btn(bf,"+ Guardar",  guardar,  ACCENT).pack(side="left",padx=6)
    btn(bf,"Actualizar",editar,   BLUE).pack(side="left",padx=6)
    btn(bf,"x Eliminar",  eliminar, RED).pack(side="left",padx=6)
    btn(bf,"Limpiar",   limpiar,  SUBTEXT,12).pack(side="left",padx=6)
    cargar()

def guardar_editorial(nombre,pais,telefono,correo):
    conn=conectar(); cur=conn.cursor()
    cur.execute("INSERT INTO editorial(nombre,pais,telefono,correo) VALUES(%s,%s,%s,%s)",(nombre,pais,telefono,correo))
    conn.commit(); cur.close(); conn.close()

def obtener_editoriales():
    conn=conectar(); cur=conn.cursor()
    cur.execute("SELECT id_editorial,nombre,pais,telefono,correo FROM editorial ORDER BY id_editorial")
    r=cur.fetchall(); cur.close(); conn.close(); return r

def eliminar_editorial(id_editorial):
    try:
        conn=conectar(); cur=conn.cursor()
        cur.execute("DELETE FROM editorial WHERE id_editorial=%s",(id_editorial,))
        conn.commit(); cur.close(); conn.close()
    except Exception as e:
        conn.rollback(); messagebox.showerror("Error",str(e))

def actualizar_editorial(id_editorial,nombre,pais,telefono,correo):
    try:
        conn=conectar(); cur=conn.cursor()
        cur.execute("UPDATE editorial SET nombre=%s,pais=%s,telefono=%s,correo=%s WHERE id_editorial=%s",(nombre,pais,telefono,correo,id_editorial))
        conn.commit(); cur.close(); conn.close()
    except Exception as e:
        conn.rollback(); messagebox.showerror("Error",str(e))