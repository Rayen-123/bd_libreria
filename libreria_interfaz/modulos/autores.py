import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
from modulos._theme import *

def abrir_autores():
    win = tk.Toplevel()
    win.title("Gestión de Autores"); win.geometry("950x580"); win.configure(bg=BG)
    header(win,"AUTORES","Agregar · Editar · Eliminar")

    form = tk.Frame(win,bg=PANEL,pady=12,padx=10); form.pack(fill="x",padx=20,pady=10)
    lbl(form,"Nombre",0,0);        e_nombre       = entry(form,0,1)
    lbl(form,"Apellido",0,2);      e_apellido     = entry(form,0,3)
    lbl(form,"Nacionalidad",1,0);  e_nacionalidad = entry(form,1,1)

    sel = [None]
    def limpiar():
        for e in [e_nombre,e_apellido,e_nacionalidad]: e.delete(0,tk.END)
        sel[0]=None

    tabla = scrollable_table(win,("ID","Nombre","Apellido","Nacionalidad"),[60,200,200,200],name="Aut")

    def cargar():
        for r in tabla.get_children(): tabla.delete(r)
        for a in obtener_Autores(): tabla.insert("","end",values=a)

    def seleccionar(event):
        s=tabla.selection()
        if not s: return
        v=tabla.item(s[0])["values"]; sel[0]=v[0]
        e_nombre.delete(0,tk.END);       e_nombre.insert(0,v[1])
        e_apellido.delete(0,tk.END);     e_apellido.insert(0,v[2])
        e_nacionalidad.delete(0,tk.END); e_nacionalidad.insert(0,v[3])

    tabla.bind("<<TreeviewSelect>>",seleccionar)

    def guardar():
        if not e_nombre.get():
            messagebox.showwarning("Faltan datos","El nombre es obligatorio.",parent=win); return
        guardar_autor(e_nombre.get(),e_apellido.get(),e_nacionalidad.get()); cargar(); limpiar()

    def editar():
        if not sel[0]:
            messagebox.showwarning("Sin selección","Selecciona un autor.",parent=win); return
        actualizar_autor(sel[0],e_nombre.get(),e_apellido.get(),e_nacionalidad.get())
        cargar(); messagebox.showinfo("","Autor actualizado.",parent=win)

    def eliminar():
        s=tabla.selection()
        if not s:
            messagebox.showwarning("Sin selección","Selecciona un autor.",parent=win); return
        v=tabla.item(s[0])["values"]
        if messagebox.askyesno("Confirmar",f"¿Eliminar a {v[1]} {v[2]}?",parent=win):
            eliminar_autor(v[0]); cargar(); limpiar()

    bf = tk.Frame(win,bg=BG); bf.pack(pady=10)
    btn(bf,"+ Guardar",  guardar,  ACCENT).pack(side="left",padx=6)
    btn(bf,"Actualizar",editar,   BLUE).pack(side="left",padx=6)
    btn(bf,"x Eliminar",  eliminar, RED).pack(side="left",padx=6)
    btn(bf,"Limpiar",   limpiar,  SUBTEXT,12).pack(side="left",padx=6)
    cargar()

def guardar_autor(nombre,apellido,nacionalidad):
    conn=conectar(); cur=conn.cursor()
    cur.execute("INSERT INTO autor(nombre,apellido,nacionalidad) VALUES(%s,%s,%s)",(nombre,apellido,nacionalidad))
    conn.commit(); cur.close(); conn.close()

def obtener_Autores():
    conn=conectar(); cur=conn.cursor()
    cur.execute("SELECT id_autor,nombre,apellido,nacionalidad FROM autor ORDER BY id_autor")
    r=cur.fetchall(); cur.close(); conn.close(); return r

def eliminar_autor(id_autor):
    try:
        conn=conectar(); cur=conn.cursor()
        cur.execute("DELETE FROM autor WHERE id_autor=%s",(id_autor,))
        conn.commit(); cur.close(); conn.close()
    except Exception as e:
        conn.rollback(); messagebox.showerror("Error",str(e))

def actualizar_autor(id_autor,nombre,apellido,nacionalidad):
    try:
        conn=conectar(); cur=conn.cursor()
        cur.execute("UPDATE autor SET nombre=%s,apellido=%s,nacionalidad=%s WHERE id_autor=%s",(nombre,apellido,nacionalidad,id_autor))
        conn.commit(); cur.close(); conn.close()
    except Exception as e:
        conn.rollback(); messagebox.showerror("Error",str(e))