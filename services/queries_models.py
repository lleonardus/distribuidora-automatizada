from datetime import date


class Top5MonthProduct:
    def __init__(self, product_name: str, total_sold: int):
        self.product_name = product_name
        self.total_sold = total_sold


class TopClient:
    def __init__(self, client_name: str, total_expense: float):
        self.client_name = client_name
        self.total_expense = total_expense


class LateDelivery:
    def __init__(
        self,
        delivery_id: int,
        client_name: str,
        expected_date: date,
        delivery_date: date,
        days_late: int,
    ):
        self.delivery_id = delivery_id
        self.client_name = client_name
        self.expected_date = expected_date
        self.delivery_date = delivery_date
        self.days_late = days_late


class BillingByState:
    def __init__(self, state: str, total_value: float):
        self.state = state
        self.total_value = total_value
