import tkinter as tk
from modulos.clientes import abrir_clientes
from modulos.productos import abrir_productos
from modulos.ventas import abrir_ventas
from modulos.libros import abrir_libros
from modulos.historial_ventas import abrir_historial_ventas
from modulos.autores import abrir_autores
from modulos.categorias import abrir_categorias
from modulos.editoriales import abrir_editoriales
from modulos.sagas import abrir_sagas
from modulos.reportes import abrir_menu_reportes
from modulos.empleados import abrir_empleados
from modulos.cajeros import abrir_cajeros

BG      = "#0F1923"
CARD    = "#162130"
PANEL   = "#1C2B3A"
ACCENT  = "#E8A045"
BLUE    = "#5B9BD5"
TEXT    = "#EEE8DC"
SUBTEXT = "#7A8FA6"

def _btn(parent, text, cmd, color, width=22):
    b = tk.Button(parent, text=text, command=cmd,
                  font=("Courier New", 11, "bold"),
                  bg=CARD, fg=TEXT, activebackground=color,
                  activeforeground=BG, relief="flat", bd=0,
                  cursor="hand2", width=width, height=2,
                  anchor="w", padx=16)
    b.bind("<Enter>", lambda e, b=b, c=color: b.config(bg=c, fg=BG))
    b.bind("<Leave>", lambda e, b=b: b.config(bg=CARD, fg=TEXT))
    return b

def abrir_inventario():
    win = tk.Toplevel(); win.title("Inventario")
    win.geometry("340x400"); win.configure(bg=BG)
    tk.Frame(win, bg=ACCENT, height=4).pack(fill="x")
    tk.Label(win, text="INVENTARIO", font=("Georgia", 15, "bold"),
             bg=BG, fg=TEXT).pack(pady=(12,6))
    body = tk.Frame(win, bg=BG); body.pack(padx=30, fill="x")
    for txt, cmd in [("  Libros", abrir_libros), ("  Productos", abrir_productos),
                     ("   Autores", abrir_autores), ("   Categorías", abrir_categorias),
                     ("  Editoriales", abrir_editoriales), ("  Sagas", abrir_sagas)]:
        _btn(body, txt, cmd, ACCENT).pack(pady=4, fill="x")

def abrir_menu_ventas():
    win = tk.Toplevel(); win.title("Ventas")
    win.geometry("340x230"); win.configure(bg=BG)
    tk.Frame(win, bg=BLUE, height=4).pack(fill="x")
    tk.Label(win, text="VENTAS", font=("Georgia", 15, "bold"),
             bg=BG, fg=TEXT).pack(pady=(12,6))
    body = tk.Frame(win, bg=BG); body.pack(padx=30, fill="x")
    _btn(body, "  Nueva Venta",       abrir_ventas,          BLUE).pack(pady=4, fill="x")
    _btn(body, "  Historial de Ventas", abrir_historial_ventas, BLUE).pack(pady=4, fill="x")

def abrir_personal():
    win = tk.Toplevel(); win.title("Personal")
    win.geometry("340x230"); win.configure(bg=BG)
    tk.Frame(win, bg=SUBTEXT, height=4).pack(fill="x")
    tk.Label(win, text="PERSONAL", font=("Georgia", 15, "bold"),
             bg=BG, fg=TEXT).pack(pady=(12,6))
    body = tk.Frame(win, bg=BG); body.pack(padx=30, fill="x")
    _btn(body, "  Empleados", abrir_empleados, SUBTEXT).pack(pady=4, fill="x")
    _btn(body, "  Cajeros",   abrir_cajeros,   SUBTEXT).pack(pady=4, fill="x")

ventana = tk.Tk()
ventana.title("Sistema Librería")
ventana.geometry("540x620")
ventana.resizable(False, False)
ventana.configure(bg=BG)

tk.Frame(ventana, bg=ACCENT, height=5).pack(fill="x")

body = tk.Frame(ventana, bg=BG)
body.pack(fill="both", expand=True, padx=44, pady=20)

tk.Label(body, text="", font=("Segoe UI Emoji", 38), bg=BG, fg=ACCENT).pack(pady=(8,0))
tk.Label(body, text="LIBRERÍA", font=("Georgia", 24, "bold"), bg=BG, fg=TEXT).pack()
tk.Label(body, text="Sistema de Gestión", font=("Courier New", 10), bg=BG, fg=SUBTEXT).pack(pady=(2,18))

tk.Frame(body, bg=ACCENT, height=1).pack(fill="x", pady=(0,18))

for txt, cmd, color in [
    ("  Ventas",      abrir_menu_ventas,  BLUE),
    ("  Clientes",    abrir_clientes,     ACCENT),
    ("  Inventario",  abrir_inventario,   ACCENT),
    ("  Reportes",    abrir_menu_reportes, BLUE),
    ("  Personal",    abrir_personal,     SUBTEXT),
]:
    _btn(body, txt, cmd, color, 30).pack(pady=5, fill="x")

tk.Label(ventana, text="v2.0  ·  Gestión Interna",
         font=("Courier New", 8), bg=BG, fg=SUBTEXT).pack(pady=(0,8))

ventana.mainloop()