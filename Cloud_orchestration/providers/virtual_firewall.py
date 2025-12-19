from enum import Enum
from typing import List, Dict, Set

class TrafficDirection(Enum):
    INGRESS = "Incoming"
    EGRESS = "Outgoing"

class FirewallPolicy(Enum):
    ALLOW = "Allow"
    DENY = "Deny"

class VirtualFirewall:
    """
    Симулира виртуален firewall, прикрепен към мрежовия интерфейс на ресурс.
    Осигурява мрежова изолация и защита срещу неоторизиран достъп.
    """

    def __init__(self, name: str):
        self._name = name
        # Списък от правила: {"port": 80, "direction": INGRESS, "policy": ALLOW}
        self._rules: List[Dict] = []
        self._default_policy = FirewallPolicy.DENY # Принцип на максимална сигурност
        self._blocked_ips: Set[str] = set()

    def add_rule(self, port: int, protocol: str, direction: TrafficDirection, policy: FirewallPolicy):
        """Добавя ново правило за филтриране на трафика."""
        rule = {
            "port": port,
            "protocol": protocol.upper(),
            "direction": direction,
            "policy": policy
        }
        self._rules.append(rule)
        print(f"[FIREWALL: {self._name}] Added rule: {policy.value} {protocol} on port {port} ({direction.value})")

    def inspect_packet(self, remote_ip: str, port: int, protocol: str, direction: TrafficDirection) -> bool:
        """
        Проверява дали даден пакет може да премине.
        Това е сърцето на мрежовата сигурност във виртуализацията.
        """
        if remote_ip in self._blocked_ips:
            return False

        for rule in self._rules:
            if (rule["port"] == port and
                rule["protocol"] == protocol.upper() and
                rule["direction"] == direction):
                return rule["policy"] == FirewallPolicy.ALLOW

        return self._default_policy == FirewallPolicy.ALLOW

    def block_ip(self, ip_address: str):
        """Динамично блокиране на злонамерен адрес (IP Blacklisting)."""
        self._blocked_ips.add(ip_address)
        print(f"[FIREWALL: {self._name}] IP {ip_address} has been blacklisted.")

    def get_active_config(self) -> str:
        """Връща списък с всички активни правила за одит."""
        config = [f"--- Firewall Config: {self._name} ---"]
        for r in self._rules:
            config.append(f"{r['direction'].value}: {r['policy'].value} {r['protocol']} {r['port']}")
        return "\n".join(config)