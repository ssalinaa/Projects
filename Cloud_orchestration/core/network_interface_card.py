import random
import re

class NetworkInterfaceCard:
    """
    Симулира виртуална мрежова карта (vNIC).
    Отговаря за мрежовата идентичност и контрола на трафика на виртуалната единица.
    """

    def __init__(self, interface_id: str, network_type: str = "NAT"):
        self._interface_id = interface_id
        self._network_type = network_type  # Опции: NAT, Bridge, Internal, Host-only

        # Генериране на уникален виртуален MAC адрес (стандарт във виртуализацията)
        self._mac_address = self._generate_virtual_mac()

        self._ip_address = "0.0.0.0"
        self._is_link_up = False

        # Лимити на трафика (Quality of Service - QoS) в Mbps
        self._bandwidth_limit = 1000.0
        self._total_data_transmitted = 0.0  # в MB

    def _generate_virtual_mac(self) -> str:
        """Генерира виртуален MAC адрес, започващ с '08:00:27' (типичен за VirtualBox/Oracle)."""
        hex_chars = "0123456789ABCDEF"
        suffix = ":".join("".join(random.sample(hex_chars, 2)) for _ in range(3))
        return f"08:00:27:{suffix}"

    def connect_to_network(self) -> bool:
        """Симулира вкарването на мрежовия кабел (Link Up)."""
        print(f"vNIC {self._interface_id}: Establishing link to {self._network_type} network...")
        self._is_link_up = True
        return self._is_link_up

    def disconnect(self):
        """Симулира прекъсване на мрежовата връзка."""
        self._is_link_up = False
        self._ip_address = "0.0.0.0"
        print(f"vNIC {self._interface_id}: Link down.")

    def assign_ip(self, ip: str):
        """Валидира и задава IP адрес на интерфейса."""
        ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        if re.match(ip_pattern, ip):
            self._ip_address = ip
            print(f"vNIC {self._interface_id}: IP {ip} assigned successfully.")
        else:
            raise ValueError(f"Invalid IP address: {ip}")

    @property
    def status_report(self) -> dict:
        """Връща детайлен статус на мрежовия интерфейс."""
        return {
            "interface": self._interface_id,
            "mac": self._mac_address,
            "ip": self._ip_address,
            "connected": self._is_link_up,
            "type": self._network_type,
            "usage_mb": round(self._total_data_transmitted, 2)
        }

    def simulate_traffic(self, amount_mb: float):
        """Регистрира преминалия трафик за целите на мониторинга."""
        if not self._is_link_up:
            print(f"vNIC {self._interface_id}: Cannot send data. Link is down.")
            return

        if amount_mb > self._bandwidth_limit / 8:  # Опростена проверка за капацитет
            print(f"vNIC {self._interface_id}: Bandwidth throttling engaged!")

        self._total_data_transmitted += amount_mb