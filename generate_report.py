import sqlite3 as connector
import pandas as pd

connection = None
cursor = None

PLANILHA = "planilha.xlsx"

try:
    connection = connector.connect("distribuidora.db")
    cursor = connection.cursor()

    top5_month_products = cursor.execute(
        """
    SELECT pr.nome_produto, SUM(i.quantidade) AS total_vendido
      FROM produtos pr
      JOIN itens_pedido i ON pr.id=i.produto_id
      JOIN pedidos pe ON i.pedido_id=pe.id
      WHERE strftime('%m', pe.data_pedido) = strftime('%m', date())
      GROUP BY pr.nome_produto
    ORDER BY total_vendido DESC, pr.nome_produto ASC LIMIT(5);
    """
    ).fetchall()

    top_clients = cursor.execute(
        """
    SELECT c.nome_cliente, SUM(pe.valor_total) AS total_gasto
      FROM clientes c
      JOIN pedidos pe ON pe.cliente_id = c.id
      GROUP BY c.nome_cliente
    ORDER BY total_gasto DESC, c.nome_cliente ASC;
    """
    ).fetchall()

    late_deliveries = cursor.execute(
        """
    SELECT e.id, c.nome_cliente, e.data_prevista, e.data_entrega
      FROM entregas e
      JOIN pedidos pe ON  pe.id = e.pedido_id
      JOIN clientes c ON  c.id = pe.cliente_id
      WHERE data_entrega > data_prevista
    ORDER BY data_entrega DESC;
    """
    ).fetchall()

    billing_by_state = cursor.execute(
        """
    SELECT c.estado, SUM(pe.valor_total) AS faturamento
      FROM clientes c 
      JOIN pedidos pe ON c.id=pe.cliente_id
      GROUP BY c.estado
    ORDER BY faturamento DESC;
    """
    ).fetchall()

    data_frames = {
        "Top 5 Produtos do Mês": pd.DataFrame(
            {
                "nome_produto": [row[0] for row in top5_month_products],
                "total_vendido": [row[1] for row in top5_month_products],
            }
        ),
        "Top Clientes": pd.DataFrame(
            {
                "nome_cliente": [row[0] for row in top_clients],
                "total_gasto": [row[1] for row in top_clients],
            }
        ),
        "Entregas Atrasadas": pd.DataFrame(
            {
                "entrega_id": [row[0] for row in late_deliveries],
                "nome_cliente": [row[1] for row in late_deliveries],
                "data_prevista": [row[2] for row in late_deliveries],
                "data_entrega": [row[3] for row in late_deliveries],
            }
        ),
        "Faturamento por Estado": pd.DataFrame(
            {
                "estado": [row[0] for row in billing_by_state],
                "faturamento": [row[1] for row in billing_by_state],
            }
        ),
    }

    with pd.ExcelWriter(PLANILHA) as writer:
        for sheet_name, df in data_frames.items():
            df.to_excel(excel_writer=writer, sheet_name=sheet_name, index=False)

except connector.DatabaseError as e:
    print(f"Something went wrong while creating the report :/\n {e}")
finally:
    if cursor is not None:
        cursor.close()
    if connection is not None:
        connection.close()
