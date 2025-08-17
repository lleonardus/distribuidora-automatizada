import random
from datetime import timedelta

from faker import Faker
from sqlalchemy.orm import Session

from db.database import engine
from db.models import Client, Product, Order, Items_Order, Delivery

fake = Faker(locale="pt_BR")

with Session(engine) as session:

    # ---------- CLIENTS ----------

    clients = [
        Client(
            name=fake.name(),
            city=fake.city(),
            state=fake.state(),
            phone=fake.phone_number(),
        )
        for _ in range(50)
    ]
    session.add_all(clients)
    session.commit()

    # ---------- PRODUCTS ----------

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

    products = [
        Product(
            name=f"{random.choice(product_names)} {fake.word().capitalize()}",
            categoria=random.choice(categories),
            price=round(random.uniform(5, 200), 2),
        )
        for _ in range(20)
    ]
    session.add_all(products)
    session.commit()

    # ---------- ORDERS + ITEMS ----------

    orders = []
    items = []

    for _ in range(200):
        client = random.choice(clients)
        order_date = fake.date_between(start_date="-6M", end_date="today")

        order = Order(client=client, order_date=order_date, total_value=0.0)
        session.add(order)
        session.flush()

        total_value = 0
        for _ in range(random.randint(1, 5)):
            product = random.choice(products)
            quantity = random.randint(1, 10)
            total_value += product.price * quantity

            items.append(Items_Order(order=order, product=product, quantity=quantity))

        order.total_value = round(total_value, 2)  # type: ignore
        orders.append(order)

    session.add_all(items)
    session.commit()

    # ---------- DELIVERIES ----------

    deliveries = []
    for order in orders:
        expected_date = order.order_date + timedelta(days=random.randint(2, 10))

        # Delays 20% of deliveries
        if random.random() < 0.2:
            delivery_date = expected_date + timedelta(days=random.randint(1, 5))
        else:
            delivery_date = expected_date

        deliveries.append(
            Delivery(
                order=order, expected_date=expected_date, delivery_date=delivery_date
            )
        )

    session.add_all(deliveries)
    session.commit()
