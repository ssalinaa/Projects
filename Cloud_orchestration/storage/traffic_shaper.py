class TrafficShaper:
    """
    Контролира честотната лента и приоритизира трафика.
    Предотвратява 'задушаването' на критични услуги от по-малко важни процеси.
    """

    def __init__(self):
        self._priority_queues = {"HIGH": 0.7, "MEDIUM": 0.2, "LOW": 0.1}

    def allocate_bandwidth(self, service_type: str, total_mbps: int):
        priority = "LOW"
        if service_type in ["VOICE", "VIDEO_CONF"]:
            priority = "HIGH"
        elif service_type == "DB_SYNC":
            priority = "MEDIUM"

        allowed = total_mbps * self._priority_queues[priority]
        print(f"[SHAPER] Service {service_type} allocated {allowed} Mbps (Priority: {priority})")
        return allowed