from typing import Dict

class GlobalLoadBalancer:
    """
    Управлява трафика на глобално ниво чрез DNS политики.
    Осигурява Disaster Recovery чрез пренасочване при срив на цял регион.
    """
    def __init__(self):
        self._regions: Dict[str, str] = {
            "EU-WEST": "1.1.1.1",
            "US-EAST": "2.2.2.2",
            "ASIA-PACIFIC": "3.3.3.3"
        }
        self._health_status: Dict[str, bool] = {r: True for r in self._regions}

    def resolve_request(self, user_country: str) -> str:
        """Насочва потребителя към най-близкия здрав регион."""
        if user_country in ["BG", "UK", "DE"]:
            target = "EU-WEST"
        elif user_country in ["JP", "CN"]:
            target = "ASIA-PACIFIC"
        else:
            target = "US-EAST"

        # Failover логика: ако регионът е 'паднал', избери резервен
        if not self._health_status[target]:
            print(f"[GSLB] Region {target} is DOWN. Redirecting to US-EAST.")
            return self._regions["US-EAST"]

        print(f"[GSLB] Routing user from {user_country} to {target}")
        return self._regions[target]

    def set_region_status(self, region: str, is_up: bool):
        self._health_status[region] = is_up