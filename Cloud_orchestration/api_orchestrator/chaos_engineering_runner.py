import random

class ChaosEngineeringRunner:
    """
    Нарочно въвежда повреди, за да тества устойчивостта на облака.
    'Най-добрият начин да избегнеш авария е да я предизвикаш сам'.
    """
    def inject_failure(self, cluster: 'CloudProvider'):
        target = random.choice(cluster.get_active_hosts())
        print(f"[CHAOS-MONKEY] Terminating random host: {target.name} to test HA.")
        target.power_off() # Тестваме дали HAController ще реагира