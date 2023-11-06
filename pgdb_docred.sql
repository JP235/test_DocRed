CREATE TABLE Clientes (
    ID_Cliente SERIAL PRIMARY KEY,
    Nombre VARCHAR(100),
    Direccion VARCHAR(100),
    Telefono VARCHAR(15),
    Fecha_Creacion DATE
)
CREATE TABLE Vendedores (
    ID_Vendedor SERIAL PRIMARY KEY,
    Nombre VARCHAR(100),
    ...
)
CREATE TABLE Productos (
    ID_Producto SERIAL PRIMARY KEY,
    Nombre VARCHAR(100),
    Descripcion VARCHAR(255),
    Precio DECIMAL(10, 2),
    Stock INT
)

CREATE TABLE Pedidos (
    ID_Pedido SERIAL PRIMARY KEY,
    Direccion_Entrega VARCHAR(100),
    Fecha DATE,
    Estado INT,
    ID_Cliente INT,
    FOREIGN KEY (ID_Cliente) REFERENCES Clientes(ID_Cliente)
    FOREIGN KEY (ID_Vendedor) REFERENCES Vendedores(ID_Vendedor)
)

CREATE TABLE Detalle_Pedido (
    ID_Pedido INT,
    ID_Producto INT,
    Cantidad INT,
    PRIMARY KEY (ID_Pedido, ID_Producto),
    FOREIGN KEY (ID_Pedido) REFERENCES Pedidos(ID_Pedido),
    FOREIGN KEY (ID_Producto) REFERENCES Productos(ID_Producto)
)