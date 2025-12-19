from typing import List

class CostOptimizer:
    """
    Интелигентен съветник за оптимизация на облачните разходи.
    Търси 'Idle' или 'Underutilized' ресурси.
    """

    def __init__(self, metrics: 'MetricsCollector'):
        self._metrics = metrics

    def analyze_vms(self, tenant_vms: List[str]):
        """Сканира натоварването и дава препоръки."""
        recommendations = []
        for vm_id in tenant_vms:
            avg_load = self._metrics.get_average_load(vm_id, window=100)

            if avg_load < 10.0:
                recommendations.append(f"DOWNSIZE: VM {vm_id} (Usage: {avg_load}%) - Save up to 50% cost.")
            elif avg_load > 85.0:
                recommendations.append(f"SCALE UP: VM {vm_id} (Usage: {avg_load}%) - Risk of performance degradation.")

        return recommendations