-- Dimensión Tiempo (Vital para análisis de tendencias)
CREATE TABLE dim_tiempo (
    id_tiempo INT PRIMARY KEY, -- Sugerencia: formato YYYYMMDD para llaves
    fecha DATE NOT NULL,
    anio INT NOT NULL,
    mes INT NOT NULL,
    nombre_mes VARCHAR(20),
    dia INT NOT NULL,
    trimestre INT,
    dia_semana VARCHAR(20)
);

-- Dimensión Producto (Unifica producto, libro, categoría, autor, editorial y saga)
CREATE TABLE dim_producto (
    id_producto INT PRIMARY KEY,
    nombre_producto VARCHAR(100) NOT NULL,
    tipo_item VARCHAR(50), -- Para diferenciar si es un 'Libro' u 'Otro producto'
    titulo_libro VARCHAR(150),
    categoria_libro VARCHAR(20),
    autor_nombre VARCHAR(200),
    nacionalidad_autor VARCHAR(100),
    editorial_nombre VARCHAR(100),
    saga_nombre VARCHAR(100),
    precio_referencial DECIMAL(10,2)
);

-- Dimensión Sucursal (Mantiene la ubicación)
CREATE TABLE dim_sucursal (
    id_sucursal INT PRIMARY KEY,
    nombre_sucursal VARCHAR(100) NOT NULL,
    direccion VARCHAR(150),
    comuna VARCHAR(100)
);

-- Dimensión Cliente
CREATE TABLE dim_cliente (
    id_cliente INT PRIMARY KEY,
    nombre_completo VARCHAR(200) NOT NULL,
    rut VARCHAR(12),
    telefono VARCHAR(15)
);

-- Dimensión Empleado (Unifica empleado y su rol al momento de la venta)
CREATE TABLE dim_empleado (
    id_empleado INT PRIMARY KEY,
    nombre_completo VARCHAR(200) NOT NULL,
    rut VARCHAR(12),
    rol VARCHAR(50),
    tipo_turno VARCHAR(50)
);

-- ==============================================================
-- NUEVA TABLA DE HECHOS: VENTAS
-- ==============================================================
CREATE TABLE hechos_ventas (
    id_hecho SERIAL PRIMARY KEY,
    id_tiempo INT NOT NULL,
    id_producto INT NOT NULL,
    id_sucursal INT NOT NULL,
    id_cliente INT NOT NULL,
    id_empleado INT NOT NULL, -- El cajero que realizó la venta
    
    -- Métricas / Medidas (Cuantificables)
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    
    -- Rastreabilidad para el proceso ETL (Upserts)
    id_venta_origen INT,
    id_detalle_origen INT UNIQUE,
    
    -- Llaves foráneas hacia las dimensiones
    FOREIGN KEY (id_tiempo) REFERENCES dim_tiempo(id_tiempo),
    FOREIGN KEY (id_producto) REFERENCES dim_producto(id_producto),
    FOREIGN KEY (id_sucursal) REFERENCES dim_sucursal(id_sucursal),
    FOREIGN KEY (id_cliente) REFERENCES dim_cliente(id_cliente),
    FOREIGN KEY (id_empleado) REFERENCES dim_empleado(id_empleado)
);