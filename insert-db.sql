-- ============================================
-- SCRIPT PARA POPULAR BASE DE DATOS - 4 AÑOS (2022-2025)
-- ============================================

-- ============================================
-- 1. CLIENTES (500)
-- ============================================
DO $$
DECLARE
    first_names TEXT[] := ARRAY[
		'Juan', 'María', 'Pedro', 'Ana', 'Luis', 'Carmen', 
		'José', 'Isabel', 'Carlos', 'Laura', 'Miguel', 'Sofía', 
		'Diego', 'Valentina', 'Jorge', 'Gabriela', 'Andrés', 'Fernanda', 
		'Ricardo', 'Daniela', 'Alejandro', 'Paula', 'Francisco', 'Martina', 
		'Javier', 'Camila', 'Roberto', 'Lucía', 'Fernando', 'Elena'
	];
    
	last_names TEXT[] := ARRAY[
		'González', 'Rodríguez', 'Martínez', 'López', 'Hernández', 'Pérez', 
		'García', 'Sánchez', 'Ramírez', 'Torres', 'Flores', 'Rivera', 
		'Morales', 'Ortiz', 'Cruz', 'Vargas', 'Reyes', 'Jiménez', 
		'Díaz', 'Moreno', 'Castillo', 'Alba', 'Gutierrez', 'Álvarez'
	];

    v_nombre 	VARCHAR;
    v_apellido 	VARCHAR;
    v_rut 		VARCHAR;
    v_telefono 	VARCHAR;
    i 			INT;
BEGIN
    FOR i IN 1..500 LOOP
        v_nombre := first_names[1 + floor(random() * array_length(first_names, 1))::INT];
        
		v_apellido := last_names[1 + floor(random() * array_length(last_names, 1))::INT];
    
		v_rut := to_char((8000000 + (random() * 15000000)::INT), 'FM99.999.999') || '-' || (random() * 9)::INT::TEXT;
        
        v_telefono := '+569' || (10000000 + (random() * 89999999)::INT)::TEXT;
        
        INSERT INTO cliente (nombre, apellido, rut, telefono)
        VALUES (v_nombre, v_apellido, v_rut, v_telefono);
    END LOOP;
END $$;

-- ============================================
-- 2. SUCURSALES (2)
-- ============================================
INSERT INTO sucursal (nombre, direccion, comuna) VALUES
    ('Sucursal Centro', 'Av. Libertador Bernardo OHiggins 1234', 'Santiago Centro'),
    ('Sucursal Providencia', 'Av. Providencia 2120', 'Providencia');

-- ============================================
-- 3. CAJAS (1-3 cajas por sucursal)
-- ============================================
DO $$
DECLARE
    suc RECORD;
    num_cajas INT;
    i INT;
BEGIN
    FOR suc IN SELECT id_sucursal FROM sucursal LOOP
        num_cajas := 1 + (random() * 2)::INT;
        FOR i IN 1..num_cajas LOOP
            INSERT INTO caja (id_sucursal, numero_caja) VALUES (suc.id_sucursal, i);
        END LOOP;
    END LOOP;
END $$;

-- ============================================
-- 4. CONTRATOS (para 12 empleados)
-- ============================================
DO $$
DECLARE
    v_tipo tipo_contrato;
    v_fecha_inicio DATE;
    i INT;
BEGIN
    FOR i IN 1..12 LOOP
        v_fecha_inicio := '2021-01-01'::DATE + (random() * 1460)::INT; -- 4 años = 1460 días
        IF v_fecha_inicio > '2025-12-31' THEN
            v_fecha_inicio := '2025-01-01'::DATE + (random() * 364)::INT;
        END IF;
        
        v_tipo := CASE WHEN random() < 0.7 THEN 'indefinido'::tipo_contrato ELSE 'plazo fijo'::tipo_contrato END;
        
        INSERT INTO contrato (fecha_inicio, tipo, salario)
        VALUES (v_fecha_inicio, v_tipo, 500000 + (random() * 800000)::INT);
    END LOOP;
END $$;

