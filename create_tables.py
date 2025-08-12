import sqlite3 as connector

connection = None
cursor = None

try:
    connection = connector.connect("distribuidora.db")
    cursor = connection.cursor()

    clients_table = """
    CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_cliente TEXT NOT NULL,
    cidade TEXT NOT NULL,
    estado TEXT NOT NULL,
    telefone TEXT
    );
    """

    cursor.execute(clients_table)

    products_table = """
    CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_produto TEXT NOT NULL,
    categoria TEXT NOT NULL,
    preco_unitario REAL NOT NULL
    );
    """

    cursor.execute(products_table)

    orders_table = """
    CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    data_pedido DATE NOT NULL,
    valor_total REAL NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
    );
    """

    cursor.execute(orders_table)

    ordered_items_table = """
    CREATE TABLE itens_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos (id),
    FOREIGN KEY (produto_id) REFERENCES produtos (id)
    );
    """

    cursor.execute(ordered_items_table)

    deliveries_table = """
    CREATE TABLE entregas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL,
    data_prevista DATE NOT NULL,
    data_entrega DATE,
    FOREIGN KEY (pedido_id) REFERENCES pedidos (id)
    );
    """

    cursor.execute(deliveries_table)

    connection.commit()
except connector.DatabaseError as e:
    print(f"Something went wrong while creating the database :/\n {e}")
finally:
    if cursor is not None:
        cursor.close()
    if connection is not None:
        connection.close()
