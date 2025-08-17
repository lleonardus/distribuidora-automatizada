import os

from dotenv import load_dotenv
import pandas as pd

from services.queries import (
    billing_by_state,
    late_deliveries,
    top5_month_products,
    top_clients,
)

load_dotenv()

REPORT_PATH = os.getenv(key="REPORT_PATH", default="report.xlsx")


def create_report():
    data_frames = {
        "Top 5 Produtos do Mês": pd.DataFrame(
            {
                "Produtos": [row[0] for row in top5_month_products()],
                "Total Vendido": [row[1] for row in top5_month_products()],
            }
        ),
        "Top Clientes": pd.DataFrame(
            {
                "Cliente": [row[0] for row in top_clients()],
                "Total Gasto": [row[1] for row in top_clients()],
            }
        ),
        "Entregas Atrasadas": pd.DataFrame(
            {
                "Entrega Id": [row[0] for row in late_deliveries()],
                "Cliente": [row[1] for row in late_deliveries()],
                "Data Prevista": [row[2] for row in late_deliveries()],
                "Data de Entrega": [row[3] for row in late_deliveries()],
                "Atraso em Dias": [row[4] for row in late_deliveries()],
            }
        ),
        "Faturamento por Estado": pd.DataFrame(
            {
                "Estado": [row[0] for row in billing_by_state()],
                "Faturamento": [row[1] for row in billing_by_state()],
            }
        ),
    }

    with pd.ExcelWriter(path=REPORT_PATH) as writer:
        for sheet_name, df in data_frames.items():
            df.to_excel(excel_writer=writer, sheet_name=sheet_name, index=False)


if __name__ == "__main__":
    create_report()
