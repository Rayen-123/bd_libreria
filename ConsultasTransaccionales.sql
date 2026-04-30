-- =========================
-- Consultas SQL
-- =========================

-- =========================
-- VENTA
-- =========================

-- Cuenta el total de ventas realizadas
SELECT COUNT(*) 
FROM venta;

-- Muestra el monto total acumulado de todas las ventas
SELECT SUM(total) 
FROM venta;

-- Muestra la venta con mayor monto
SELECT MAX(total) 
FROM venta;

-- =========================
-- DETALLEVENTA
-- =========================

-- Cuenta la cantidad total de productos vendidos (registros en detalle)
SELECT COUNT(*) 
FROM detalleventa;

-- Calcula la cantidad total de unidades vendidas
SELECT SUM(cantidad) 
FROM detalleventa;

-- =========================
-- STOCK
-- =========================

-- Cuenta cuántos registros de stock existen en el sistema
SELECT COUNT(*) 
FROM stockproducto;

-- Muestra el total de productos disponibles en stock
SELECT SUM(cantidad_stock) 
FROM stockproducto;

