from _ast import Dict
from enum import Enum
import time
from typing import List

class AlertLevel(Enum):
    INFO = "Information"
    WARNING = "Warning"
    CRITICAL = "Critical"
    RESOLVED = "Resolved"

class NotificationService:
    """
    Управлява изпращането на известия към администраторите.
    Интегрира се с външни системи за известяване.
    """

    def __init__(self):
        self._subscribers: Dict[str, List[str]] = {
            "EMAIL": [],
            "SLACK": [],
            "SMS": []
        }
        self._alert_history = []

    def subscribe(self, channel: str, endpoint: str):
        """Регистрира нов получател (напр. email адрес или Slack webhook)."""
        channel = channel.upper()
        if channel in self._subscribers:
            self._subscribers[channel].append(endpoint)
            print(f"[NOTIFY] Registered {endpoint} to {channel} channel.")

    def notify(self, level: AlertLevel, message: str, source: str = "System"):
        """Изпраща аларма през всички регистрирани канали."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        alert_msg = f"[{timestamp}] [{level.value}] {source}: {message}"

        self._alert_history.append(alert_msg)

        if level == AlertLevel.CRITICAL:
            self._send_to_channel("SMS", f"URGENT: {alert_msg}")
            self._send_to_channel("SLACK", f"<!channel>  {alert_msg}")

        self._send_to_channel("EMAIL", alert_msg)

    def _send_to_channel(self, channel: str, content: str):
        """Вътрешен метод за комуникация с API-тата на доставчиците."""
        endpoints = self._subscribers.get(channel, [])
        for endpoint in endpoints:
            print(f"[SENDING {channel} to {endpoint}]: {content[:60]}...")

    def get_alert_logs(self, limit: int = 10) -> List[str]:
        """Връща последните регистрирани аларми за одит."""
        return self._alert_history[-limit:]