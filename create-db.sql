CREATE TABLE cliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100),
    rut VARCHAR(12) UNIQUE NOT NULL,
    telefono VARCHAR(15)
);

CREATE TABLE sucursal (
    id_sucursal SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(150),
    comuna VARCHAR(100)
);

CREATE TABLE caja (
    id_caja SERIAL PRIMARY KEY,
    id_sucursal INT NOT NULL,
    numero_caja INT NOT NULL,
    FOREIGN KEY (id_sucursal) REFERENCES sucursal(id_sucursal)
);

CREATE TYPE tipo_contrato AS ENUM ('plazo fijo', 'indefinido');
CREATE TABLE contrato (
    id_contrato SERIAL PRIMARY KEY,
    fecha_inicio DATE NOT NULL, 		
    tipo tipo_contrato,
    salario INT CHECK (salario >= 0)
);

CREATE TYPE empleado_tipo_turno AS ENUM ('fijo', 'rotativo');
CREATE TYPE empleado_rol AS ENUM ('cajero', 'reponedor');
CREATE TABLE empleado (
	id_empleado SERIAL PRIMARY KEY,
    id_contrato INT NOT NULL,	
    id_sucursal INT NOT NULL,
    tipo_turno empleado_tipo_turno NOT NULL,
    rol empleado_rol NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    rut VARCHAR(12) UNIQUE NOT NULL,
    FOREIGN KEY (id_contrato) REFERENCES contrato(id_contrato),
    FOREIGN KEY (id_sucursal) REFERENCES sucursal(id_sucursal)
);

CREATE TABLE cajero (
    id_cajero SERIAL PRIMARY KEY,
    id_empleado INT UNIQUE NOT NULL,
    FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado)
);

CREATE TABLE turno (
    id_turno SERIAL PRIMARY KEY,
    id_empleado INT NOT NULL,
    hora_ingreso TIME NOT NULL,
    hora_salida TIME NOT NULL,
    horas_trabajo DECIMAL(6, 4) NOT NULL CHECK (horas_trabajo >= 0),					
    cantidad_dias INT NOT NULL CHECK (cantidad_dias >= 0),
    FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado)
);

CREATE TABLE producto (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL CHECK (precio >= 0)
);

CREATE TABLE stockProducto (
    id_stock SERIAL PRIMARY KEY,
    id_sucursal INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad_stock INT NOT NULL CHECK (cantidad_stock >= 0),
    fecha_actualizacion TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES sucursal(id_sucursal),
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto),
    UNIQUE (id_sucursal, id_producto)
);

CREATE TABLE venta (
    id_venta SERIAL PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_caja INT NOT NULL,
    id_cajero INT NOT NULL,
    fecha_hora TIMESTAMP NOT NULL,
    total DECIMAL(10,2) NOT NULL CHECK (total >= 0),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_caja) REFERENCES caja(id_caja),
    FOREIGN KEY (id_cajero) REFERENCES cajero(id_cajero)
);

CREATE TABLE detalleventa (
    id_detalle SERIAL PRIMARY KEY,
    id_venta INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_venta) REFERENCES venta(id_venta) ON DELETE cascade,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto),
    UNIQUE (id_venta, id_producto)									
);

CREATE TABLE categoria (
    id_categoria SERIAL PRIMARY KEY,
    tipo VARCHAR(20)
);

CREATE TABLE autor (
    id_autor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    nacionalidad VARCHAR(100) NOT NULL
);

CREATE TABLE editorial (
    id_editorial SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    pais VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
	correo VARCHAR(50)    						
);

CREATE TABLE sagas (							
    id_saga SERIAL PRIMARY KEY,					
    nombre VARCHAR(100) NOT NULL,
    cantidad_libros INT NOT NULL CHECK (cantidad_libros > 0)
);

CREATE TABLE libro (
    id_libro SERIAL PRIMARY KEY,
    id_autor INT NOT NULL,
    id_categoria INT,
    id_editorial INT NOT NULL,
    id_saga INT,
    titulo VARCHAR(150) NOT NULL,
    anio_publicacion INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL CHECK (precio >= 0),
    estante VARCHAR(20),						
    FOREIGN KEY (id_autor) REFERENCES autor(id_autor),
    FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria),
    FOREIGN KEY (id_editorial) REFERENCES editorial(id_editorial),
    FOREIGN KEY (id_saga) REFERENCES sagas(id_saga)
);
