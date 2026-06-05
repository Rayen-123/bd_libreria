import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
from modulos._theme import *

def abrir_libros():
    win = tk.Toplevel()
    win.title("Gestión de Libros"); win.geometry("1200x700"); win.configure(bg=BG)
    header(win, "LIBROS", "Catálogo completo · Agregar · Editar · Eliminar")

    form = tk.Frame(win, bg=PANEL, pady=12, padx=10)
    form.pack(fill="x", padx=20, pady=10)
    lbl(form,"Título",0,0);          e_titulo  = entry(form,0,1,30)
    lbl(form,"Precio",1,0);          e_precio  = entry(form,1,1,14)
    lbl(form,"Año Publicación",2,0); e_anio    = entry(form,2,1,10)
    lbl(form,"Estante",3,0);         e_estante = entry(form,3,1,10)

    autores     = obtener_autores()
    categorias  = obtener_categorias()
    editoriales = obtener_editoriales()
    sagas       = obtener_sagas()

    lbl(form,"Autor",0,2)
    cb_autor = combo(form,[f"{a[0]} - {a[1]} {a[2]}" for a in autores])
    cb_autor.grid(row=0,column=3,padx=8,pady=4)

    lbl(form,"Categoría",1,2)
    cb_cat = combo(form,[f"{c[0]} - {c[1]}" for c in categorias])
    cb_cat.grid(row=1,column=3,padx=8,pady=4)

    lbl(form,"Editorial",2,2)
    cb_ed = combo(form,[f"{e[0]} - {e[1]}" for e in editoriales])
    cb_ed.grid(row=2,column=3,padx=8,pady=4)

    lbl(form,"Saga",3,2)
    cb_saga = combo(form,[f"{s[0]} - {s[1]}" for s in sagas])
    cb_saga.grid(row=3,column=3,padx=8,pady=4)

    libro_sel = [None]

    def limpiar():
        for e in [e_titulo,e_precio,e_anio,e_estante]: e.delete(0,tk.END)
        for cb in [cb_autor,cb_cat,cb_ed,cb_saga]: cb.set("")
        libro_sel[0] = None

    tabla = scrollable_table(win,("ID","Título","Precio","Año","Autor","Categoría"),
                             [55,280,90,60,200,120],height=11,name="Lib")

    def cargar():
        for r in tabla.get_children(): tabla.delete(r)
        for lb in obtener_libros():
            tabla.insert("","end",values=(lb[0],lb[1],lb[2],lb[3],lb[9],lb[10]))

    def seleccionar(event):
        sel = tabla.selection()
        if not sel: return
        id_lb = tabla.item(sel[0])["values"][0]
        datos = next((l for l in obtener_libros() if l[0]==id_lb),None)
        if not datos: return
        libro_sel[0]=datos[0]
        e_titulo.delete(0,tk.END);  e_titulo.insert(0,datos[1])
        e_precio.delete(0,tk.END);  e_precio.insert(0,datos[2])
        e_anio.delete(0,tk.END);    e_anio.insert(0,datos[3])
        e_estante.delete(0,tk.END); e_estante.insert(0,datos[4])
        for a in autores:
            if a[0]==datos[5]: cb_autor.set(f"{a[0]} - {a[1]} {a[2]}"); break
        for c in categorias:
            if c[0]==datos[6]: cb_cat.set(f"{c[0]} - {c[1]}"); break
        for e in editoriales:
            if e[0]==datos[7]: cb_ed.set(f"{e[0]} - {e[1]}"); break
        for s in sagas:
            if s[0]==datos[8]: cb_saga.set(f"{s[0]} - {s[1]}"); break

    tabla.bind("<<TreeviewSelect>>",seleccionar)

    def guardar():
        try:
            id_autor=int(cb_autor.get().split(" - ")[0]); id_cat=int(cb_cat.get().split(" - ")[0])
            id_ed=int(cb_ed.get().split(" - ")[0]);       id_saga=int(cb_saga.get().split(" - ")[0])
        except:
            messagebox.showwarning("Faltan datos","Completa todos los campos.",parent=win); return
        if guardar_libro(e_titulo.get(),float(e_precio.get()),id_autor,id_cat,id_ed,id_saga,int(e_anio.get()),e_estante.get()):
            cargar(); limpiar()

    def editar():
        if not libro_sel[0]:
            messagebox.showwarning("Sin selección","Selecciona un libro.",parent=win); return
        if actualizar_libro(libro_sel[0],e_titulo.get(),float(e_precio.get())):
            cargar(); messagebox.showinfo("","Libro actualizado.",parent=win)

    def eliminar():
        sel = tabla.selection()
        if not sel:
            messagebox.showwarning("Sin selección","Selecciona un libro.",parent=win); return
        v = tabla.item(sel[0])["values"]
        if messagebox.askyesno("Confirmar",f"¿Eliminar '{v[1]}'?",parent=win):
            if eliminar_libro(v[0]): cargar(); limpiar()

    bf = tk.Frame(win,bg=BG); bf.pack(pady=10)
    btn(bf,"+ Guardar",  guardar,  ACCENT).pack(side="left",padx=6)
    btn(bf,"Actualizar",editar,   BLUE).pack(side="left",padx=6)
    btn(bf,"x Eliminar",  eliminar, RED).pack(side="left",padx=6)
    btn(bf,"Limpiar",   limpiar,  SUBTEXT,12).pack(side="left",padx=6)
    cargar()

