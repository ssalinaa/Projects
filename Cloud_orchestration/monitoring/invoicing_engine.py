import datetime
import time
from typing import List

class InvoicingEngine:
    """
    Генератор на финансови отчети и фактури.
    Архивира историята на транзакциите за одит.
    """

    def __init__(self):
        self._invoice_archive: List[dict] = []

    def generate_monthly_invoice(self, tenant_id: str, amount: float):
        invoice_id = f"INV-{tenant_id}-{int(time.time())}"
        invoice_data = {
            "invoice_id": invoice_id,
            "date": datetime.now().isoformat(),
            "amount": amount,
            "status": "ISSUED"
        }
        self._invoice_archive.append(invoice_data)
        print(f"[BILLING] Invoice {invoice_id} generated: ${amount}")
        return invoice_id

    def get_unpaid_total(self) -> float:
        return sum(inv["amount"] for inv in self._invoice_archive if inv["status"] == "ISSUED")