import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
from modulos._theme import *

def abrir_categorias():
    win = tk.Toplevel()
    win.title("Categorías"); win.geometry("600x500"); win.configure(bg=BG)
    header(win,"CATEGORÍAS","Agregar · Editar · Eliminar")

    form = tk.Frame(win,bg=PANEL,pady=12,padx=10); form.pack(fill="x",padx=20,pady=10)
    lbl(form,"Tipo",0,0); e_tipo = entry(form,0,1,30)

    sel = [None]
    def limpiar(): e_tipo.delete(0,tk.END); sel[0]=None

    tabla = scrollable_table(win,("ID","Tipo"),[80,380],name="Cat",accent=BLUE)

    def cargar():
        for r in tabla.get_children(): tabla.delete(r)
        for c in obtener_categorias(): tabla.insert("","end",values=c)

    def seleccionar(event):
        s=tabla.selection()
        if not s: return
        v=tabla.item(s[0])["values"]; sel[0]=v[0]
        e_tipo.delete(0,tk.END); e_tipo.insert(0,v[1])

    tabla.bind("<<TreeviewSelect>>",seleccionar)

    def guardar():
        if not e_tipo.get():
            messagebox.showwarning("Faltan datos","El tipo es obligatorio.",parent=win); return
        guardar_categoria(e_tipo.get()); cargar(); limpiar()

    def editar():
        if not sel[0]:
            messagebox.showwarning("Sin selección","Selecciona una categoría.",parent=win); return
        actualizar_categoria(sel[0],e_tipo.get()); cargar()

    def eliminar():
        s=tabla.selection()
        if not s:
            messagebox.showwarning("Sin selección","Selecciona una categoría.",parent=win); return
        v=tabla.item(s[0])["values"]
        if messagebox.askyesno("Confirmar",f"¿Eliminar '{v[1]}'?",parent=win):
            eliminar_categoria(v[0]); cargar(); limpiar()

    bf = tk.Frame(win,bg=BG); bf.pack(pady=10)
    btn(bf,"+ Guardar",  guardar,  BLUE).pack(side="left",padx=6)
    btn(bf,"Actualizar",editar,   ACCENT).pack(side="left",padx=6)
    btn(bf,"x Eliminar",  eliminar, RED).pack(side="left",padx=6)
    btn(bf,"Limpiar",   limpiar,  SUBTEXT,12).pack(side="left",padx=6)
    cargar()

def guardar_categoria(tipo):
    conn=conectar(); cur=conn.cursor()
    cur.execute("INSERT INTO categoria(tipo) VALUES(%s)",(tipo,))
    conn.commit(); cur.close(); conn.close()

def obtener_categorias():
    conn=conectar(); cur=conn.cursor()
    cur.execute("SELECT id_categoria,tipo FROM categoria ORDER BY id_categoria")
    r=cur.fetchall(); cur.close(); conn.close(); return r

def eliminar_categoria(id_categoria):
    try:
        conn=conectar(); cur=conn.cursor()
        cur.execute("DELETE FROM categoria WHERE id_categoria=%s",(id_categoria,))
        conn.commit(); cur.close(); conn.close()
    except Exception as e:
        conn.rollback(); messagebox.showerror("Error",str(e))

def actualizar_categoria(id_categoria,tipo):
    try:
        conn=conectar(); cur=conn.cursor()
        cur.execute("UPDATE categoria SET tipo=%s WHERE id_categoria=%s",(tipo,id_categoria))
        conn.commit(); cur.close(); conn.close()
    except Exception as e:
        conn.rollback(); messagebox.showerror("Error",str(e))