def obtener_autores():
    conn=conectar(); cur=conn.cursor()
    cur.execute("SELECT id_autor,nombre,apellido FROM autor ORDER BY nombre")
    r=cur.fetchall(); cur.close(); conn.close(); return r

def obtener_categorias():
    conn=conectar(); cur=conn.cursor()
    cur.execute("SELECT id_categoria,tipo FROM categoria ORDER BY tipo")
    r=cur.fetchall(); cur.close(); conn.close(); return r

def obtener_editoriales():
    conn=conectar(); cur=conn.cursor()
    cur.execute("SELECT id_editorial,nombre FROM editorial ORDER BY nombre")
    r=cur.fetchall(); cur.close(); conn.close(); return r

def obtener_sagas():
    conn=conectar(); cur=conn.cursor()
    cur.execute("SELECT id_saga,nombre FROM sagas ORDER BY nombre")
    r=cur.fetchall(); cur.close(); conn.close(); return r

def guardar_libro(titulo,precio,id_autor,id_categoria,id_editorial,id_saga,anio,estante):
    try:
        conn=conectar(); cur=conn.cursor()
        cur.execute("INSERT INTO producto(nombre,precio) VALUES(%s,%s) RETURNING id_producto",(titulo,precio))
        id_producto=cur.fetchone()[0]
        cur.execute("INSERT INTO libro(id_autor,id_categoria,id_editorial,id_saga,titulo,anio_publicacion,precio,estante,id_producto) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (id_autor,id_categoria,id_editorial,id_saga,titulo,anio,precio,estante,id_producto))
        conn.commit(); cur.close(); conn.close(); return True
    except Exception as e:
        conn.rollback(); messagebox.showerror("Error",str(e)); return False

def obtener_libros():
    conn=conectar(); cur=conn.cursor()
    cur.execute("""SELECT l.id_libro,l.titulo,l.precio,l.anio_publicacion,l.estante,
                   l.id_autor,l.id_categoria,l.id_editorial,l.id_saga,
                   a.nombre||' '||a.apellido,c.tipo
                   FROM libro l JOIN autor a ON l.id_autor=a.id_autor
                   JOIN categoria c ON l.id_categoria=c.id_categoria ORDER BY l.id_libro""")
    r=cur.fetchall(); cur.close(); conn.close(); return r

def actualizar_libro(id_libro,titulo,precio):
    try:
        conn=conectar(); cur=conn.cursor()
        cur.execute("UPDATE libro SET titulo=%s,precio=%s WHERE id_libro=%s",(titulo,precio,id_libro))
        conn.commit(); cur.close(); conn.close(); return True
    except Exception as e:
        conn.rollback(); messagebox.showerror("Error",str(e)); return False

def eliminar_libro(id_libro):
    try:
        conn=conectar(); cur=conn.cursor()
        cur.execute("DELETE FROM libro WHERE id_libro=%s",(id_libro,))
        conn.commit(); cur.close(); conn.close(); return True
    except Exception as e:
        conn.rollback(); messagebox.showerror("Error",f"No se puede eliminar: {e}"); return False