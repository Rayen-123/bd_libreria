import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
from modulos._theme import *

def abrir_ventas():
    win = tk.Toplevel()
    win.title("Nueva Venta"); win.geometry("900x660"); win.configure(bg=BG)
    header(win, "NUEVA VENTA", "Agrega productos y finaliza la venta")

    clientes  = obtener_clientes()
    cajeros   = obtener_cajeros()
    cajas     = obtener_cajas()
    sucursales= obtener_sucursales()
    productos = obtener_productos()

    top = tk.Frame(win,bg=PANEL,pady=10,padx=20); top.pack(fill="x",padx=20,pady=8)

    def lbl2(p,t,r,c): tk.Label(p,text=t,font=("Courier New",10),bg=PANEL,fg=SUBTEXT).grid(row=r,column=c,sticky="w",padx=8,pady=3)

    lbl2(top,"Cliente",0,0)
    cb_cliente = combo(top,[f"{c[0]} - {c[1]} {c[2]}" for c in clientes],38)
    cb_cliente.grid(row=0,column=1,padx=8,pady=3)
    lbl2(top,"Cajero",0,2)
    cb_cajero = combo(top,[f"{c[0]} - {c[1]}" for c in cajeros],28)
    cb_cajero.grid(row=0,column=3,padx=8,pady=3)
    lbl2(top,"Caja",1,0)
    cb_caja = combo(top,[f"{c[0]} - Caja {c[1]}" for c in cajas],20)
    cb_caja.grid(row=1,column=1,padx=8,pady=3)
    lbl2(top,"Sucursal",1,2)
    cb_suc = combo(top,[f"{s[0]} - {s[1]}" for s in sucursales],28)
    cb_suc.grid(row=1,column=3,padx=8,pady=3)

    mid = tk.Frame(win,bg=PANEL,pady=10,padx=20); mid.pack(fill="x",padx=20,pady=2)
    lbl2(mid,"Producto",0,0)
    cb_prod = combo(mid,[f"{p[0]} - {p[1]}" for p in productos],40)
    cb_prod.grid(row=0,column=1,padx=8,pady=3)
    lbl2(mid,"Cantidad",0,2)
    e_cant = tk.Entry(mid,font=("Courier New",11),bg=BG,fg=TEXT,insertbackground=ACCENT,
                      relief="flat",bd=0,width=8,highlightthickness=1,
                      highlightbackground=SUBTEXT,highlightcolor=ACCENT)
    e_cant.grid(row=0,column=3,padx=8,pady=3,ipady=5); e_cant.insert(0,"1")

    tabla = scrollable_table(win,("Producto","Precio Unit.","Cantidad","Subtotal"),
                             [360,130,100,130],height=8,name="VtaN",accent=BLUE)

    tf = tk.Frame(win,bg=BG); tf.pack(fill="x",padx=24)
    tk.Label(tf,text="TOTAL:",font=("Courier New",12,"bold"),bg=BG,fg=SUBTEXT).pack(side="left")
    lbl_total = tk.Label(tf,text="$ 0",font=("Georgia",15,"bold"),bg=BG,fg=ACCENT)
    lbl_total.pack(side="left",padx=10)

    detalle_venta = []

    def refrescar():
        for r in tabla.get_children(): tabla.delete(r)
        for item in detalle_venta:
            tabla.insert("","end",values=(item["nombre"],f"$ {item['precio']:,.0f}",item["cantidad"],f"$ {item['subtotal']:,.0f}"))
        lbl_total.config(text=f"$ {sum(i['subtotal'] for i in detalle_venta):,.0f}")

    def agregar_producto():
        try:
            id_p=int(cb_prod.get().split(" - ")[0]); cant=int(e_cant.get())
            if cant<=0: raise ValueError
        except:
            messagebox.showwarning("Error","Selecciona producto y cantidad válida.",parent=win); return
        prod=next((p for p in productos if p[0]==id_p),None)
        if not prod: return
        for item in detalle_venta:
            if item["id_producto"]==id_p:
                item["cantidad"]+=cant; item["subtotal"]=item["cantidad"]*item["precio"]; break
        else:
            detalle_venta.append({"id_producto":id_p,"nombre":prod[1],"cantidad":cant,"precio":float(prod[2]),"subtotal":cant*float(prod[2])})
        refrescar(); cb_prod.set(""); e_cant.delete(0,tk.END); e_cant.insert(0,"1")

    def quitar():
        sel=tabla.selection()
        if not sel: return
        detalle_venta.pop(tabla.index(sel[0])); refrescar()

    def registrar():
        if not detalle_venta:
            messagebox.showwarning("Carrito vacío","Agrega al menos un producto.",parent=win); return
        try:
            id_cliente=int(cb_cliente.get().split(" - ")[0])
            id_cajero=int(cb_cajero.get().split(" - ")[0])
            id_caja=int(cb_caja.get().split(" - ")[0])
        except:
            messagebox.showwarning("Faltan datos","Selecciona cliente, cajero y caja.",parent=win); return
        id_venta=crear_venta(id_cliente,id_caja,id_cajero)
        total=0
        for item in detalle_venta:
            total+=agregar_detalle(id_venta,item["id_producto"],item["cantidad"],item["precio"])
        actualizar_total(id_venta,total)
        messagebox.showinfo("Venta registrada",f"Venta #{id_venta} registrada.\nTotal: $ {total:,.0f}",parent=win)
        detalle_venta.clear(); refrescar()
        for cb in [cb_cliente,cb_cajero,cb_caja,cb_suc,cb_prod]: cb.set("")

    bf = tk.Frame(win,bg=BG); bf.pack(pady=10)
    btn(bf,"+ Agregar Producto",   agregar_producto, BLUE,22).pack(side="left",padx=6)
    btn(bf,"x Quitar Seleccionado", quitar,           RED,20).pack(side="left",padx=6)
    btn(bf,"Registrar Venta",     registrar,        GREEN,20).pack(side="left",padx=6)

