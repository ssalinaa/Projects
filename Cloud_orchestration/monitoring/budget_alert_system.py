from typing import Dict
from providers.notification_service import AlertLevel

class BudgetAlertSystem:
    """
    Следи разходите в реално време спрямо зададени бюджети.
    Изпраща известия при достигане на 50%, 80% и 100% от лимита.
    """

    def __init__(self, notifier: 'NotificationService'):
        self._notifier = notifier
        self._budgets: Dict[str, float] = {} # tenant_id -> budget_amount

    def set_budget(self, tenant_id: str, amount: float):
        self._budgets[tenant_id] = amount

    def check_thresholds(self, tenant_id: str, current_spend: float):
        limit = self._budgets.get(tenant_id, 0)
        if limit == 0: return

        percentage = (current_spend / limit) * 100
        if percentage >= 100:
            self._notifier.notify(AlertLevel.CRITICAL, f"Budget EXCEEDED for {tenant_id}!", "Budget-Svc")
        elif percentage >= 80:
            self._notifier.notify(AlertLevel.WARNING, f"Budget at 80% for {tenant_id}", "Budget-Svc")