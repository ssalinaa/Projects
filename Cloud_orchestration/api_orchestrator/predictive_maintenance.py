import random

class PredictiveMaintenance:
    """
    Интелигентен модул за предсказване на хардуерни дефекти.
    Намалява Downtime чрез превантивни действия.
    """
    def __init__(self, metrics_collector: 'MetricsCollector'):
        self._collector = metrics_collector
        self._failure_probability = 0.05 # 5%

    def analyze_health_trends(self, host_id: str):
        """Анализира тенденциите и вдига аларма при аномалии."""
        # Симулация на ML модел, който открива нарастваща температура
        prediction = random.random()
        if prediction < self._failure_probability:
            print(f"[PREDICTIVE] High risk of failure detected for Host {host_id} in the next 24h!")
            return "MIGRATE_IMMEDIATELY"
        return "HEALTHY"