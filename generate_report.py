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

    print(top5_month_products)

    connection.commit()
except connector.DatabaseError as e:
    print(f"Something went wrong while creating the report :/\n {e}")
finally:
    if cursor is not None:
        cursor.close()
    if connection is not None:
        connection.close()
