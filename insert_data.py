import os
from dotenv import load_dotenv
import sqlite3 as connector
from faker import Faker
import random
from datetime import datetime, timedelta

load_dotenv()

DATABASE = os.getenv("DATABASE") or "distribuidora.db"

fake = Faker(locale="pt_BR")

connection = None
cursor = None

try:
    connection = connector.connect(DATABASE)
    connection.execute("PRAGMA foreign_keys = on")
    cursor = connection.cursor()

    # ---------- CLIENTS ----------

    clients = []

    for _ in range(50):
        name = fake.name()
        city = fake.city()
        state = fake.state()
        phone = fake.phone_number()
        clients.append((name, city, state, phone))

    cursor.executemany(
        """
    INSERT INTO clientes(nome_cliente, cidade, estado, telefone) 
    VALUES(?, ?, ?, ?);
    """,
        clients,
    )

    # ---------- PRODUCTS ----------

    products = []
    product_names = ["Caixa", "Pacote", "Garrafa", "Kit"]
    categories = [
        "Alimentos",
        "Bebidas",
        "Beleza",
        "Calçados",
        "Higiene",
        "Limpeza",
        "Saúde",
        "Bazar",
    ]

    for _ in range(20):
        product_name = f"{random.choice(product_names)} {fake.word().capitalize()}"
        category = random.choice(categories)
        unit_price = round(random.uniform(5, 200), 2)
        products.append((product_name, category, unit_price))

    cursor.executemany(
        """
    INSERT INTO produtos(nome_produto, categoria, preco_unitario)
    VALUES (?, ?, ?);
    """,
        products,
    )

    # ---------- ORDERS + ORDERED ITEMS ----------

    orders = []
    ordered_items_temp = []

    for _ in range(200):
        client_id = random.randint(1, len(clients))
        order_date = fake.date_between(start_date="-6M", end_date="today")
        total_price = 0

        num_items = random.randint(1, 5)

        for _ in range(num_items):
            product_id = random.randint(1, len(products))
            unit_price = products[product_id - 1][2]
            quantity = random.randint(1, 10)

            total_price += unit_price * quantity
            ordered_items_temp.append((None, product_id, quantity))

        orders.append((client_id, order_date, round(total_price, 2)))

    cursor.executemany(
        """
        INSERT INTO pedidos(cliente_id, data_pedido, valor_total)
        VALUES (?, ?, ?);
    """,
        orders,
    )

    cursor.execute("SELECT id FROM pedidos;")
    order_ids = [row[0] for row in cursor.fetchall()]

    ordered_items = []
    index = 0

    for order_id in order_ids:
        for _ in range(random.randint(1, 5)):
            if index < len(ordered_items_temp):
                _, product_id, quantity = ordered_items_temp[index]
                ordered_items.append((order_id, product_id, quantity))
                index += 1

    cursor.executemany(
        """
        INSERT INTO itens_pedido (pedido_id, produto_id, quantidade)
        VALUES (?, ?, ?);
    """,
        ordered_items,
    )

    # ---------- DELIVERIES ----------

    deliveries = []

    for order_id, client_id, order_date, _ in [
        (order_ids[i], orders[i][0], orders[i][1], orders[i][2])
        for i in range(len(orders))
    ]:
        expected_date = datetime.strptime(str(order_date), "%Y-%m-%d") + timedelta(
            days=random.randint(2, 10)
        )

        if random.random() < 0.2:
            delivery_date = expected_date + timedelta(days=random.randint(1, 5))
        else:
            delivery_date = expected_date

        deliveries.append((order_id, expected_date.date(), delivery_date.date()))

    cursor.executemany(
        """
        INSERT INTO entregas (pedido_id, data_prevista, data_entrega)
        VALUES (?, ?, ?);
    """,
        deliveries,
    )

    connection.commit()
except connector.DatabaseError as e:
    print(f"Something went wrong while inserting data into the database :/\n {e}")
finally:
    if cursor is not None:
        cursor.close()
    if connection is not None:
        connection.close()
