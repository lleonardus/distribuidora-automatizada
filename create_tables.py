import os
from dotenv import load_dotenv
import sqlite3 as connector

load_dotenv()

DATABASE = os.getenv("DATABASE") or "distribuidora.db"

connection = None
cursor = None

try:
    connection = connector.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
    CREATE TABLE clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_cliente TEXT NOT NULL,
        cidade TEXT NOT NULL,
        estado TEXT NOT NULL,
        telefone TEXT
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_produto TEXT NOT NULL,
        categoria TEXT NOT NULL,
        preco_unitario REAL NOT NULL
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        data_pedido DATE NOT NULL,
        valor_total REAL NOT NULL,
        FOREIGN KEY (cliente_id) REFERENCES clientes (id)
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE itens_pedido (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER NOT NULL,
        produto_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        FOREIGN KEY (pedido_id) REFERENCES pedidos (id),
        FOREIGN KEY (produto_id) REFERENCES produtos (id)
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE entregas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER NOT NULL,
        data_prevista DATE NOT NULL,
        data_entrega DATE,
        FOREIGN KEY (pedido_id) REFERENCES pedidos (id)
    );
    """
    )

    connection.commit()
except connector.DatabaseError as e:
    print(f"Something went wrong while creating the database :/\n {e}")
finally:
    if cursor is not None:
        cursor.close()
    if connection is not None:
        connection.close()
