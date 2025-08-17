from datetime import date

from sqlalchemy import Integer, cast, func

from db.database import engine, Session
from db.models import Client, Items_Order, Order, Product, Delivery


def top5_month_products():
    current_month = date.today().month

    with Session() as session:
        products = (
            session.query(Product.name, func.sum(Items_Order.quantity))
            .join(Items_Order, Items_Order.product_id == Product.id)
            .join(Order, Order.id == Items_Order.order_id)
            .filter(func.extract("month", Order.order_date) == current_month)
            .group_by(Product.name)
            .order_by(func.sum(Items_Order.quantity).desc(), Product.name.asc())
            .limit(5)
        ).all()

        return [
            {"product_name": product[0], "total_sold": product[1]}
            for product in products
        ]


def top_clients():
    with Session() as session:
        clients = (
            session.query(Client.name, func.round(func.sum(Order.total_value), 2))
            .join(Order, Order.client_id == Client.id)
            .group_by(Client.name)
            .order_by(func.sum(Order.total_value).desc(), Client.name.asc())
        ).all()

        return [
            {"client_name": client[0], "total_expense": client[1]} for client in clients
        ]


def late_deliveries():
    # SQLite não entende bem o tipo Date

    is_sqlite = engine.dialect.name == "sqlite"
    days_late = None

    if is_sqlite:
        days_late = (
            func.julianday(Delivery.delivery_date)
            - func.julianday(Delivery.expected_date)
        ).label("days_late")
    else:
        days_late = cast(
            Delivery.delivery_date - Delivery.expected_date, Integer
        ).label("days_late")

    with Session() as session:
        deliveries = (
            session.query(
                Delivery.id,
                Client.name,
                Delivery.expected_date,
                Delivery.delivery_date,
                days_late,
            )
            .join(Order, Order.id == Delivery.order_id)
            .join(Client, Client.id == Order.client_id)
            .filter(Delivery.delivery_date > Delivery.expected_date)
            .order_by(
                days_late.desc(),
                Client.name.asc(),
            )
            .all()
        )

        return [
            {
                "delivery_id": delivery[0],
                "client_name": delivery[1],
                "expected_date": delivery[2],
                "delivery_date": delivery[3],
                "days_late": delivery[4],
            }
            for delivery in deliveries
        ]


def billing_by_state():
    with Session() as session:
        billings = (
            session.query(Client.state, func.round(func.sum(Order.total_value), 2))
            .join(Order, Order.client_id == Client.id)
            .group_by(Client.state)
            .order_by(func.sum(Order.total_value).desc(), Client.state.asc())
        ).all()

        return [
            {"state": billing[0], "total_value": billing[1]} for billing in billings
        ]
