from datetime import date

from sqlalchemy import Integer, cast, func, case

from utils.utils import get_month

from db.database import engine, Session
from db.models import Client, Items_Order, Order, Product, Delivery


def top5_month_products():
    current_month = date.today().month

    with Session() as session:
        return (
            session.query(
                Product.name.label("Produtos"),
                func.sum(Items_Order.quantity).label("Total Vendido"),
            )
            .join(Items_Order, Items_Order.product_id == Product.id)
            .join(Order, Order.id == Items_Order.order_id)
            .filter(func.extract("month", Order.order_date) == current_month)
            .group_by(Product.name)
            .order_by(func.sum(Items_Order.quantity).desc(), Product.name.asc())
            .limit(5)
        ).all()


def top_clients():
    with Session() as session:
        return (
            session.query(
                Client.name.label("Cliente"),
                func.round(func.sum(Order.total_value), 2).label("Total Gasto"),
            )
            .join(Order, Order.client_id == Client.id)
            .group_by(Client.name)
            .order_by(func.sum(Order.total_value).desc(), Client.name.asc())
        ).all()


def late_deliveries():
    # SQLite não entende bem o tipo Date

    is_sqlite = engine.dialect.name == "sqlite"
    days_late = None

    if is_sqlite:
        days_late = func.julianday(Delivery.delivery_date) - func.julianday(
            Delivery.expected_date
        )
    else:
        days_late = cast(Delivery.delivery_date - Delivery.expected_date, Integer)

    with Session() as session:
        return (
            session.query(
                Delivery.id.label("Entrega Id"),
                Client.name.label("Cliente"),
                Delivery.expected_date.label("Data Prevista"),
                Delivery.delivery_date.label("Data de Entrega"),
                days_late.label("Atraso em Dias"),
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


def billing_by_state():
    with Session() as session:
        return (
            session.query(
                Client.state.label("Estado"),
                func.round(func.sum(Order.total_value), 2).label("Faturamento"),
            )
            .join(Order, Order.client_id == Client.id)
            .group_by(Client.state)
            .order_by(func.sum(Order.total_value).desc(), Client.state.asc())
        ).all()


def sales_history():
    with Session() as session:
        return (
            session.query(
                func.extract("year", Delivery.delivery_date).label("Ano"),
                case(
                    *[
                        (
                            func.extract("month", Delivery.delivery_date) == month_key,
                            month_value,
                        )
                        for month_key, month_value in get_month()
                    ],
                    else_="Desconhecido"
                ).label("Mês"),
                Product.name.label("Produto"),
                (Items_Order.quantity * Product.price).label("Faturamento"),
            )
            .join(Order, Order.id == Delivery.order_id)
            .join(Items_Order, Items_Order.order_id == Order.id)
            .join(Product, Product.id == Items_Order.product_id)
            .group_by(
                func.extract("year", Delivery.delivery_date),
                func.extract("month", Delivery.delivery_date),
                Product.name,
            )
            .all()
        )