-- ============================================
-- 5. EMPLEADOS (12 - 9 cajeros, 3 reponedores)
-- ============================================
DO $$
DECLARE
    first_names TEXT[] := ARRAY[
		'Juan', 'Pedro', 'Diego', 'Carlos', 
		'Miguel', 'Luis', 'Jorge', 'Andrés', 
		'Alejandro', 'Francisco', 'María', 'Ana', 
		'Isabel', 'Laura', 'Carmen', 'Sofía', 
		'Valentina', 'Gabriela', 'Fernanda', 'Daniela'
	];

    last_names TEXT[] := ARRAY[
		'González', 'Rodríguez', 'Martínez', 'López', 'Hernández', 
		'Pérez', 'García', 'Sánchez', 'Ramírez', 'Torres'
	];

    v_nombre VARCHAR;
    v_apellido VARCHAR;
    v_rut VARCHAR;
    v_rol empleado_rol;
    v_tipo_turno empleado_tipo_turno;
    v_id_contrato INT;
    i INT;
BEGIN
    FOR i IN 1..12 LOOP
        v_nombre := first_names[1 + floor(random() * array_length(first_names, 1))::INT];
        
		v_apellido := last_names[1 + floor(random() * array_length(last_names, 1))::INT];
    
		v_rut := to_char((8000000 + (random() * 15000000)::INT), 'FM99.999.999') || '-' || (random() * 9)::INT::TEXT;
        
        -- 75% cajeros, 25% reponedores
        v_rol := CASE WHEN i <= 9 THEN 'cajero'::empleado_rol ELSE 'reponedor'::empleado_rol END;
        v_turno := CASE WHEN random() < 0.5 THEN 'fijo'::empleado_tipo_turno ELSE 'rotativo'::empleado_tipo_turno END;
        
        -- dar un contrato de manera aleatoria
        SELECT id_contrato INTO v_id_contrato FROM contrato ORDER BY random() LIMIT 1;
        
        INSERT INTO empleado (id_contrato, id_sucursal, tipo_turno, rol, nombre, apellido, rut)
        VALUES (v_id_contrato, 1 + (random() * 5)::INT, v_turno, v_rol, v_nombre, v_apellido, v_rut);
    END LOOP;
END $$;

-- ============================================
-- 6. CAJEROS 
-- ============================================
INSERT INTO cajero (id_empleado)
SELECT id_empleado FROM empleado WHERE rol = 'cajero';

-- ============================================
-- 7. TURNOS (para 12 empleados)
-- ============================================
DO $$
DECLARE
    emp RECORD;
    turno_count INT;
    v_tipo_turno empleado_tipo_turno;
    i INT;
BEGIN
    FOR emp IN SELECT e.id_empleado, e.tipo_turno FROM empleado e LOOP
        turno_count := 3 + (random() * 2)::INT; -- 3 a 5 turnos distintos para cada empleado
        
        FOR i IN 1..turno_count LOOP
            IF emp.tipo_turno = 'fijo' THEN
                -- Siempre las mismas horas
                INSERT INTO turno (id_empleado, hora_ingreso, hora_salida, horas_trabajo, cantidad_dias)
                VALUES (
                    emp.id_empleado,
                    '08:00'::TIME + (i * INTERVAL '1 hour'),
                    '08:00'::TIME + (i * INTERVAL '1 hour') + INTERVAL '8 hours',
                    8.0000,
                    5
                );
            ELSE
                -- Horas distintas
                INSERT INTO turno (id_empleado, hora_ingreso, hora_salida, horas_trabajo, cantidad_dias)
                VALUES (
                    emp.id_empleado,
                    ('06:00'::TIME + (random() * 8)::INT * INTERVAL '1 hour')::TIME,
                    ('14:00'::TIME + (random() * 8)::INT * INTERVAL '1 hour')::TIME,
                    (6 + (random() * 4))::DECIMAL(6,4),
                    (3 + (random() * 4))::INT
                );
            END IF;
        END LOOP;
    END LOOP;
END $$;

