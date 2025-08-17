import os

from dotenv import load_dotenv
import pandas as pd

from services.queries import (
    billing_by_state,
    late_deliveries,
    top5_month_products,
    top_clients,
    sales_history,
)

load_dotenv()

REPORT_PATH = os.getenv(key="REPORT_PATH", default="report.xlsx")


def create_report():
    data_frames = {
        "Top 5 Produtos do Mês": pd.DataFrame(top5_month_products()),
        "Top Clientes": pd.DataFrame(top_clients()),
        "Entregas Atrasadas": pd.DataFrame(late_deliveries()),
        "Faturamento por Estado": pd.DataFrame(billing_by_state()),
        "Histórico de Vendas": pd.DataFrame(sales_history()),
    }

    with pd.ExcelWriter(path=REPORT_PATH) as writer:
        for sheet_name, df in data_frames.items():
            df.to_excel(excel_writer=writer, sheet_name=sheet_name, index=False)


if __name__ == "__main__":
    create_report()
