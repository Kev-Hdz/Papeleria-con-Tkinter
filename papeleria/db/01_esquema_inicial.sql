-- ===================================================== 

-- BASE DE DATOS PARA EL CASO PRÁCTICO: PAPELERÍA 

-- ===================================================== 

 

CREATE DATABASE IF NOT EXISTS bd_papeleria 

CHARACTER SET utf8mb4 

COLLATE utf8mb4_spanish_ci; 

 

USE bd_papeleria; 

 

-- ===================================================== 

-- TABLA: categorias 

-- Guarda las categorías de los productos de papelería 

-- ===================================================== 

 

CREATE TABLE categorias ( 

    id_categoria INT AUTO_INCREMENT PRIMARY KEY, 

    nombre_categoria VARCHAR(60) NOT NULL UNIQUE 

); 

 

-- ===================================================== 

-- TABLA: marcas 

-- Guarda las marcas de los productos 

-- ===================================================== 

 

CREATE TABLE marcas ( 

    id_marca INT AUTO_INCREMENT PRIMARY KEY, 

    nombre_marca VARCHAR(60) NOT NULL UNIQUE 

); 

 

-- ===================================================== 

-- TABLA: proveedores 

-- Guarda los datos de los proveedores 

-- ===================================================== 

 

CREATE TABLE proveedores ( 

    id_proveedor INT AUTO_INCREMENT PRIMARY KEY, 

    nombre VARCHAR(80) NOT NULL, 

    telefono VARCHAR(15), 

    correo VARCHAR(80), 

    direccion VARCHAR(150) 

); 

 

-- ===================================================== 

-- TABLA: clientes 

-- Guarda los datos de los clientes 

-- ===================================================== 

 

CREATE TABLE clientes ( 

    id_cliente INT AUTO_INCREMENT PRIMARY KEY, 

    nombre VARCHAR(80) NOT NULL, 

    telefono VARCHAR(15), 

    correo VARCHAR(80) 

); 

 

-- ===================================================== 

-- TABLA: productos 

-- Guarda los productos que se venden en la papelería 

-- ===================================================== 

 

CREATE TABLE productos ( 

    id_producto INT AUTO_INCREMENT PRIMARY KEY, 

    nombre VARCHAR(80) NOT NULL, 

    id_categoria INT NOT NULL, 

    id_marca INT, 

    descripcion VARCHAR(200), 

    precio_compra DECIMAL(10,2) NOT NULL, 

    precio_venta DECIMAL(10,2) NOT NULL, 

    existencia INT NOT NULL, 

    id_proveedor INT, 

    fecha_registro DATE NOT NULL, 

 

    CONSTRAINT fk_producto_categoria 

        FOREIGN KEY (id_categoria) 

        REFERENCES categorias(id_categoria) 

        ON UPDATE CASCADE 

        ON DELETE RESTRICT, 

 

    CONSTRAINT fk_producto_marca 

        FOREIGN KEY (id_marca) 

        REFERENCES marcas(id_marca) 

        ON UPDATE CASCADE 

        ON DELETE SET NULL, 

 

    CONSTRAINT fk_producto_proveedor 

        FOREIGN KEY (id_proveedor) 

        REFERENCES proveedores(id_proveedor) 

        ON UPDATE CASCADE 

        ON DELETE SET NULL, 

 

    CONSTRAINT chk_precio_compra 

        CHECK (precio_compra > 0), 

 

    CONSTRAINT chk_precio_venta 

        CHECK (precio_venta > 0), 

 

    CONSTRAINT chk_existencia 

        CHECK (existencia >= 0) 

); 

 

-- ===================================================== 

-- TABLA: ventas 

-- Guarda los datos generales de cada venta 

-- ===================================================== 

 

CREATE TABLE ventas ( 

    id_venta INT AUTO_INCREMENT PRIMARY KEY, 

    fecha_venta DATE NOT NULL, 

    id_cliente INT, 

    total DECIMAL(10,2) NOT NULL DEFAULT 0.00, 

 

    CONSTRAINT fk_venta_cliente 

        FOREIGN KEY (id_cliente) 

        REFERENCES clientes(id_cliente) 

        ON UPDATE CASCADE 

        ON DELETE SET NULL, 

 

    CONSTRAINT chk_total_venta 

        CHECK (total >= 0) 

); 

 

-- ===================================================== 

-- TABLA: detalle_venta 

-- Guarda los productos vendidos en cada venta 

-- ===================================================== 

 

CREATE TABLE detalle_venta ( 

    id_detalle INT AUTO_INCREMENT PRIMARY KEY, 

    id_venta INT NOT NULL, 

    id_producto INT NOT NULL, 

    cantidad INT NOT NULL, 

    precio_unitario DECIMAL(10,2) NOT NULL, 

    subtotal DECIMAL(10,2) GENERATED ALWAYS AS (cantidad * precio_unitario) STORED, 

 

    CONSTRAINT fk_detalle_venta 

        FOREIGN KEY (id_venta) 

        REFERENCES ventas(id_venta) 

        ON UPDATE CASCADE 

        ON DELETE CASCADE, 

 

    CONSTRAINT fk_detalle_producto 

        FOREIGN KEY (id_producto) 

        REFERENCES productos(id_producto) 

        ON UPDATE CASCADE 

        ON DELETE RESTRICT, 

 

    CONSTRAINT chk_cantidad_detalle 

        CHECK (cantidad > 0), 

 

    CONSTRAINT chk_precio_unitario_detalle 

        CHECK (precio_unitario > 0) 

); 

 