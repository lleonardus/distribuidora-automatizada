import sqlite3 as connector

connection = None
cursor = None

try:
    connection = connector.connect("distribuidora.db")
    cursor = connection.cursor()

    top5_month_products_sql = """
    SELECT pr.nome_produto, pe.data_pedido, SUM(i.quantidade) as total_vendido
      FROM produtos pr
      JOIN itens_pedido i ON pr.id=i.produto_id
      JOIN pedidos pe on i.pedido_id=pe.id
      WHERE strftime('%m', pe.data_pedido) = strftime('%m', date())
      GROUP BY pr.nome_produto
    ORDER BY total_vendido DESC, pr.nome_produto ASC LIMIT(5);
    """

    cursor.execute(top5_month_products_sql)

    top5_month_products = cursor.fetchall()

    print(f"Top 5 month products:\n{top5_month_products}\n")

    top_clients_sql = """
    SELECT c.nome_cliente, SUM(pe.valor_total) total_gasto
      FROM clientes c
      JOIN pedidos pe ON pe.cliente_id = c.id
      GROUP BY c.nome_cliente
    ORDER BY total_gasto DESC, c.nome_cliente ASC;
    """

    cursor.execute(top_clients_sql)

    top_clients = cursor.fetchall()

    print(f"Top Clients:\n{top_clients}\n")

    late_deliveries_sql = """
    SELECT e.id, c.nome_cliente, e.data_prevista, e.data_entrega
      FROM entregas e
      JOIN pedidos pe ON  pe.id = e.pedido_id
      JOIN clientes c ON  c.id = pe.cliente_id
      WHERE data_entrega > data_prevista
    ORDER BY data_entrega DESC;
    """

    cursor.execute(late_deliveries_sql)

    late_deliveries = cursor.fetchall()

    print(f"Late Deliveries:\n{late_deliveries}\n")

    billing_by_state_sql = """
    SELECT c.estado, SUM(pe.valor_total) AS faturamento
      FROM clientes c 
      JOIN pedidos pe ON c.id=pe.cliente_id
      GROUP BY c.estado
    ORDER BY faturamento DESC;
    """

    cursor.execute(billing_by_state_sql)

    billing_by_state = cursor.fetchall()

    print(f"Billing By State: \n{billing_by_state}\n")

    connection.commit()
except connector.DatabaseError as e:
    print(f"Something went wrong while creating the report :/\n {e}")
finally:
    if cursor is not None:
        cursor.close()
    if connection is not None:
        connection.close()
