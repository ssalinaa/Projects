import time
from typing import Dict

class SubscriptionService:
    """
    Управлява дългосрочни абонаменти и резервиран капацитет.
    Гарантира наличието на ресурси за приоритетни клиенти.
    """

    def __init__(self):
        # tenant_id -> subscription_info
        self._active_subscriptions: Dict[str, dict] = {}

    def purchase_reservation(self, tenant_id: str, resource_type: str, duration_months: int):
        sub_id = f"SUB-{tenant_id}-{int(time.time())}"
        self._active_subscriptions[tenant_id] = {
            "sub_id": sub_id,
            "type": resource_type,
            "expiry": time.time() + (duration_months * 30 * 86400),
            "discount": 0.40
        }
        print(f"[SUBSCRIPTION] Tenant {tenant_id} reserved {resource_type} for {duration_months} months.")