#  SQL 
def obtener_clientes():
    conn=conectar(); cur=conn.cursor()
    cur.execute("SELECT id_cliente,nombre,apellido FROM cliente ORDER BY nombre")
    r=cur.fetchall(); cur.close(); conn.close(); return r

def obtener_cajeros():
    conn=conectar(); cur=conn.cursor()
    cur.execute("SELECT c.id_cajero,e.nombre,e.apellido FROM cajero c JOIN empleado e ON c.id_empleado=e.id_empleado ORDER BY e.nombre")
    r=cur.fetchall(); cur.close(); conn.close(); return r

def obtener_cajas():
    conn=conectar(); cur=conn.cursor()
    cur.execute("SELECT id_caja,numero_caja FROM caja ORDER BY numero_caja")
    r=cur.fetchall(); cur.close(); conn.close(); return r

def obtener_sucursales():
    conn=conectar(); cur=conn.cursor()
    cur.execute("SELECT id_sucursal,nombre FROM sucursal ORDER BY nombre")
    r=cur.fetchall(); cur.close(); conn.close(); return r

def obtener_productos():
    conn=conectar(); cur=conn.cursor()
    cur.execute("SELECT id_producto,nombre,precio FROM producto ORDER BY nombre")
    r=cur.fetchall(); cur.close(); conn.close(); return r

def crear_venta(id_cliente,id_caja,id_cajero):
    conn=conectar(); cur=conn.cursor()
    cur.execute("INSERT INTO venta(fecha_hora,total,id_cliente,id_caja,id_cajero) VALUES(NOW(),0,%s,%s,%s) RETURNING id_venta",(id_cliente,id_caja,id_cajero))
    id_v=cur.fetchone()[0]; conn.commit(); cur.close(); conn.close(); return id_v

def agregar_detalle(id_venta,id_producto,cantidad,precio):
    subtotal=cantidad*precio
    conn=conectar(); cur=conn.cursor()
    cur.execute("INSERT INTO detalleventa(id_venta,id_producto,cantidad,precio_unitario,subtotal) VALUES(%s,%s,%s,%s,%s)",(id_venta,id_producto,cantidad,precio,subtotal))
    conn.commit(); cur.close(); conn.close(); return subtotal

def actualizar_total(id_venta,total):
    conn=conectar(); cur=conn.cursor()
    cur.execute("UPDATE venta SET total=%s WHERE id_venta=%s",(total,id_venta))
    conn.commit(); cur.close(); conn.close()