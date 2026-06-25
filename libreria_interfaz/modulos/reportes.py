import tkinter as tk
from tkinter import ttk
from database import conectar
from modulos._theme import *

def abrir_menu_reportes():
    win = tk.Toplevel()
    win.title("Reportes"); win.geometry("360x360"); win.configure(bg=BG)
    header(win,"REPORTES","Consultas y estadísticas")
    body = tk.Frame(win,bg=BG); body.pack(padx=40,pady=10,fill="x")
    for txt,cmd,color in [
        ("  Libros Más Vendidos",  abrir_reporte_libros,      ACCENT),
        ("  Clientes Frecuentes",  abrir_reporte_clientes,    BLUE),
        ("  Ventas por Día",       abrir_reporte_ventas_dia,  ACCENT),
        ("  Ventas por Cajero",    abrir_reporte_cajeros,     BLUE),
    ]:
        b = tk.Button(body,text=txt,command=cmd,font=("Courier New",11,"bold"),
                      bg=CARD,fg=TEXT,activebackground=color,activeforeground=BG,
                      relief="flat",bd=0,cursor="hand2",width=28,height=2,anchor="w",padx=16)
        b.bind("<Enter>",lambda e,b=b,c=color:b.config(bg=c,fg=BG))
        b.bind("<Leave>",lambda e,b=b:b.config(bg=CARD,fg=TEXT))
        b.pack(pady=5,fill="x")

def _reporte_tabla(titulo,subtitle,cols,widths,datos,name,accent=ACCENT):
    win = tk.Toplevel()
    win.title(titulo); win.geometry("800x520"); win.configure(bg=BG)
    header(win,titulo,subtitle)
    tabla = scrollable_table(win,cols,widths,height=16,name=name,accent=accent)
    for fila in datos: tabla.insert("","end",values=fila)

def abrir_reporte_libros():
    datos = _obtener("SELECT l.titulo,SUM(dv.cantidad) FROM detalleventa dv JOIN libro l ON dv.id_producto=l.id_producto GROUP BY l.titulo ORDER BY 2 DESC")
    _reporte_tabla("LIBROS MÁS VENDIDOS","Ranking por cantidad vendida",("Título","Cantidad Vendida"),(480,160),datos,"RLib")

def abrir_reporte_clientes():
    datos = _obtener("SELECT c.nombre||' '||c.apellido,SUM(v.total) FROM venta v JOIN cliente c ON v.id_cliente=c.id_cliente GROUP BY c.id_cliente,c.nombre,c.apellido ORDER BY 2 DESC")
    formatted = [(d[0], f"$ {d[1]:,.0f}") for d in datos]
    _reporte_tabla("CLIENTES FRECUENTES","Ordenados por total comprado",("Cliente","Total Comprado"),(380,200),formatted,"RCli",accent=BLUE)

def abrir_reporte_ventas_dia():
    datos = _obtener("SELECT DATE(fecha_hora),SUM(total) FROM venta GROUP BY DATE(fecha_hora) ORDER BY 1 DESC")
    formatted = [(str(d[0]), f"$ {d[1]:,.0f}") for d in datos]
    _reporte_tabla("VENTAS POR DÍA","Total diario de ventas",("Fecha","Total Vendido"),(280,200),formatted,"RDia")

def abrir_reporte_cajeros():
    datos = _obtener("SELECT e.nombre||' '||e.apellido,COUNT(v.id_venta) FROM venta v JOIN cajero c ON v.id_cajero=c.id_cajero JOIN empleado e ON c.id_empleado=e.id_empleado GROUP BY e.nombre,e.apellido ORDER BY 2 DESC")
    _reporte_tabla("VENTAS POR CAJERO","Cantidad de ventas por cajero",("Cajero","Ventas"),(400,160),datos,"RCaj",accent=BLUE)

def _obtener(query):
    conn=conectar(); cur=conn.cursor()
    cur.execute(query); r=cur.fetchall(); cur.close(); conn.close(); return r