-- ============================================
-- 8. CATEGORIAS (10)
-- ============================================
INSERT INTO categoria (tipo) VALUES
    ('Ficción'), ('No Ficción'), ('Ciencia'), ('Historia'), ('Filosofía'),
    ('Infantil'), ('Autoayuda'), ('Biografía'), ('Poesía'), ('Terror');

-- ============================================
-- 9. AUTORES (50)
-- ============================================
DO $$
DECLARE
    first_names TEXT[] := ARRAY[
		'Gabriel', 'Jorge', 'Mario', 'Julio', 'Isabel', 
		'Pablo', 'Roberto', 'Octavio', 'Alejandra', 'Laura', 
		'Ernesto', 'Carlos', 'Miguel', 'Juan', 'María', 
		'José', 'Antonio', 'Federico', 'Alfonsina', 'Nicanor'
	];
    
	last_names TEXT[] := ARRAY[
		'García Márquez', 'Luis Borges', 'Vargas Llosa', 'Cortázar', 'Allende', 
		'Neruda', 'Bolaño', 'Paz', 'Pizarnik', 'Esquivel', 
		'Sábato', 'Fuentes', 'de Cervantes', 'Rulfo', 'Benedetti', 
		'Saramago', 'Skármeta', 'García Lorca', 'Storni', 'Parra'
	];

    countries TEXT[] := ARRAY[
		'Chile', 'Argentina', 'Perú', 'México', 'Colombia', 
		'España', 'Uruguay', 'Cuba', 'Brasil', 'Portugal', 
		'Francia', 'Inglaterra', 'Estados Unidos', 'Italia', 'Alemania', 
		'Rusia', 'Japón', 'China', 'India', 'Egipto'
	];

    v_nombre VARCHAR;
    v_apellido VARCHAR;
    i INT;
