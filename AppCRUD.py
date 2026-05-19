import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import psycopg2
from psycopg2 import Error

class AppCRUD:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor PostgreSQL")
        self.root.geometry("400x350")
        
        # --- APLICAR ESTILOS GLOBALES ---
        self.color_fondo = "#f7f9fc"
        self.root.config(padx=20, pady=20, bg=self.color_fondo)
        self.aplicar_estilos_visuales()
        
        # 1. Inicializar la base de datos
        self.preparar_base_datos()
        
        # 2. Crear el formulario si la conexión fue exitosa
        if hasattr(self, 'conexion'):
            self.mostrar()

    def aplicar_estilos_visuales(self):
        """Configura la estética global de la aplicación (fuentes, temas y colores)"""
        style = ttk.Style()
        style.theme_use('clam') # Tema moderno y plano
        
        # Configuración de la tabla (Treeview)
        style.configure("Treeview", font=("Helvetica", 10), rowheight=25, background="white")
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background="#e0e0e0", foreground="black")
        style.map("Treeview", background=[('selected', '#2196F3')]) # Color al seleccionar fila

        # Configuraciones globales para los widgets clásicos de tk
        self.root.option_add("*Font", "Helvetica 10")
        self.root.option_add("*Label.background", self.color_fondo)
        self.root.option_add("*Button.relief", "flat")
        self.root.option_add("*Button.cursor", "hand2")
        self.root.option_add("*Button.font", "Helvetica 10 bold")
        self.root.option_add("*Button.pady", 5)

    def preparar_base_datos(self):
        try:
            self.conexion = psycopg2.connect(
                host="localhost",      
                database="libreria",    
                user="postgres",     
                password="21970",   
                port="5432"            
            )
            self.cursor = self.conexion.cursor()
            self.conexion.commit()
        except Error as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a PostgreSQL:\n{e}")

    def mostrar(self):
        # Título del menú principal
        tk.Label(self.root, text="Panel de Control", font=("Helvetica", 16, "bold"), fg="#333").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        tk.Button(self.root, text="Insertar Nuevo Registro", command=self.menu_insertar, bg="#4CAF50", fg="white", width=25).grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Actualizar Existente", command=self.menu_actualizar, bg="#FFC107", fg="black", width=25).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Eliminar Registro", command=self.menu_eliminar, bg="#F44336", fg="white", width=25).grid(row=3, column=0, columnspan=2, pady=10)


    # =========================================================
    # MENÚ INSERTAR
    # =========================================================
    def menu_insertar(self):
        nueva_ventana = tk.Toplevel(self.root)
        nueva_ventana.title("Menú Insertar")
        nueva_ventana.geometry("300x380")
        nueva_ventana.config(padx=20, pady=20, bg=self.color_fondo)

        tk.Label(nueva_ventana, text="¿Qué deseas insertar?", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0,15))

        tk.Button(nueva_ventana, text="Insertar Cliente", command=self.cliente_insertar, bg="#4CAF50", fg="white", width=20).grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(nueva_ventana, text="Insertar Libro", command=self.libro_insertar, bg="#4CAF50", fg="white", width=20).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(nueva_ventana, text="Insertar Empleado", command=self.empleado_insertar, bg="#4CAF50", fg="white", width=20).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(nueva_ventana, text="Registrar Venta", command=self.venta_insertar, bg="#4CAF50", fg="white", width=20).grid(row=4, column=0, columnspan=2, pady=10)

    # --- CLIENTE ---
    def cliente_insertar(self):
        ventana_cliente = tk.Toplevel(self.root)
        ventana_cliente.title("Insertar Cliente")
        ventana_cliente.geometry("320x300")
        ventana_cliente.config(padx=20, pady=20, bg=self.color_fondo)

        tk.Label(ventana_cliente, text="Nombre:").grid(row=0, column=0, pady=8, sticky="w")
        self.entry_nombre = ttk.Entry(ventana_cliente, width=25)
        self.entry_nombre.grid(row=0, column=1, pady=8)

        tk.Label(ventana_cliente, text="Apellido:").grid(row=1, column=0, pady=8, sticky="w")
        self.entry_apellido = ttk.Entry(ventana_cliente, width=25)
        self.entry_apellido.grid(row=1, column=1, pady=8)

        tk.Label(ventana_cliente, text="Rut:").grid(row=2, column=0, pady=8, sticky="w")
        self.entry_rut = ttk.Entry(ventana_cliente, width=25)
        self.entry_rut.grid(row=2, column=1, pady=8)

        tk.Label(ventana_cliente, text="Teléfono:").grid(row=3, column=0, pady=8, sticky="w")
        self.entry_telefono = ttk.Entry(ventana_cliente, width=25)
        self.entry_telefono.grid(row=3, column=1, pady=8)

        tk.Button(ventana_cliente, text="Guardar Cliente", command=self.insertar_datos_cliente, bg="#4CAF50", fg="white", width=15).grid(row=4, column=0, columnspan=2, pady=20)

    def insertar_datos_cliente(self):
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        rut = self.entry_rut.get().strip()
        telefono = self.entry_telefono.get().strip()

        if not all([nombre, apellido, rut, telefono]):
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return
            
        try:
            self.cursor.execute("INSERT INTO cliente (nombre, apellido, rut, telefono) VALUES (%s, %s, %s, %s)", (nombre, apellido, rut, telefono))
            self.conexion.commit()
            messagebox.showinfo("Éxito", "Registro guardado correctamente")
            self.entry_nombre.delete(0, tk.END)
            self.entry_apellido.delete(0, tk.END)
            self.entry_rut.delete(0, tk.END)
            self.entry_telefono.delete(0, tk.END)
        except Error as e:
            self.conexion.rollback()
            messagebox.showerror("Error de Base de Datos", str(e))

    # --- LIBRO ---
    def libro_insertar(self):
        ventana_libro = tk.Toplevel(self.root)
        ventana_libro.title("Insertar Libro")
        ventana_libro.geometry("380x480")
        ventana_libro.config(padx=20, pady=20, bg=self.color_fondo)

        self.mostrar_campos_autor = False
        self.mostrar_campos_editorial = False

        tk.Label(ventana_libro, text="Título:").grid(row=0, column=0, pady=6, sticky="w")
        self.entry_titulo = ttk.Entry(ventana_libro, width=25)
        self.entry_titulo.grid(row=0, column=1, pady=6)

        tk.Label(ventana_libro, text="Autor (Nombre Ap):").grid(row=1, column=0, pady=6, sticky="w")
        self.entry_autor = ttk.Entry(ventana_libro, width=25)
        self.entry_autor.grid(row=1, column=1, pady=6)

        tk.Label(ventana_libro, text="Categoría:").grid(row=2, column=0, pady=6, sticky="w")
        self.entry_categoria = ttk.Entry(ventana_libro, width=25)
        self.entry_categoria.grid(row=2, column=1, pady=6)

        tk.Label(ventana_libro, text="Editorial:").grid(row=3, column=0, pady=6, sticky="w")
        self.entry_editorial = ttk.Entry(ventana_libro, width=25)
        self.entry_editorial.grid(row=3, column=1, pady=6)

        tk.Label(ventana_libro, text="Saga (Opcional):").grid(row=4, column=0, pady=6, sticky="w")
        self.entry_saga = ttk.Entry(ventana_libro, width=25)
        self.entry_saga.grid(row=4, column=1, pady=6)

        tk.Label(ventana_libro, text="Año publicación:").grid(row=5, column=0, pady=6, sticky="w")
        self.entry_ano_publicacion = ttk.Entry(ventana_libro, width=25)
        self.entry_ano_publicacion.grid(row=5, column=1, pady=6)

        tk.Label(ventana_libro, text="Precio:").grid(row=6, column=0, pady=6, sticky="w")
        self.entry_precio = ttk.Entry(ventana_libro, width=25)
        self.entry_precio.grid(row=6, column=1, pady=6)

        tk.Label(ventana_libro, text="Estante:").grid(row=7, column=0, pady=6, sticky="w")
        self.entry_estante = ttk.Entry(ventana_libro, width=25)
        self.entry_estante.grid(row=7, column=1, pady=6)

        # Campos extra
        self.lbl_nacionalidad = tk.Label(ventana_libro, text="Nac. Autor:", fg="#1976D2")
        self.entry_nacionalidad = ttk.Entry(ventana_libro, width=25)
        self.lbl_pais = tk.Label(ventana_libro, text="País Edit.:", fg="#1976D2")
        self.entry_pais = ttk.Entry(ventana_libro, width=25)
        self.lbl_telefono_ed = tk.Label(ventana_libro, text="Tel. Edit.:", fg="#1976D2")
        self.entry_telefono_ed = ttk.Entry(ventana_libro, width=25)
        self.lbl_correo = tk.Label(ventana_libro, text="Correo Edit.:", fg="#1976D2")
        self.entry_correo = ttk.Entry(ventana_libro, width=25)

        self.btn_guardar_libro = tk.Button(ventana_libro, text="Guardar Libro", command=lambda: self.insertar_datos_libro(ventana_libro), bg="#4CAF50", fg="white", width=15)
        self.btn_guardar_libro.grid(row=8, column=0, columnspan=2, pady=20)

    def insertar_datos_libro(self, ventana_libro):
        titulo = self.entry_titulo.get().strip()
        autor_texto = self.entry_autor.get().strip()
        categoria_texto = self.entry_categoria.get().strip()
        editorial_texto = self.entry_editorial.get().strip()
        saga_texto = self.entry_saga.get().strip()
        anio_publicacion = self.entry_ano_publicacion.get().strip()
        precio = self.entry_precio.get().strip()
        estante = self.entry_estante.get().strip()

        if not all([titulo, autor_texto, categoria_texto, editorial_texto, anio_publicacion, precio, estante]):
            messagebox.showwarning("Error", "Todos los campos principales son obligatorios (excepto Saga)")
            return

        try:
            partes = autor_texto.split(" ", 1)
            nombre_a = partes[0]
            apellido_a = partes[1] if len(partes) > 1 else ""

            self.cursor.execute("SELECT id_autor FROM autor WHERE nombre = %s AND apellido = %s", (nombre_a, apellido_a))
            res_autor = self.cursor.fetchone()

            self.cursor.execute("SELECT id_editorial FROM editorial WHERE nombre = %s", (editorial_texto,))
            res_editorial = self.cursor.fetchone()

            necesita_mas_info = False

            if not res_autor:
                if not self.mostrar_campos_autor:
                    self.lbl_nacionalidad.grid(row=9, column=0, pady=5, sticky="w")
                    self.entry_nacionalidad.grid(row=9, column=1, pady=5)
                    self.mostrar_campos_autor = True
                    necesita_mas_info = True
                elif not self.entry_nacionalidad.get().strip():
                    messagebox.showwarning("Falta Información", "Por favor introduce la nacionalidad del nuevo autor.")
                    return

            if not res_editorial:
                if not self.mostrar_campos_editorial:
                    self.lbl_pais.grid(row=10, column=0, pady=5, sticky="w")
                    self.entry_pais.grid(row=10, column=1, pady=5)
                    self.lbl_telefono_ed.grid(row=11, column=0, pady=5, sticky="w")
                    self.entry_telefono_ed.grid(row=11, column=1, pady=5)
                    self.lbl_correo.grid(row=12, column=0, pady=5, sticky="w")
                    self.entry_correo.grid(row=12, column=1, pady=5)
                    self.mostrar_campos_editorial = True
                    necesita_mas_info = True
                elif not all([self.entry_pais.get().strip(), self.entry_telefono_ed.get().strip(), self.entry_correo.get().strip()]):
                    messagebox.showwarning("Falta Información", "Por favor completa todos los datos de la nueva editorial.")
                    return

            if necesita_mas_info:
                ventana_libro.geometry("380x680")
                self.btn_guardar_libro.grid(row=13, column=0, columnspan=2, pady=20)
                messagebox.showinfo("Campos Adicionales", "Autor o editorial nuevos. Completa las casillas adicionales desplegadas.")
                return

            if not res_autor:
                self.cursor.execute("INSERT INTO autor (nombre, apellido, nacionalidad) VALUES (%s, %s, %s) RETURNING id_autor", (nombre_a, apellido_a, self.entry_nacionalidad.get().strip()))
                id_autor = self.cursor.fetchone()[0]
            else: id_autor = res_autor[0]

            if not res_editorial:
                self.cursor.execute("INSERT INTO editorial (nombre, pais, telefono, correo) VALUES (%s, %s, %s, %s) RETURNING id_editorial", (editorial_texto, self.entry_pais.get().strip(), self.entry_telefono_ed.get().strip(), self.entry_correo.get().strip()))
                id_editorial = self.cursor.fetchone()[0]
            else: id_editorial = res_editorial[0]

            self.cursor.execute("SELECT id_categoria FROM categoria WHERE tipo = %s", (categoria_texto,))
            res_cat = self.cursor.fetchone()
            if res_cat: id_categoria = res_cat[0]
            else:
                self.cursor.execute("INSERT INTO categoria (tipo) VALUES (%s) RETURNING id_categoria", (categoria_texto,))
                id_categoria = self.cursor.fetchone()[0]

            id_saga = None
            if saga_texto:
                self.cursor.execute("SELECT id_saga FROM sagas WHERE nombre = %s", (saga_texto,))
                res_saga = self.cursor.fetchone()
                if res_saga: id_saga = res_saga[0]
                else:
                    self.cursor.execute("INSERT INTO sagas (nombre, cantidad_libros) VALUES (%s, 1) RETURNING id_saga", (saga_texto,))
                    id_saga = self.cursor.fetchone()[0]

            self.cursor.execute("INSERT INTO libro (id_autor, id_categoria, id_editorial, id_saga, titulo, anio_publicacion, precio, estante) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (id_autor, id_categoria, id_editorial, id_saga, titulo, anio_publicacion, precio, estante))
            self.conexion.commit()

            messagebox.showinfo("Éxito", "Libro registrado correctamente.")
            ventana_libro.destroy()

        except Error as e:
            self.conexion.rollback()
            messagebox.showerror("Error de Base de Datos", str(e))
    
    # --- EMPLEADO ---
    def empleado_insertar(self):
        ventana_emp = tk.Toplevel(self.root)
        ventana_emp.title("Insertar Empleado")
        ventana_emp.geometry("380x450")
        ventana_emp.config(padx=20, pady=20, bg=self.color_fondo)

        self.mostrar_campos_sucursal = False
        self.mostrar_campos_contrato = False

        tk.Label(ventana_emp, text="RUT Empleado:").grid(row=0, column=0, pady=6, sticky="w")
        self.entry_emp_rut = ttk.Entry(ventana_emp, width=25)
        self.entry_emp_rut.grid(row=0, column=1, pady=6)

        tk.Label(ventana_emp, text="Nombre:").grid(row=1, column=0, pady=6, sticky="w")
        self.entry_emp_nombre = ttk.Entry(ventana_emp, width=25)
        self.entry_emp_nombre.grid(row=1, column=1, pady=6)

        tk.Label(ventana_emp, text="Apellido:").grid(row=2, column=0, pady=6, sticky="w")
        self.entry_emp_apellido = ttk.Entry(ventana_emp, width=25)
        self.entry_emp_apellido.grid(row=2, column=1, pady=6)

        tk.Label(ventana_emp, text="Rol:").grid(row=3, column=0, pady=6, sticky="w")
        self.entry_emp_rol = ttk.Entry(ventana_emp, width=25)
        self.entry_emp_rol.grid(row=3, column=1, pady=6)

        tk.Label(ventana_emp, text="Tipo Turno:").grid(row=4, column=0, pady=6, sticky="w")
        self.entry_emp_turno = ttk.Entry(ventana_emp, width=25)
        self.entry_emp_turno.grid(row=4, column=1, pady=6)

        tk.Label(ventana_emp, text="Sucursal:").grid(row=5, column=0, pady=6, sticky="w")
        self.entry_emp_sucursal = ttk.Entry(ventana_emp, width=25)
        self.entry_emp_sucursal.grid(row=5, column=1, pady=6)

        tk.Label(ventana_emp, text="Contrato (Tipo):").grid(row=6, column=0, pady=6, sticky="w")
        self.entry_emp_contrato = ttk.Entry(ventana_emp, width=25)
        self.entry_emp_contrato.grid(row=6, column=1, pady=6)

        self.lbl_suc_dir = tk.Label(ventana_emp, text="Dir. Sucursal:", fg="#1976D2")
        self.entry_suc_dir = ttk.Entry(ventana_emp, width=25)
        self.lbl_suc_com = tk.Label(ventana_emp, text="Comuna Suc.:", fg="#1976D2")
        self.entry_suc_com = ttk.Entry(ventana_emp, width=25)

        self.lbl_con_fecha = tk.Label(ventana_emp, text="Inicio (YYYY-MM-DD):", fg="#1976D2")
        self.entry_con_fecha = ttk.Entry(ventana_emp, width=25)
        self.lbl_con_salario = tk.Label(ventana_emp, text="Salario:", fg="#1976D2")
        self.entry_con_salario = ttk.Entry(ventana_emp, width=25)

        self.btn_guardar_emp = tk.Button(ventana_emp, text="Guardar", command=lambda: self.insertar_datos_empleado(ventana_emp), bg="#4CAF50", fg="white", width=15)
        self.btn_guardar_emp.grid(row=7, column=0, columnspan=2, pady=20)

    def insertar_datos_empleado(self, ventana_emp):
        rut = self.entry_emp_rut.get().strip()
        nombre = self.entry_emp_nombre.get().strip()
        apellido = self.entry_emp_apellido.get().strip()
        rol = self.entry_emp_rol.get().strip()
        turno = self.entry_emp_turno.get().strip()
        sucursal = self.entry_emp_sucursal.get().strip()
        contrato = self.entry_emp_contrato.get().strip()

        if not all([rut, nombre, apellido, rol, turno, sucursal, contrato]):
            messagebox.showwarning("Error", "Todos los campos principales son obligatorios.")
            return

        try:
            self.cursor.execute("SELECT id_sucursal FROM sucursal WHERE nombre = %s", (sucursal,))
            res_suc = self.cursor.fetchone()
            self.cursor.execute("SELECT id_contrato FROM contrato WHERE tipo = %s", (contrato,))
            res_con = self.cursor.fetchone()

            necesita_mas_info = False

            if not res_suc:
                if not self.mostrar_campos_sucursal:
                    self.lbl_suc_dir.grid(row=8, column=0, pady=5, sticky="w")
                    self.entry_suc_dir.grid(row=8, column=1, pady=5)
                    self.lbl_suc_com.grid(row=9, column=0, pady=5, sticky="w")
                    self.entry_suc_com.grid(row=9, column=1, pady=5)
                    self.mostrar_campos_sucursal = True
                    necesita_mas_info = True
                elif not all([self.entry_suc_dir.get().strip(), self.entry_suc_com.get().strip()]):
                    messagebox.showwarning("Falta Información", "Completa la dirección y comuna de la sucursal.")
                    return

            if not res_con:
                if not self.mostrar_campos_contrato:
                    self.lbl_con_fecha.grid(row=10, column=0, pady=5, sticky="w")
                    self.entry_con_fecha.grid(row=10, column=1, pady=5)
                    self.lbl_con_salario.grid(row=11, column=0, pady=5, sticky="w")
                    self.entry_con_salario.grid(row=11, column=1, pady=5)
                    self.mostrar_campos_contrato = True
                    necesita_mas_info = True
                elif not all([self.entry_con_fecha.get().strip(), self.entry_con_salario.get().strip()]):
                    messagebox.showwarning("Falta Información", "Completa la fecha de inicio y salario del contrato.")
                    return

            if necesita_mas_info:
                ventana_emp.geometry("380x650")
                self.btn_guardar_emp.grid(row=12, column=0, columnspan=2, pady=20)
                messagebox.showinfo("Información Faltante", "Sucursal o Contrato nuevos. Completa los campos desplegados.")
                return

            if not res_suc:
                self.cursor.execute("INSERT INTO sucursal (nombre, direccion, comuna) VALUES (%s, %s, %s) RETURNING id_sucursal", (sucursal, self.entry_suc_dir.get().strip(), self.entry_suc_com.get().strip()))
                id_sucursal = self.cursor.fetchone()[0]
            else: id_sucursal = res_suc[0]

            if not res_con:
                self.cursor.execute("INSERT INTO contrato (fecha_inicio, tipo, salario) VALUES (%s, %s, %s) RETURNING id_contrato", (self.entry_con_fecha.get().strip(), contrato, self.entry_con_salario.get().strip()))
                id_contrato = self.cursor.fetchone()[0]
            else: id_contrato = res_con[0]

            self.cursor.execute("INSERT INTO empleado (id_contrato, id_sucursal, tipo_turno, rol, nombre, apellido, rut) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (id_contrato, id_sucursal, turno, rol, nombre, apellido, rut))
            self.conexion.commit()
            messagebox.showinfo("Éxito", "Empleado registrado correctamente.")
            ventana_emp.destroy()

        except Error as e:
            self.conexion.rollback()
            messagebox.showerror("Error DB", str(e))

    # --- VENTA ---
    def venta_insertar(self):
        ventana_ven = tk.Toplevel(self.root)
        ventana_ven.title("Registrar Venta")
        ventana_ven.geometry("350x400")
        ventana_ven.config(padx=20, pady=20, bg=self.color_fondo)

        self.mostrar_campos_cliente = False

        tk.Label(ventana_ven, text="RUT Cliente:").grid(row=0, column=0, pady=6, sticky="w")
        self.entry_ven_rut = ttk.Entry(ventana_ven, width=25)
        self.entry_ven_rut.grid(row=0, column=1, pady=6)

        tk.Label(ventana_ven, text="Número Caja:").grid(row=1, column=0, pady=6, sticky="w")
        self.entry_ven_caja = ttk.Entry(ventana_ven, width=25)
        self.entry_ven_caja.grid(row=1, column=1, pady=6)

        tk.Label(ventana_ven, text="ID Cajero:").grid(row=2, column=0, pady=6, sticky="w")
        self.entry_ven_cajero = ttk.Entry(ventana_ven, width=25)
        self.entry_ven_cajero.grid(row=2, column=1, pady=6)

        tk.Label(ventana_ven, text="Fecha/Hora:").grid(row=3, column=0, pady=6, sticky="w")
        self.entry_ven_fecha = ttk.Entry(ventana_ven, width=25)
        self.entry_ven_fecha.grid(row=3, column=1, pady=6)

        tk.Label(ventana_ven, text="Total:").grid(row=4, column=0, pady=6, sticky="w")
        self.entry_ven_total = ttk.Entry(ventana_ven, width=25)
        self.entry_ven_total.grid(row=4, column=1, pady=6)

        self.lbl_cli_nom = tk.Label(ventana_ven, text="Nom. Cliente:", fg="#1976D2")
        self.entry_cli_nom = ttk.Entry(ventana_ven, width=25)
        self.lbl_cli_ape = tk.Label(ventana_ven, text="Ape. Cliente:", fg="#1976D2")
        self.entry_cli_ape = ttk.Entry(ventana_ven, width=25)
        self.lbl_cli_tel = tk.Label(ventana_ven, text="Tel. Cliente:", fg="#1976D2")
        self.entry_cli_tel = ttk.Entry(ventana_ven, width=25)

        self.btn_guardar_ven = tk.Button(ventana_ven, text="Registrar Venta", command=lambda: self.insertar_datos_venta(ventana_ven), bg="#4CAF50", fg="white", width=15)
        self.btn_guardar_ven.grid(row=5, column=0, columnspan=2, pady=20)

    def insertar_datos_venta(self, ventana_ven):
        rut_cliente = self.entry_ven_rut.get().strip()
        num_caja = self.entry_ven_caja.get().strip()
        id_cajero = self.entry_ven_cajero.get().strip()
        fecha_hora = self.entry_ven_fecha.get().strip()
        total = self.entry_ven_total.get().strip()

        if not all([rut_cliente, num_caja, id_cajero, fecha_hora, total]):
            messagebox.showwarning("Error", "Todos los campos de la venta son obligatorios.")
            return

        try:
            self.cursor.execute("SELECT id_cajero FROM cajero WHERE id_cajero = %s", (id_cajero,))
            if not self.cursor.fetchone():
                messagebox.showerror("Error", "El ID de Cajero ingresado no existe.")
                return

            self.cursor.execute("SELECT id_caja FROM caja WHERE numero_caja = %s", (num_caja,))
            res_caja = self.cursor.fetchone()
            if not res_caja:
                messagebox.showerror("Error", "El Número de Caja no existe en el sistema.")
                return
            id_caja = res_caja[0]

            self.cursor.execute("SELECT id_cliente FROM cliente WHERE rut = %s", (rut_cliente,))
            res_cli = self.cursor.fetchone()

            if not res_cli:
                if not self.mostrar_campos_cliente:
                    self.lbl_cli_nom.grid(row=6, column=0, pady=5, sticky="w")
                    self.entry_cli_nom.grid(row=6, column=1, pady=5)
                    self.lbl_cli_ape.grid(row=7, column=0, pady=5, sticky="w")
                    self.entry_cli_ape.grid(row=7, column=1, pady=5)
                    self.lbl_cli_tel.grid(row=8, column=0, pady=5, sticky="w")
                    self.entry_cli_tel.grid(row=8, column=1, pady=5)
                    self.mostrar_campos_cliente = True
                    ventana_ven.geometry("350x550")
                    self.btn_guardar_ven.grid(row=9, column=0, columnspan=2, pady=20)
                    messagebox.showinfo("Cliente Nuevo", "El RUT no está registrado. Ingresa los datos del nuevo cliente.")
                    return
                else:
                    nom = self.entry_cli_nom.get().strip()
                    ape = self.entry_cli_ape.get().strip()
                    tel = self.entry_cli_tel.get().strip()
                    if not all([nom, ape, tel]):
                        messagebox.showwarning("Falta Información", "Completa todos los datos del nuevo cliente.")
                        return
                    self.cursor.execute("INSERT INTO cliente (nombre, apellido, rut, telefono) VALUES (%s, %s, %s, %s) RETURNING id_cliente", (nom, ape, rut_cliente, tel))
                    id_cliente = self.cursor.fetchone()[0]
            else: id_cliente = res_cli[0]

            self.cursor.execute("INSERT INTO venta (id_cliente, id_caja, id_cajero, fecha_hora, total) VALUES (%s, %s, %s, %s, %s)", (id_cliente, id_caja, id_cajero, fecha_hora, total))
            self.conexion.commit()
            messagebox.showinfo("Éxito", "Venta registrada correctamente.")
            ventana_ven.destroy()

        except Error as e:
            self.conexion.rollback()
            messagebox.showerror("Error DB", str(e))

    # =========================================================
    # MENÚ ELIMINAR
    # =========================================================
    def menu_eliminar(self):
        ventana_eliminar = tk.Toplevel(self.root)
        ventana_eliminar.title("Menú Eliminar")
        ventana_eliminar.geometry("300x350")
        ventana_eliminar.config(padx=20, pady=20, bg=self.color_fondo)

        tk.Label(ventana_eliminar, text="¿Qué deseas eliminar?", font=("Helvetica", 12, "bold")).grid(row=0, column=0, pady=(0,15))

        tk.Button(ventana_eliminar, text="Eliminar Cliente", command=self.cliente_eliminar, bg="#F44336", fg="white", width=20).grid(row=1, column=0, pady=10)
        tk.Button(ventana_eliminar, text="Eliminar Libro", command=self.libro_eliminar, bg="#F44336", fg="white", width=20).grid(row=2, column=0, pady=10)
        tk.Button(ventana_eliminar, text="Eliminar Empleado", command=self.empleado_eliminar, bg="#F44336", fg="white", width=20).grid(row=3, column=0, pady=10)
        tk.Button(ventana_eliminar, text="Eliminar Venta", command=self.venta_eliminar, bg="#F44336", fg="white", width=20).grid(row=4, column=0, pady=10)

    def cliente_eliminar(self): self.crear_ventana_eliminacion("Cliente", "rut", "cliente")
    def empleado_eliminar(self): self.crear_ventana_eliminacion("Empleado", "rut", "empleado")
    def venta_eliminar(self): self.crear_ventana_eliminacion("Venta", "id_venta", "venta")

    def crear_ventana_eliminacion(self, entidad, campo_id, tabla):
        ventana_del = tk.Toplevel(self.root)
        ventana_del.title(f"Eliminar {entidad}")
        ventana_del.geometry("300x150")
        ventana_del.config(padx=20, pady=20, bg=self.color_fondo)

        tk.Label(ventana_del, text=f"{campo_id.capitalize()}:").grid(row=0, column=0, pady=10, sticky="w")
        entry_id = ttk.Entry(ventana_del)
        entry_id.grid(row=0, column=1, pady=10)

        tk.Button(ventana_del, text="Confirmar", command=lambda: self.ejecutar_eliminar(ventana_del, tabla, campo_id, entry_id.get().strip()), bg="#F44336", fg="white").grid(row=1, column=0, columnspan=2, pady=20)

    def ejecutar_eliminar(self, ventana, tabla, campo_id, valor_id):
        if not valor_id:
            messagebox.showwarning("Error", f"Por favor, ingresa un {campo_id} válido.")
            return
        if messagebox.askyesno("Confirmar", f"¿Seguro que deseas eliminar de {tabla} donde {campo_id} = '{valor_id}'?"):
            try:
                self.cursor.execute(f"DELETE FROM {tabla} WHERE {campo_id} = %s", (valor_id,))
                if self.cursor.rowcount > 0:
                    self.conexion.commit()
                    messagebox.showinfo("Éxito", f"Registro eliminado.")
                    ventana.destroy()
                else:
                    messagebox.showwarning("Aviso", "No se encontró ningún registro.")
            except Error as e:
                self.conexion.rollback()
                messagebox.showerror("Error", f"No se pudo eliminar.\nDetalle: {e}")

    # =========================================================
    # MENÚ ACTUALIZAR
    # =========================================================
    def menu_actualizar(self):
        ventana_act = tk.Toplevel(self.root)
        ventana_act.title("Menú Actualizar")
        ventana_act.geometry("300x200")
        ventana_act.config(padx=20, pady=20, bg=self.color_fondo)

        tk.Label(ventana_act, text="¿Qué deseas actualizar?", font=("Helvetica", 12, "bold")).grid(row=0, column=0, pady=(0,15))
        tk.Button(ventana_act, text="Actualizar Cliente", command=self.cliente_actualizar, bg="#FFC107", fg="black", width=20).grid(row=1, column=0, pady=10)
        tk.Button(ventana_act, text="Actualizar Libro", command=self.libro_actualizar, bg="#FFC107", fg="black", width=20).grid(row=2, column=0, pady=10)

    def cliente_actualizar(self):
        ventana_upd_cli = tk.Toplevel(self.root)
        ventana_upd_cli.title("Actualizar Cliente")
        ventana_upd_cli.geometry("350x320")
        ventana_upd_cli.config(padx=20, pady=20, bg=self.color_fondo)

        tk.Label(ventana_upd_cli, text="RUT a buscar:").grid(row=0, column=0, pady=5, sticky="w")
        entry_rut_buscar = ttk.Entry(ventana_upd_cli)
        entry_rut_buscar.grid(row=0, column=1, pady=5)

        tk.Label(ventana_upd_cli, text="--- Nuevos Datos ---", font=("Helvetica", 10, "bold")).grid(row=2, column=0, columnspan=2, pady=15)
        
        tk.Label(ventana_upd_cli, text="Nombre:").grid(row=3, column=0, pady=6, sticky="w")
        entry_nom = ttk.Entry(ventana_upd_cli)
        entry_nom.grid(row=3, column=1, pady=6)

        tk.Label(ventana_upd_cli, text="Apellido:").grid(row=4, column=0, pady=6, sticky="w")
        entry_ape = ttk.Entry(ventana_upd_cli)
        entry_ape.grid(row=4, column=1, pady=6)

        tk.Label(ventana_upd_cli, text="Teléfono:").grid(row=5, column=0, pady=6, sticky="w")
        entry_tel = ttk.Entry(ventana_upd_cli)
        entry_tel.grid(row=5, column=1, pady=6)

        def cargar_datos_cliente():
            rut = entry_rut_buscar.get().strip()
            self.cursor.execute("SELECT nombre, apellido, telefono FROM cliente WHERE rut = %s", (rut,))
            cliente = self.cursor.fetchone()
            if cliente:
                entry_nom.delete(0, tk.END); entry_nom.insert(0, cliente[0])
                entry_ape.delete(0, tk.END); entry_ape.insert(0, cliente[1])
                entry_tel.delete(0, tk.END); entry_tel.insert(0, cliente[2] if cliente[2] else "")
            else: messagebox.showwarning("No encontrado", "No existe cliente con ese RUT.")

        def guardar_cambios_cliente():
            try:
                self.cursor.execute("UPDATE cliente SET nombre=%s, apellido=%s, telefono=%s WHERE rut=%s",
                    (entry_nom.get().strip(), entry_ape.get().strip(), entry_tel.get().strip(), entry_rut_buscar.get().strip()))
                if self.cursor.rowcount > 0:
                    self.conexion.commit()
                    messagebox.showinfo("Éxito", "Cliente actualizado.")
                    ventana_upd_cli.destroy()
            except Error as e:
                self.conexion.rollback()
                messagebox.showerror("Error", str(e))

        tk.Button(ventana_upd_cli, text="Buscar", command=cargar_datos_cliente, bg="#2196F3", fg="white").grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(ventana_upd_cli, text="Guardar Cambios", command=guardar_cambios_cliente, bg="#FFC107", fg="black").grid(row=6, column=0, columnspan=2, pady=20)

    # =========================================================
    # TABLA DE LIBROS (ELIMINAR / ACTUALIZAR)
    # =========================================================
    def libro_eliminar(self):
        self.mostrar_lista_libros("eliminar")

    def libro_actualizar(self):
        self.mostrar_lista_libros("actualizar")

    def mostrar_lista_libros(self, accion):
        ventana_lista = tk.Toplevel(self.root)
        ventana_lista.title(f"{accion.capitalize()} Libro")
        ventana_lista.geometry("620x450")
        ventana_lista.config(padx=15, pady=15, bg=self.color_fondo)

        paginacion = {"offset": 0, "limite": 10}

        frame_tabla = tk.Frame(ventana_lista, bg=self.color_fondo)
        frame_tabla.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        columnas = ("ID", "Título", "Año", "Precio", "Estante")
        tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", yscrollcommand=scrollbar.set)
        
        tree.heading("ID", text="ID")
        tree.column("ID", width=40, anchor="center")
        tree.heading("Título", text="Título")
        tree.column("Título", width=220)
        tree.heading("Año", text="Año")
        tree.column("Año", width=60, anchor="center")
        tree.heading("Precio", text="Precio")
        tree.column("Precio", width=80, anchor="center")
        tree.heading("Estante", text="Estante")
        tree.column("Estante", width=100, anchor="center")
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=tree.yview)

        frame_paginacion = tk.Frame(ventana_lista, bg=self.color_fondo)
        frame_paginacion.pack(pady=15)

        lbl_pagina = tk.Label(frame_paginacion, text="Página 1", font=("Helvetica", 10, "bold"))
        lbl_pagina.grid(row=0, column=1, padx=25)

        def cargar_datos():
            for item in tree.get_children(): tree.delete(item)
            try:
                self.cursor.execute("SELECT id_libro, titulo, anio_publicacion, precio, estante FROM libro ORDER BY id_libro ASC LIMIT %s OFFSET %s", (paginacion["limite"], paginacion["offset"]))
                filas = self.cursor.fetchall()
                for fila in filas: tree.insert("", tk.END, values=fila)
                
                lbl_pagina.config(text=f"Página {(paginacion['offset'] // paginacion['limite']) + 1}")
                btn_anterior.config(state="normal" if paginacion["offset"] > 0 else "disabled")
                btn_siguiente.config(state="normal" if len(filas) == paginacion["limite"] else "disabled")
            except Error as e: messagebox.showerror("Error", f"Error al cargar datos:\n{e}")

        def ir_anterior():
            if paginacion["offset"] >= paginacion["limite"]:
                paginacion["offset"] -= paginacion["limite"]
                cargar_datos()

        def ir_siguiente():
            paginacion["offset"] += paginacion["limite"]
            cargar_datos()

        btn_anterior = tk.Button(frame_paginacion, text="< Anterior", command=ir_anterior, bg="#ddd", fg="black")
        btn_anterior.grid(row=0, column=0)
        btn_siguiente = tk.Button(frame_paginacion, text="Siguiente >", command=ir_siguiente, bg="#ddd", fg="black")
        btn_siguiente.grid(row=0, column=2)

        def ejecutar_accion():
            seleccion = tree.selection()
            if not seleccion:
                messagebox.showwarning("Aviso", "Seleccione un libro haciendo clic en la lista.")
                return
            
            item = tree.item(seleccion[0])
            id_libro = item["values"][0]
            titulo = item["values"][1]

            if accion == "eliminar":
                if messagebox.askyesno("Confirmar", f"¿Eliminar el libro:\n'{titulo}'?"):
                    try:
                        self.cursor.execute("DELETE FROM libro WHERE id_libro = %s", (id_libro,))
                        self.conexion.commit()
                        messagebox.showinfo("Éxito", "Libro eliminado.")
                        if len(tree.get_children()) == 1 and paginacion["offset"] > 0: paginacion["offset"] -= paginacion["limite"]
                        cargar_datos() 
                    except Error as e:
                        self.conexion.rollback()
                        messagebox.showerror("Error", str(e))
            elif accion == "actualizar":
                self.abrir_formulario_actualizar_libro(id_libro, cargar_datos)

        texto_btn = "Eliminar Seleccionado" if accion == "eliminar" else "Actualizar Seleccionado"
        color_btn = "#F44336" if accion == "eliminar" else "#FFC107"
        color_texto = "white" if accion == "eliminar" else "black"

        tk.Button(ventana_lista, text=texto_btn, command=ejecutar_accion, bg=color_btn, fg=color_texto, width=25).pack(pady=5)
        cargar_datos()

    def abrir_formulario_actualizar_libro(self, id_libro, callback_recargar_tabla):
        ventana_upd = tk.Toplevel(self.root)
        ventana_upd.title(f"Actualizando ID: {id_libro}")
        ventana_upd.geometry("320x260")
        ventana_upd.config(padx=20, pady=20, bg=self.color_fondo)

        self.cursor.execute("SELECT titulo, anio_publicacion, precio, estante FROM libro WHERE id_libro = %s", (id_libro,))
        libro = self.cursor.fetchone()

        tk.Label(ventana_upd, text="Título:").grid(row=0, column=0, pady=6, sticky="w")
        entry_titulo = ttk.Entry(ventana_upd, width=25)
        entry_titulo.insert(0, libro[0])
        entry_titulo.grid(row=0, column=1, pady=6)

        tk.Label(ventana_upd, text="Año Pub.:").grid(row=1, column=0, pady=6, sticky="w")
        entry_anio = ttk.Entry(ventana_upd, width=25)
        entry_anio.insert(0, libro[1])
        entry_anio.grid(row=1, column=1, pady=6)

        tk.Label(ventana_upd, text="Precio:").grid(row=2, column=0, pady=6, sticky="w")
        entry_precio = ttk.Entry(ventana_upd, width=25)
        entry_precio.insert(0, libro[2])
        entry_precio.grid(row=2, column=1, pady=6)

        tk.Label(ventana_upd, text="Estante:").grid(row=3, column=0, pady=6, sticky="w")
        entry_estante = ttk.Entry(ventana_upd, width=25)
        entry_estante.insert(0, libro[3])
        entry_estante.grid(row=3, column=1, pady=6)

        def guardar():
            try:
                self.cursor.execute("UPDATE libro SET titulo=%s, anio_publicacion=%s, precio=%s, estante=%s WHERE id_libro=%s",
                    (entry_titulo.get().strip(), entry_anio.get().strip(), entry_precio.get().strip(), entry_estante.get().strip(), id_libro))
                self.conexion.commit()
                messagebox.showinfo("Éxito", "Cambios guardados.")
                ventana_upd.destroy()
                callback_recargar_tabla() 
            except Error as e:
                self.conexion.rollback()
                messagebox.showerror("Error", str(e))

        tk.Button(ventana_upd, text="Guardar Cambios", command=guardar, bg="#4CAF50", fg="white", width=15).grid(row=4, column=0, columnspan=2, pady=20)

if __name__ == "__main__":
    ventana = tk.Tk()
    app = AppCRUD(ventana)
    ventana.mainloop()