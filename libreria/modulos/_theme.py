# ─── Paleta compartida ───────────────────────────────────────────
BG      = "#0F1923"
CARD    = "#162130"
PANEL   = "#1C2B3A"
ACCENT  = "#E8A045"
BLUE    = "#5B9BD5"
TEXT    = "#EEE8DC"
SUBTEXT = "#7A8FA6"
RED     = "#C0392B"
GREEN   = "#27AE60"

def style_table(tree, name, accent=ACCENT):
    from tkinter import ttk
    s = ttk.Style(); s.theme_use("clam")
    s.configure(f"{name}.Treeview", background=CARD, foreground=TEXT,
        fieldbackground=CARD, rowheight=27, font=("Courier New", 10))
    s.configure(f"{name}.Treeview.Heading", background=PANEL, foreground=accent,
        font=("Courier New", 10, "bold"), relief="flat")
    s.map(f"{name}.Treeview",
        background=[("selected", accent)], foreground=[("selected", BG)])
    tree.configure(style=f"{name}.Treeview")

def lbl(parent, text, row, col, bg=None):
    import tkinter as tk
    tk.Label(parent, text=text, font=("Courier New", 10),
             bg=bg or PANEL, fg=SUBTEXT).grid(row=row, column=col,
             sticky="w", padx=8, pady=4)

def entry(parent, row, col, width=24, bg=None):
    import tkinter as tk
    e = tk.Entry(parent, font=("Courier New", 11), bg=bg or BG, fg=TEXT,
                 insertbackground=ACCENT, relief="flat", bd=0, width=width,
                 highlightthickness=1, highlightbackground=SUBTEXT,
                 highlightcolor=ACCENT)
    e.grid(row=row, column=col, padx=8, pady=4, ipady=5)
    return e

def combo(parent, vals, width=30):
    from tkinter import ttk
    cb = ttk.Combobox(parent, values=vals, font=("Courier New", 10),
                      width=width, state="readonly")
    s = ttk.Style()
    s.configure("TCombobox", fieldbackground=BG, foreground=TEXT, arrowcolor=ACCENT)
    return cb

def btn(parent, text, cmd, color=None, width=16):
    import tkinter as tk
    c = color or ACCENT
    b = tk.Button(parent, text=text, command=cmd,
                  font=("Courier New", 10, "bold"), bg=PANEL, fg=c,
                  activebackground=c, activeforeground=BG,
                  relief="flat", bd=0, cursor="hand2", width=width, pady=6)
    b.bind("<Enter>", lambda e: b.config(bg=c, fg=BG))
    b.bind("<Leave>", lambda e: b.config(bg=PANEL, fg=c))
    return b

def header(win, title, subtitle=""):
    import tkinter as tk
    tk.Frame(win, bg=ACCENT, height=4).pack(fill="x")
    tk.Label(win, text=title, font=("Georgia", 17, "bold"),
             bg=BG, fg=TEXT).pack(pady=(12,2))
    if subtitle:
        tk.Label(win, text=subtitle, font=("Courier New", 9),
                 bg=BG, fg=SUBTEXT).pack()

def scrollable_table(parent, cols, widths, height=14, name="T", accent=ACCENT):
    import tkinter as tk
    from tkinter import ttk
    frame = tk.Frame(parent, bg=BG)
    frame.pack(fill="both", expand=True, padx=20, pady=6)
    tabla = ttk.Treeview(frame, columns=cols, show="headings", height=height)
    style_table(tabla, name, accent)
    for col, w in zip(cols, widths):
        tabla.heading(col, text=col)
        tabla.column(col, width=w, anchor="center")
    sb = ttk.Scrollbar(frame, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=sb.set)
    tabla.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")
    return tabla