BEGIN
    FOR i IN 1..50 LOOP
        v_nombre := first_names[1 + floor(random() * array_length(first_names, 1))::INT];
        
		v_apellido := last_names[1 + floor(random() * array_length(last_names, 1))::INT];
        
        INSERT INTO autor (nombre, apellido, nacionalidad)
        VALUES (
            v_nombre,
            v_apellido,
            countries[1 + floor(random() * (array_length(countries, 1))::INT]
        );
    END LOOP;
END $$;

-- ============================================
-- 10. EDITORIALES (15)
-- ============================================
INSERT INTO editorial (nombre, pais, telefono, correo) VALUES
    ('Planeta', 'España', '+34911234567', 'info@planeta.es'),
    ('Penguin Random House', 'Estados Unidos', '+12125556789', 'contact@penguinrandomhouse.com'),
    ('Alfaguara', 'España', '+34911987654', 'alfaguara@alfaguara.es'),
    ('Sudamericana', 'Argentina', '+54114567890', 'sudamericana@edito.ar'),
    ('Fondo de Cultura Económica', 'México', '+52559876543', 'fce@fce.com.mx'),
    ('Anagrama', 'España', '+34932567890', 'anagrama@anagrama.es'),
    ('Eterna Cadencia', 'Argentina', '+54112345678', 'info@eternacadencia.com'),
    ('Seix Barral', 'España', '+34914567890', 'seixbarral@seixbarral.es'),
    ('Lumen', 'España', '+34913456789', 'lumen@lumen.es'),
    ('Tusquets', 'España', '+34914561234', 'tusquets@tusquets.es'),
    ('Editorial Universitaria', 'Chile', '+56223456789', 'universitaria@edit.cl'),
    ('Cuarto Propio', 'Chile', '+56228765432', 'info@cuartopropio.cl'),
    ('Fondo Editorial PUCP', 'Perú', '+51151234567', 'fondo@pucp.edu.pe'),
    ('Siglo XXI', 'México', '+52555678901', 'siglo21@sigloxxi.com.mx'),
    ('Companhia das Letras', 'Brasil', '+551134567890', 'info@companhiadasletras.com.br');

-- ============================================
-- 11. SAGAS (12)
-- ============================================
INSERT INTO sagas (nombre, cantidad_libros) VALUES
    ('Harry Potter', 7),
    ('El Señor de los Anillos', 3),
    ('Canción de Hielo y Fuego', 5),
    ('Crónicas de Narnia', 7),
    ('Los Juegos del Hambre', 3),
    ('Millennium', 3),
    ('Percy Jackson', 5),
    ('Divergente', 3),
    ('Cincuenta Sombras', 3),
    ('La Torre Oscura', 7),
    ('Fundación', 7),
    ('Dune', 6);

-- ============================================
-- 12. LIBROS (200)
-- ============================================
DO $$
DECLARE
    titulos TEXT[] := ARRAY[
        'Cien años de soledad', 'El amor en los tiempos del cólera', 'Rayuela', 'La casa de los espíritus',
        'Veinte poemas de amor', '2666', 'El túnel', 'Pedro Páramo', 'La tregua', 'El Aleph',
        'Ficciones', 'La ciudad y los perros', 'Pantaleón y las visitadoras', 'El beso de la mujer araña',
        'El reino de este mundo', 'La muerte de Artemio Cruz', 'Como agua para chocolate', 'El laberinto de la soledad',
        'Hijo de ladrón', 'La amortajada', 'Altazor', 'Residencia en la tierra', 'Canto general',
        'Confieso que he vivido', 'El otoño del patriarca', 'Crónica de una muerte anunciada',
        'Los detectives salvajes', 'El obsceno pájaro de la noche', 'Coronación', 'El lugar sin límites',
        'Bestiario', 'Final del juego', 'Las armas secretas', 'Historias de cronopios y de famas',
        'La invención de Morel', 'El túnel de los pájaros muertos', 'Sobre héroes y tumbas',
        'La resistencia', 'El libro de arena', 'El informe de Brodie', 'El hacedor',
        'La naranja mecánica', '1984', 'Un mundo feliz', 'Fahrenheit 451',
        'El gran Gatsby', 'Matar a un ruiseñor', 'En el camino', 'Ulises'
    ];
    v_titulo VARCHAR;
    v_anio INT;
    v_precio DECIMAL;
    v_id_autor INT;
    v_id_categoria INT;
    v_id_editorial INT;
    v_id_saga INT;
    v_estante VARCHAR;
    v_libros_en_saga INT;
    v_saga_actual RECORD;
    i INT;
    j INT;
BEGIN
    -- Primero insertar los libros que pertenecen a sagas para asegurar cantidad correcta
    FOR v_saga_actual IN SELECT id_saga, nombre, cantidad_libros FROM sagas LOOP
        FOR j IN 1..v_saga_actual.cantidad_libros LOOP
            v_titulo := v_saga_actual.nombre || ' - Libro ' || j;
            v_anio := 1980 + (floor(random() * 47))::INT;
            v_precio := (9900 + (random() * 50000))::DECIMAL(10,2);
            
            SELECT id_autor INTO v_id_autor FROM autor ORDER BY random() LIMIT 1;
            SELECT id_categoria INTO v_id_categoria FROM categoria ORDER BY random() LIMIT 1;
            SELECT id_editorial INTO v_id_editorial FROM editorial ORDER BY random() LIMIT 1;
            
            v_estante := UPPER(CHR(65 + floor(random() * 11)::INT)) || '-' || (1 + (floor(random() * 20))::INT)::TEXT;
            
            INSERT INTO libro (id_autor, id_categoria, id_editorial, id_saga, titulo, anio_publicacion, precio, estante)
            VALUES (v_id_autor, v_id_categoria, v_id_editorial, v_saga_actual.id_saga, v_titulo, v_anio, v_precio, v_estante);
        END LOOP;
    END LOOP;
    
    -- Calcular cuántos libros de sagas se insertaron
    SELECT COUNT(*) INTO v_libros_en_saga FROM libro WHERE id_saga IS NOT NULL;
    
    -- Insertar el resto de libros sin saga hasta completar 200
    FOR i IN 1..(200 - v_libros_en_saga) LOOP
        IF i <= array_length(titulos, 1) THEN
            v_titulo := titulos[i];
        ELSE
            v_titulo := 'Libro ' || i;
        END IF;
        
        v_anio := 1980 + (floor(random() * 47))::INT;
        v_precio := (9900 + (random() * 50000))::DECIMAL(10,2);
        
        SELECT id_autor INTO v_id_autor FROM autor ORDER BY random() LIMIT 1;
        SELECT id_categoria INTO v_id_categoria FROM categoria ORDER BY random() LIMIT 1;
        SELECT id_editorial INTO v_id_editorial FROM editorial ORDER BY random() LIMIT 1;
        
        v_estante := UPPER(CHR(65 + floor(random() * 11)::INT)) || '-' || (1 + (floor(random() * 20))::INT)::TEXT;
        
        INSERT INTO libro (id_autor, id_categoria, id_editorial, id_saga, titulo, anio_publicacion, precio, estante)
        VALUES (v_id_autor, v_id_categoria, v_id_editorial, NULL, v_titulo, v_anio, v_precio, v_estante);
    END LOOP;
END $$;

-- ============================================
-- 13. PRODUCTOS (libros y artículos de librería)
-- ============================================
-- Los libros también son productos que se venden
INSERT INTO producto (nombre, precio)
SELECT titulo, precio FROM libro;

-- Artículos de librería adicionales
INSERT INTO producto (nombre, precio) VALUES
    ('Mochila escolar', 15000.00),
    ('Cuaderno universitario', 3500.00),
    ('Set de lápices', 5000.00),
    ('Borrador', 500.00),
    ('Regla 30cm', 1200.00),
    ('Destacadores (pack 4)', 3200.00),
    ('Corrector líquido', 2400.00),
    ('Pegamento en barra', 1800.00),
    ('Carpeta archivadora', 4500.00),
    ('Calculadora básica', 8900.00),
    ('Agenda 2025', 7500.00),
    ('Stickers decorativos', 2200.00),
    ('Post-it (pack 5)', 3900.00),
    ('Tijeras escolares', 2500.00),
    ('Plumones (set 12)', 6500.00),
    ('Estuche porta lápices', 4200.00),
    ('Block de dibujo', 3800.00),
    ('Saca puntas eléctrico', 5500.00),
    ('Bolígrafos (pack 3)', 2900.00),
    ('Goma de borrar premium', 1500.00);

-- ============================================
-- 14. STOCK DE PRODUCTOS
-- ============================================
DO $$
DECLARE
    prod RECORD;
    suc RECORD;
    v_stock INT;
BEGIN
    FOR prod IN SELECT id_producto FROM producto LOOP
        FOR suc IN SELECT id_sucursal FROM sucursal LOOP
            v_stock := (10 + (random() * 200))::INT;
            
            INSERT INTO stockProducto (id_sucursal, id_producto, cantidad_stock, fecha_actualizacion)
            VALUES (suc.id_sucursal, prod.id_producto, v_stock, NOW() - (random() * INTERVAL '30 days'));
        END LOOP;
    END LOOP;
END $$;

-- ============================================
-- 15. VENTAS Y DETALLE DE VENTA (4 años)
-- ============================================
DO $$
DECLARE
    v_fecha_actual DATE;
    v_fecha_fin DATE;
    v_ventas_diarias INT;
    v_num_venta INT;
    v_hora_base TIMESTAMP;
    v_id_cliente INT;
    v_id_caja INT;
    v_id_cajero INT;
    v_id_venta INT;
    v_id_producto INT;
    v_cantidad INT;
    v_precio DECIMAL(10,2);
    v_subtotal DECIMAL(10,2);
    v_total DECIMAL(10,2);
    v_productos_venta INT;
    v_producto_count INT;
    v_anio_publicacion INT;
    v_es_libro BOOLEAN;
BEGIN
    v_fecha_actual := '2022-01-01';
    v_fecha_fin := '2025-12-31';
    
    -- Tabla temporal para asignar cajero-caja por sucursal
    CREATE TEMP TABLE cajero_caja_temp AS
    SELECT c.id_cajero, cj.id_caja, cj.id_sucursal
    FROM cajero c
    JOIN empleado e ON c.id_empleado = e.id_empleado
    JOIN caja cj ON e.id_sucursal = cj.id_sucursal
    ORDER BY random();
    
    WHILE v_fecha_actual <= v_fecha_fin LOOP
        -- Entre 50 y 150 ventas por día
        v_ventas_diarias := 50 + (random() * 100)::INT;
        
        FOR v_num_venta IN 1..v_ventas_diarias LOOP
            -- Hora aleatoria entre 8:00 y 22:00
            v_hora_base := v_fecha_actual + TIME '08:00:00' + (random() * 50400)::INT * INTERVAL '1 second';
            
            -- 95% de las ventas tienen cliente, 5% usan cliente por defecto
            IF random() < 0.95 THEN
                SELECT id_cliente INTO v_id_cliente FROM cliente ORDER BY random() LIMIT 1;
            ELSE
                v_id_cliente := 1;
            END IF;
            
            -- Caja y cajero aleatorios de la misma sucursal
            SELECT cct.id_caja, cct.id_cajero INTO v_id_caja, v_id_cajero
            FROM cajero_caja_temp cct
            ORDER BY random() LIMIT 1;
            
            -- Insertar venta con total temporal 0
            v_total := 0;
            
            INSERT INTO venta (id_cliente, id_caja, id_cajero, fecha_hora, total)
            VALUES (v_id_cliente, v_id_caja, v_id_cajero, v_hora_base, 0)
            RETURNING id_venta INTO v_id_venta;
            
            -- Agregar entre 1 y 8 productos por venta
            v_productos_venta := 1 + (random() * 7)::INT;
            v_total := 0;
            
            FOR v_producto_count IN 1..v_productos_venta LOOP
                -- Seleccionar producto aleatorio
                SELECT p.id_producto, p.precio INTO v_id_producto, v_precio
                FROM producto p
                ORDER BY random() LIMIT 1;
                
                -- Verificar que el producto es válido para la fecha de venta
                v_es_libro := FALSE;
                v_anio_publicacion := NULL;
                
                -- Revisar si el producto es un libro y obtener su año de publicación
                SELECT l.anio_publicacion INTO v_anio_publicacion
                FROM libro l
                JOIN producto p ON l.titulo = p.nombre AND l.precio = p.precio
                WHERE p.id_producto = v_id_producto;
                
                v_es_libro := v_anio_publicacion IS NOT NULL;
                
                -- Si es un libro, solo se puede vender si el año de publicación es menor o igual al año de la venta
                IF v_es_libro AND v_anio_publicacion > EXTRACT(YEAR FROM v_hora_base) THEN
                    -- Buscar otro producto que no sea libro o que tenga año de publicación válido
                    SELECT p.id_producto, p.precio INTO v_id_producto, v_precio
                    FROM producto p
                    LEFT JOIN libro l ON l.titulo = p.nombre AND l.precio = p.precio
                    WHERE (l.id_libro IS NULL) OR (l.anio_publicacion <= EXTRACT(YEAR FROM v_hora_base))
                    ORDER BY random() LIMIT 1;
                    
                    -- Si no hay producto alternativo, usar artículo de librería
                    IF NOT FOUND THEN
                        SELECT p.id_producto, p.precio INTO v_id_producto, v_precio
                        FROM producto p
                        LEFT JOIN libro l ON l.titulo = p.nombre AND l.precio = p.precio
                        WHERE l.id_libro IS NULL
                        ORDER BY random() LIMIT 1;
                    END IF;
                END IF;
                
                v_cantidad := 1 + (random() * 3)::INT;
                
                -- Verificar si el producto ya está en esta venta
                IF EXISTS (SELECT 1 FROM detalleventa WHERE id_venta = v_id_venta AND id_producto = v_id_producto) THEN
                    -- Actualizar cantidad y subtotal si el producto ya existe
                    UPDATE detalleventa
                    SET cantidad = cantidad + v_cantidad,
                        subtotal = (cantidad + v_cantidad) * precio_unitario
                    WHERE id_venta = v_id_venta AND id_producto = v_id_producto;
                    
                    SELECT subtotal INTO v_subtotal FROM detalleventa WHERE id_venta = v_id_venta AND id_producto = v_id_producto;
                ELSE
                    -- Insertar nuevo detalle
                    v_subtotal := v_cantidad * v_precio;
                    
                    INSERT INTO detalleventa (id_venta, id_producto, cantidad, precio_unitario, subtotal)
                    VALUES (v_id_venta, v_id_producto, v_cantidad, v_precio, v_subtotal);
                END IF;
                
                v_total := v_total + v_subtotal;
            END LOOP;
            
            -- Actualizar el total de la venta
            UPDATE venta SET total = v_total WHERE id_venta = v_id_venta;
        END LOOP;
        
        -- Indicador de progreso cada 30 días
        IF EXTRACT(DAY FROM v_fecha_actual) = 1 AND EXTRACT(MONTH FROM v_fecha_actual) IN (1, 4, 7, 10) THEN
            RAISE NOTICE 'Procesando fecha: %', v_fecha_actual;
        END IF;
        
        v_fecha_actual := v_fecha_actual + INTERVAL '1 day';
    END LOOP;
    
    DROP TABLE IF EXISTS cajero_caja_temp;
END $$;

-- ============================================
-- CONSULTAS DE VERIFICACIÓN
-- ============================================
DO $$
DECLARE
    v_count INT;
    v_min_date DATE;
    v_max_date DATE;
BEGIN            
    RAISE NOTICE '==================== VERIFICACIÓN DE DATOS ====================';
    
    SELECT COUNT(*) INTO v_count FROM cliente;
    RAISE NOTICE 'Clientes: %', v_count;
    
    SELECT COUNT(*) INTO v_count FROM sucursal;
    RAISE NOTICE 'Sucursales: %', v_count;
    
    SELECT COUNT(*) INTO v_count FROM caja;
    RAISE NOTICE 'Cajas: %', v_count;
    
    SELECT COUNT(*) INTO v_count FROM empleado;
    RAISE NOTICE 'Empleados: %', v_count;
    
    SELECT COUNT(*) INTO v_count FROM cajero;
    RAISE NOTICE 'Cajeros: %', v_count;
    
    SELECT COUNT(*) INTO v_count FROM producto;
    RAISE NOTICE 'Productos: %', v_count;
    
    SELECT COUNT(*) INTO v_count FROM libro;
    RAISE NOTICE 'Libros: %', v_count;
    
    -- Verificar cantidad de libros por saga
    RAISE NOTICE '--- Libros por saga ---';
    FOR v_count IN 
        SELECT COUNT(*) FROM libro WHERE id_saga IS NOT NULL
    LOOP
        RAISE NOTICE 'Total libros en sagas: %', v_count;
    END LOOP;
    
    SELECT COUNT(*) INTO v_count FROM venta;
    RAISE NOTICE 'Ventas totales: %', v_count;
    
    SELECT COUNT(*) INTO v_count FROM detalleventa;
    RAISE NOTICE 'Detalles de venta: %', v_count;
    
    SELECT MIN(fecha_hora)::DATE, MAX(fecha_hora)::DATE INTO v_min_date, v_max_date FROM venta;
    RAISE NOTICE 'Rango de fechas de ventas: % a %', v_min_date, v_max_date;
    
    -- Verificar que no hay ventas de libros antes de su publicación
    SELECT COUNT(*) INTO v_count
    FROM detalleventa dv
    JOIN producto p ON dv.id_producto = p.id_producto
    JOIN libro l ON l.titulo = p.nombre AND l.precio = p.precio
    JOIN venta v ON dv.id_venta = v.id_venta
    WHERE l.anio_publicacion > EXTRACT(YEAR FROM v.fecha_hora);
    RAISE NOTICE 'Ventas inválidas de libros (venta antes de publicación): %', v_count;
    
    SELECT COUNT(*) INTO v_count FROM stockProducto;
    RAISE NOTICE 'Registros de stock: %', v_count;
    
    RAISE NOTICE '==============================================================';
END $$;