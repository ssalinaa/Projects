class BillingCalculator:
    """
    Пресмята дължимите суми на база на ценова листа (Rate Card).
    Поддържа различни валути и данъчни ставки.
    """

    def __init__(self, currency: str = "USD"):
        self.currency = currency
        self._rates = {
            "cpu_hour": 0.05,
            "ram_gb_hour": 0.01,
            "storage_gb_month": 0.10
        }

    def calculate_invoice(self, usage_report: dict) -> float:
        """Изчислява финалната сума за конкретен ресурс."""
        cpu_cost = usage_report["cpu_hours"] * self._rates["cpu_hour"]
        ram_cost = usage_report["ram_gb_hours"] * self._rates["ram_gb_hour"]

        subtotal = cpu_cost + ram_cost
        tax = subtotal * 0.20

        return round(subtotal + tax, 2)

    def apply_discount(self, amount: float, promo_code: str) -> float:
        if promo_code == "CLOUD_NEWBIE":
            return amount * 0.90
        return amount