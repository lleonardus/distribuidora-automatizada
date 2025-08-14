import os
from dotenv import load_dotenv
import sqlite3 as connector
import pandas as pd

load_dotenv()

DATABASE = os.getenv("DATABASE") or "distribuidora.db"
REPORT_PATH = os.getenv("REPORT_PATH") or "relatorio.xlsx"

connection = None
cursor = None

try:
    connection = connector.connect(DATABASE)
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
    SELECT e.id, c.nome_cliente, e.data_prevista, e.data_entrega, (julianday(e.data_entrega) - julianday(e.data_prevista)) AS dias_de_atraso
      FROM entregas e
      JOIN pedidos pe ON  pe.id = e.pedido_id
      JOIN clientes c ON  c.id = pe.cliente_id
      WHERE data_entrega > data_prevista
    ORDER BY dias_de_atraso DESC, c.nome_cliente ASC;
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
                "Produto": [row[0] for row in top5_month_products],
                "Total Vendido": [row[1] for row in top5_month_products],
            }
        ),
        "Top Clientes": pd.DataFrame(
            {
                "Cliente": [row[0] for row in top_clients],
                "Total Gasto": [row[1] for row in top_clients],
            }
        ),
        "Entregas Atrasadas": pd.DataFrame(
            {
                "Entrega Id": [row[0] for row in late_deliveries],
                "Cliente": [row[1] for row in late_deliveries],
                "Data Prevista": [row[2] for row in late_deliveries],
                "Data de Entrega": [row[3] for row in late_deliveries],
                "Atraso em Dias": [row[4] for row in late_deliveries],
            }
        ),
        "Faturamento por Estado": pd.DataFrame(
            {
                "Estado": [row[0] for row in billing_by_state],
                "Faturamento": [row[1] for row in billing_by_state],
            }
        ),
    }

    with pd.ExcelWriter(REPORT_PATH) as writer:
        for sheet_name, df in data_frames.items():
            df.to_excel(excel_writer=writer, sheet_name=sheet_name, index=False)

except connector.DatabaseError as e:
    print(f"Something went wrong while creating the report :/\n {e}")
finally:
    if cursor is not None:
        cursor.close()
    if connection is not None:
        connection.close()
