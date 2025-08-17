from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class Client(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True)
    name = Column("nome_cliente", String, nullable=False)
    city = Column("cidade", String, nullable=False)
    state = Column("estado", String, nullable=False)
    phone = Column("telefone", String, nullable=True)

    orders = relationship("Order", back_populates="client")


class Order(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True)
    client_id = Column("cliente_id", Integer, ForeignKey("clientes.id"), nullable=False)
    order_date = Column("data_pedido", Date, nullable=False)
    total_value = Column("valor_total", Float, nullable=False)

    client = relationship("Client", back_populates="orders")
    items = relationship("Items_Order", back_populates="order")
    deliveries = relationship("Delivery", back_populates="order")


class Product(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True)
    name = Column("nome_produto", String, nullable=False)
    categoria = Column("categoria", String, nullable=False)
    price = Column("preco_unitario", Float, nullable=False)

    itens = relationship("Items_Order", back_populates="product")


class Delivery(Base):
    __tablename__ = "entregas"

    id = Column(Integer, primary_key=True)
    order_id = Column("pedido_id", Integer, ForeignKey("pedidos.id"), nullable=False)
    expected_date = Column("data_prevista", Date, nullable=False)
    delivery_date = Column("data_entrega", Date, nullable=True)

    order = relationship("Order", back_populates="deliveries")


class Items_Order(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True)
    product_id = Column(
        "produto_id", Integer, ForeignKey("produtos.id"), nullable=False
    )
    order_id = Column("pedido_id", Integer, ForeignKey("pedidos.id"), nullable=False)
    quantity = Column("quantidade", Integer, nullable=False)

    product = relationship("Product", back_populates="itens")
    order = relationship("Order", back_populates="items")
