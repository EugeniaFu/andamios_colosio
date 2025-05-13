CREATE DATABASE IF NOT EXISTS SistemaRentas;
USE SistemaRentas;

-- Tabla Cliente
CREATE TABLE Cliente (
    IDCliente INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(50),
    Apellido VARCHAR(50),
    Telefono VARCHAR(20),
    FechaAlta DATE,
    IneArchivo VARCHAR(100),
    Estatus VARCHAR(20)
);

-- Tabla Prefactura
CREATE TABLE Prefactura (
    idPrefactura INT PRIMARY KEY AUTO_INCREMENT,
    IDCliente INT,
    Nombre VARCHAR(50),
    MetodoDePago VARCHAR(50),
    Descripcion TEXT,
    Dias INT,
    Periodo VARCHAR(20),
    Costo DECIMAL(10,2),
    Piezas INT,
    Subtotal DECIMAL(10,2),
    IVA DECIMAL(10,2),
    FOREIGN KEY (IDCliente) REFERENCES Cliente(IDCliente)
);

-- Tabla Pago
CREATE TABLE Pago (
    IDPago INT PRIMARY KEY AUTO_INCREMENT,
    FechaPago DATE,
    MetodoDePago VARCHAR(50),
    ConceptoDePago TEXT,
    MontoFinalIVA DECIMAL(10,2)
);

-- Relación Prefactura - Pago (1 a 1)
ALTER TABLE Prefactura
ADD COLUMN IDPago INT UNIQUE,
ADD CONSTRAINT fk_pago FOREIGN KEY (IDPago) REFERENCES Pago(IDPago);

-- Tabla Productos (Inventario)
CREATE TABLE Productos (
    IDProducto INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(100),
    Descripcion TEXT,
    Precio DECIMAL(10,2),
    Entrada INT,
    Salida INT
);

-- Tabla Envio
CREATE TABLE Envio (
    ID_TEnvio INT PRIMARY KEY AUTO_INCREMENT,
    ViajeRedondo BOOLEAN,
    AreaEnvio VARCHAR(100)
);

-- Tabla Renta
CREATE TABLE Renta (
    FOLIO INT PRIMARY KEY AUTO_INCREMENT,
    FechaHora DATETIME,
    FechaHoraVencimiento DATETIME,
    Estatus VARCHAR(50),
    Material TEXT,
    Referencias TEXT,
    Observaciones TEXT
);

-- Relación Cliente - Renta
CREATE TABLE Cliente_Renta (
    IDCliente INT,
    FOLIO INT,
    PRIMARY KEY (IDCliente, FOLIO),
    FOREIGN KEY (IDCliente) REFERENCES Cliente(IDCliente),
    FOREIGN KEY (FOLIO) REFERENCES Renta(FOLIO)
);

-- Relación Renta - Prefactura
ALTER TABLE Renta
ADD COLUMN idPrefactura INT,
ADD CONSTRAINT fk_prefactura FOREIGN KEY (idPrefactura) REFERENCES Prefactura(idPrefactura);

-- Relación Renta - Envio (N a N)
CREATE TABLE Renta_Envio (
    FOLIO INT,
    ID_TEnvio INT,
    PRIMARY KEY (FOLIO, ID_TEnvio),
    FOREIGN KEY (FOLIO) REFERENCES Renta(FOLIO),
    FOREIGN KEY (ID_TEnvio) REFERENCES Envio(ID_TEnvio)
);

-- Relación Renta - Productos (N a N)
CREATE TABLE Renta_Producto (
    FOLIO INT,
    IDProducto INT,
    PRIMARY KEY (FOLIO, IDProducto),
    FOREIGN KEY (FOLIO) REFERENCES Renta(FOLIO),
    FOREIGN KEY (IDProducto) REFERENCES Productos(IDProducto)
);

-- Tabla PersonaRef
CREATE TABLE PersonaRef (
    IDPersona INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(50),
    Apellido VARCHAR(50),
    Telefono VARCHAR(20)
);

-- Tabla UbicacionObra
CREATE TABLE UbicacionObra (
    IDUbicacion INT PRIMARY KEY AUTO_INCREMENT,
    Calle VARCHAR(100),
    Num_Ext VARCHAR(10),
    Num_Int VARCHAR(10),
    Colonia VARCHAR(100),
    CP VARCHAR(10),
    IDPersona INT,
    FOREIGN KEY (IDPersona) REFERENCES PersonaRef(IDPersona)
);

CREATE TABLE Usuarios (
    IDUsuario INT PRIMARY KEY AUTO_INCREMENT,
    NombreUsuario VARCHAR(50) UNIQUE NOT NULL,
    Nombre VARCHAR(50),
    ApellidoPaterno VARCHAR(50),
    ApellidoMaterno VARCHAR(50),
    Correo VARCHAR(100),
    Contrasena VARCHAR(255) NOT NULL,
    Rol ENUM('Administrador', 'Empleado') DEFAULT 'Empleado',
    Accesos TEXT,
    FotoPerfil VARCHAR(255),
    Telefono VARCHAR(20),
    FechaRegistro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Relación Renta - UbicaciónObra
ALTER TABLE Renta
ADD COLUMN IDUbicacion INT,
ADD CONSTRAINT fk_ubicacion FOREIGN KEY (IDUbicacion) REFERENCES UbicacionObra(IDUbicacion);

-- Vista
CREATE VIEW VistaUsuarios AS
SELECT 
    IDUsuario,
    NombreUsuario,
    Nombre,
    ApellidoPaterno,
    ApellidoMaterno,
    Correo,
    Rol,
    Accesos,
    FotoPerfil,
    Telefono,
    FechaRegistro
FROM Usuarios;

INSERT INTO Usuarios (
    NombreUsuario, ApellidoPaterno, ApellidoMaterno, Correo, Contrasena, Rol, Accesos
) VALUES (
    'Administrador', 'Colosio', 'Principal', 'admin@colosio.com',
    'scrypt:32768:8:1$ZMxcb8GiZTuP4Z82$e9f8b2e47da3447b75ff5ae448496c6365d809e76c264a0203b9ca6a35477560d23dc9e16ce41f05ea130999e300763f418439eae13f42dbe101a01fd79ee40f',
    'Administrador',
    '["ventas", "inventario", "usuarios", "reportes"]'
);
